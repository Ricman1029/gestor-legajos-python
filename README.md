# GeLeDi: Gestor de Legajos Digitales

Sistema de automatización administrativa desarrollado en Python para la gestión de empleados y la generación de contratos y documentación legal. Diseñado para agilizar el proceso de alta de personal, completando automáticamente formularios oficiales (AFIP/ARCA, ART, Seguros) y contratos laborales.

## 🚀 Funcionalidades Principales

* **Gestión Multi-Empresa:** Alta, baja (lógica) y modificación de empresas con sus respectivas razones sociales y datos fiscales.
* **Administración de Personal:** ABM de empleados con gestión de categorías, convenios y sindicatos.
* **Generación de Documentos:**
    * Creación de contratos de ~18 páginas en un solo archivo PDF.
    * Completado de datos en formularios oficiales existentes (AFIP/ARCA, Anses) usando `PyMuPDF`.
    * Generación dinámica de cláusulas contractuales.

## 🛠️ Stack Tecnológico

Este proyecto está construido utilizando tecnologías modernas de Python para escritorio y manipulación de documentos:

* **[Flet](https://flet.dev/):** Framework de UI basado en Flutter para crear interfaces modernas y reactivas en Python.
* **PyMuPDF (Fitz) & pypdf:** Motores potentes para la lectura, renderizado y superposición de datos en formularios oficiales (AFIP/ARCA, ANSES) preexistentes.
* **FPDF2:** Generación dinámica de contratos de texto desde cero.

## ⚙️ Instalación y Configuración

Para ejecutar este proyecto localmente, sigue estos pasos:

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/Ricman1029/gestor-legajos-python
    cd gestor-legajos-python
    ```

2.  **Crear un entorno virtual (Recomendado):**
    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la aplicación:**
    ```bash
    flet run 
    ```
### 🐧 Requisitos adicionales para Linux (Ubuntu/WSL/Debian)

Si ejecutas la aplicación en Linux y obtienes errores relacionados con librerías compartidas (GStreamer), necesitas instalar las dependencias gráficas del sistema:

En Ubuntu:
```bash
sudo apt-get update
sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl libgtk-3-0
```

## Cosas que todavía faltan agregar

- [x] Notificaciones para las diferentes acciones  
- [ ] Selector de carpeta para guardar legajos
- [x] Validación para los campos de fechas
- [ ] Validación para los campos de cuiles
- [ ] Ver empleados activos e inactivos en la lista de empleados
- [ ] Cambiar el estado de los empleados en la lista de empleados
- [x] Agregar lista de las obras sociales existentes
- [x] Agregar lista de los convenios existentes
- [x] Poder actualizar lista de obras sociales
- [x] Agregar lista de categorias de cada empresa
- [x] Agregar lista de sindicatos
- [x] Poder elegir para cada empresa los archivos que conforman el legajo.
- 
