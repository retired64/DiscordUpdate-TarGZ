import sys
import os
import subprocess
import tempfile
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QLabel, QPushButton, QMessageBox)
from PySide6.QtCore import Qt, QProcess, QTimer

# --- SCRIPT BASH INCRUSTADO ---
# Este es tu script original, pero preparado para ser inyectado dinámicamente.
# Usamos {tar_path} como marcador para insertar la ruta detectada por Python.
INSTALL_SCRIPT_TEMPLATE = r"""#!/bin/bash
# Script generado temporalmente por el instalador

DISCORD_TAR="{tar_path}"
echo "Iniciando instalación para: $DISCORD_TAR"

# 1. Crear directorio temporal para extracción
TEMP_DIR=$(mktemp -d)
tar -xzf "$DISCORD_TAR" -C "$TEMP_DIR"

# 2. Buscar la carpeta extraída
DISCORD_FOLDER=$(find "$TEMP_DIR" -type d -name "Discord" | head -n 1)

if [ -z "$DISCORD_FOLDER" ]; then
    echo "Error: No se encontró la carpeta Discord dentro del archivo."
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 3. Limpieza previa
if [ -d "/usr/share/discord" ]; then
    rm -rf /usr/share/discord
fi

# 4. Mover a /usr/share
mv "$DISCORD_FOLDER" /usr/share/discord

# 5. Configurar permisos y accesos directos
chmod +x /usr/share/discord/Discord

# Crear archivo .desktop
cat <<EOF > /usr/share/discord/discord.desktop
[Desktop Entry]
Name=Discord
StartupWMClass=discord
Comment=All-in-one voice and text chat for gamers
GenericName=Internet Messenger
Exec=/usr/share/discord/Discord
Icon=/usr/share/discord/discord.png
Type=Application
Categories=Network;InstantMessaging;
Terminal=false
StartupNotify=true
EOF

cp /usr/share/discord/discord.desktop /usr/share/applications/

# Enlace simbólico
rm -f /usr/local/bin/discord
ln -s /usr/share/discord/Discord /usr/local/bin/discord

# Actualizar base de datos
update-desktop-database

# Limpiar
rm -rf "$TEMP_DIR"

echo "Instalación completada con éxito."
"""

class DiscordInstallerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Discord Installer")
        self.setFixedSize(400, 480)
        
        # Estilos generales (Tema Oscuro + Tipografía)
        self.setStyleSheet("""
            QMainWindow { background-color: #23272A; }
            QLabel { color: #FFFFFF; font-family: 'Segoe UI', sans-serif; }
        """)

        # Layout Principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        self.layout.setSpacing(15)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 1. Título
        self.title = QLabel("DISCORD\nUPDATER")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 32px; font-weight: 900; color: #5865F2; margin-bottom: 10px;")
        self.layout.addWidget(self.title)

        # 2. Icono simulado (Círculo)
        self.icon_label = QLabel("🚀")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 60px; margin-bottom: 20px;")
        self.layout.addWidget(self.icon_label)

        # 3. Estado
        self.status_label = QLabel("Escaneando sistema...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: #99AAB5;")
        self.layout.addWidget(self.status_label)

        # Espaciador
        self.layout.addSpacing(20)

        # 4. Botón 3D (Estilo CSS puro)
        self.install_btn = QPushButton("BUSCANDO...")
        self.install_btn.setFixedSize(260, 70)
        self.install_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.install_btn.setEnabled(False)
        
        # CSS para efecto 3D
        self.btn_style_normal = """
            QPushButton {
                background-color: #5865F2;
                color: white; font-size: 16px; font-weight: bold;
                border-radius: 20px;
                border-bottom: 6px solid #38409e;
                margin-top: 0px;
            }
            QPushButton:hover { background-color: #4752C4; }
            QPushButton:pressed {
                border-bottom: 0px;
                margin-top: 6px;
            }
        """
        self.btn_style_disabled = """
            QPushButton {
                background-color: #40444B;
                color: #72767D; font-size: 16px; font-weight: bold;
                border-radius: 20px; border-bottom: 6px solid #2C2F33;
            }
        """
        self.install_btn.setStyleSheet(self.btn_style_disabled)
        self.install_btn.clicked.connect(self.start_installation)
        self.layout.addWidget(self.install_btn)

        # 5. Pie de página
        self.footer = QLabel("v2.0 | Single File Edition")
        self.footer.setStyleSheet("color: #40444B; font-size: 10px; margin-top: 20px;")
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.footer)

        # Buscar archivo al iniciar
        QTimer.singleShot(500, self.find_file)
        self.tar_file = None

    def find_file(self):
        """Busca automáticamente el tar.gz en Descargas"""
        downloads = Path.home() / "Descargas"
        if not downloads.exists():
            downloads = Path.home() / "Downloads"

        found = None
        if downloads.exists():
            files = list(downloads.glob("discord-*.tar.gz"))
            if files:
                # Tomar el más nuevo
                found = max(files, key=os.path.getctime)

        if found:
            self.tar_file = str(found)
            filename = found.name
            self.status_label.setText(f"Listo para instalar:\n{filename}")
            self.status_label.setStyleSheet("color: #57F287; font-weight: bold;")
            self.install_btn.setText("INSTALAR / ACTUALIZAR")
            self.install_btn.setStyleSheet(self.btn_style_normal)
            self.install_btn.setEnabled(True)
        else:
            self.status_label.setText("No se encontró discord-*.tar.gz\nen la carpeta Descargas.")
            self.status_label.setStyleSheet("color: #ED4245; font-weight: bold;")
            self.install_btn.setText("ARCHIVO NO ENCONTRADO")
            self.install_btn.setStyleSheet(self.btn_style_disabled)

    def start_installation(self):
        if not self.tar_file: return

        # Crear archivo temporal con el script bash
        try:
            # 1. Preparar el script inyectando la ruta del archivo
            script_content = INSTALL_SCRIPT_TEMPLATE.format(tar_path=self.tar_file)
            
            # 2. Crear archivo temporal en el sistema (/tmp/...)
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as tmp_script:
                tmp_script.write(script_content)
                tmp_script_path = tmp_script.name

            # 3. Dar permisos de ejecución al temporal
            os.chmod(tmp_script_path, 0o755)

            # 4. Ejecutar con pkexec (pide contraseña gráfica)
            self.install_btn.setText("INSTALANDO...")
            self.install_btn.setEnabled(False)
            self.repaint()

            # Usamos QProcess para no bloquear completamente la UI
            process = QProcess()
            # pkexec ejecutará nuestro script temporal como root
            process.start("pkexec", [tmp_script_path])
            process.waitForFinished()

            # 5. Limpieza y Resultados
            os.remove(tmp_script_path) # Borrar script temporal

            if process.exitCode() == 0:
                QMessageBox.information(self, "¡Éxito!", "Discord se actualizó correctamente.")
                self.close()
            elif process.exitCode() == 126 or process.exitCode() == 127:
                 # Cancelado por usuario
                self.install_btn.setText("INSTALAR / ACTUALIZAR")
                self.install_btn.setEnabled(True)
            else:
                err = process.readAllStandardError().data().decode()
                QMessageBox.critical(self, "Error", f"Falló la instalación.\n\n{err}")
                self.install_btn.setText("REINTENTAR")
                self.install_btn.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", str(e))
            self.install_btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiscordInstallerApp()
    window.show()
    sys.exit(app.exec())
