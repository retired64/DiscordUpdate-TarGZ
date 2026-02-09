Guía de Empaquetado (Binario → AppImage)

### 1. Requisitos Previos

En tu carpeta de trabajo debes tener solamente estos 3 archivos:

1. **`discord-updater`** (Tu ejecutable/binario ya compilado).
2. **`icon.png`** (Tu icono).
3. **`appimagetool-*.AppImage`** (La herramienta de creación).

### 2. El Script de Empaquetado (`package.sh`)

Crea un archivo llamado `package.sh`, pega el siguiente código y dale permisos (`chmod +x package.sh`).

Este script toma tu binario y construye la AppImage automáticamente.

```bash
#!/bin/bash

# --- CONFIGURACIÓN ---
APP_NAME="discord-updater"  # Nombre exacto de tu binario
PRETTY_NAME="Discord Updater" # Nombre bonito para el menú
VERSION="1.0"               # Cambia esto en cada versión

# 1. Limpieza de entorno
echo "🧹 Limpiando carpeta AppDir antigua..."
rm -rf AppDir *.AppImage

# 2. Crear estructura de carpetas estándar de Linux
echo "📂 Creando estructura de directorios..."
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps

# 3. Copiar tus archivos (Binario e Icono)
echo "📋 Copiando binario e icono..."
# Copiamos el ejecutable a /usr/bin/
cp "$APP_NAME" "AppDir/usr/bin/$APP_NAME"

# Copiamos el icono a varios lugares necesarios
cp "icon.png" "AppDir/$APP_NAME.png"
cp "icon.png" "AppDir/.DirIcon"
cp "icon.png" "AppDir/usr/share/icons/hicolor/256x256/apps/$APP_NAME.png"

# 4. Crear el archivo .desktop (Lanzador)
echo "📝 Generando archivo .desktop..."
cat <<EOF > AppDir/$APP_NAME.desktop
[Desktop Entry]
Type=Application
Name=$PRETTY_NAME
Exec=$APP_NAME
Icon=$APP_NAME
Categories=Utility;System;
Terminal=false
StartupNotify=true
EOF

# Mover el .desktop a su sitio
cp "AppDir/$APP_NAME.desktop" "AppDir/usr/share/applications/"

# 5. Crear el enlace maestro (AppRun)
echo "🔗 Conectando AppRun..."
# Esto le dice a la AppImage qué ejecutar al hacer doble clic
ln -s "usr/bin/$APP_NAME" "AppDir/AppRun"

# 6. Permisos de ejecución
chmod +x AppDir/AppRun
chmod +x "AppDir/usr/bin/$APP_NAME"
chmod +x "AppDir/$APP_NAME.desktop"

# 7. Generar la AppImage final
echo "📦 Generando archivo final..."
# Detecta cualquier versión de appimagetool que tengas en la carpeta
TOOL=$(find . -name "appimagetool-*.AppImage" | head -n 1)

if [ -z "$TOOL" ]; then
    echo "❌ Error: No encuentro appimagetool-*.AppImage en esta carpeta."
    exit 1
fi

# Ejecuta la herramienta definiendo la arquitectura
ARCH=x86_64 "$TOOL" AppDir

echo "✅ ¡LISTO! Tu AppImage se ha creado correctamente."

```

### 3. Cómo usarlo (Flujo de trabajo)

Cada vez que tengas un nuevo binario `discord-updater`:

1. Pon el binario en la carpeta junto con el script.
2. Ejecuta:
```bash
./package.sh

```


3. ¡Listo! Aparecerá el archivo `.AppImage` nuevo.
