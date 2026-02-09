# DiscordUpdate-TarGZ
Herramienta para actualizar la version tar de discord en linux para ser mostrada en el menu de aplicaciones desktop
¡Me parece perfecto! Una aplicación genial no sirve de mucho si el usuario no sabe cómo usarla. Aquí tienes una guía lista para copiar y pegar.
Discord Updater para Linux

**Guía de Uso Rápida**

### ¿Qué es esto?

Es una pequeña herramienta que automatiza la instalación manual de Discord en Linux.
Si usas Discord en Fedora o Arch, etc. sabes que cuando sale una actualización, la aplicación se bloquea cuando la descargaste y usas desde el sitio oficial descargado el tar.gz y esta desactualizado, no es como hacer un sudo dnf/apt install discord o upgrade discord. Te pide descargar un archivo `.tar.gz`. Instalar ese archivo manualmente es tedioso. **Esta aplicación lo hace por ti con un solo clic.**

---

### Requisitos Previos

Solo necesitas una cosa antes de abrir la aplicación:

1. Ve a la página oficial de Discord o haz clic en el aviso de actualización de tu Discord actual.
2. Descarga la versión para Linux **tar.gz**.
3. **¡IMPORTANTE!** Deja el archivo en tu carpeta de **Descargas** (Downloads). No lo descomprimas ni le cambies el nombre.

---

### 🛠️ Cómo usarlo (Paso a Paso)

**1. Abre el Actualizador**
Haz doble clic en el archivo `DiscordUpdater` (o ejecútalo desde tu terminal).

**2. Verificación Automática**
Verás una ventana moderna.

* ✅ **Si el texto está en VERDE:** Significa que la aplicación encontró el archivo de actualización en tus Descargas.
* ❌ **Si el texto está en ROJO:** No se encontró el archivo `.tar.gz`. Revisa que lo hayas descargado correctamente en la carpeta *Descargas*.

**3. Instalar**
Presiona el botón azul **"INSTALAR / ACTUALIZAR"**.

**4. Permisos de Administrador**
Te aparecerá una ventana del sistema pidiéndote tu **contraseña de usuario**.

> *¿Por qué?* Discord se instala en las carpetas del sistema (`/usr/share`), por lo que necesitamos permisos especiales para copiar los archivos allí. Es totalmente seguro.

**5. ¡Listo!**
Una vez termine (tarda unos segundos), verás un mensaje de éxito. Ya puedes abrir Discord normalmente desde tu menú de aplicaciones con la nueva versión instalada.

---

### ❓ Preguntas Frecuentes

* **¿Borrará mis datos de Discord?**
No. Solo actualiza el programa. Tu inicio de sesión, servidores y configuraciones se mantienen intactos.
* **Hago doble clic y no se abre.**
Asegúrate de que el archivo tenga permisos de ejecución.
* *Clic derecho -> Propiedades -> Permisos -> Marcar "Permitir ejecutar el archivo como un programa".*
