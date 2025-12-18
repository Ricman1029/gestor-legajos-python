# GeLeDi: Gestor de Legajos Digitales

Sistema de gestión de empleados y generación de contratos y documentación legal. Diseñado para agilizar el proceso de alta de personal, completando automáticamente 
formularios oficiales (AFIP/ARCA, ART, Seguros) y contratos laborales.

## 🚀 Funcionalidades Principales

* **Gestión Multi-Empresa:** Alta, baja (lógica) y modificación de empresas con sus respectivas razones sociales y datos fiscales.
* **Administración de Personal:** ABM de empleados con gestión de categorías, sindicatos, convenios y obras sociales.

## 🛠️ Stack Tecnológico

Este proyecto está construido utilizando tecnologías modernas de Python para escritorio y manipulación de documentos:

* **[Flet](https://flet.dev/):** Framework de UI basado en Flutter para crear interfaces modernas y reactivas en Python.
* **PyMuPDF:** Utilizado para el rellenado de datos en formularios oficiales (AFIP/ARCA, ANSES, ART) preexistentes.
* **Typst:** Generación dinámica de documentos PDF.

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

- [ ] Selector de carpeta para guardar legajos
- [ ] Poder elegir para cada empresa los archivos que conforman el legajo.
- [ ] Poder agregar y preparar pdfs y formularios para incluir en el contrato.

### Nota adicional
Por ahora solo se pueden crear contratos para las ARTs Galeno, Mapfre y Andina. Proximamente se busca añadir una funcionalidad para poder generar el contrato con cualquier pdf que desée el usuario.

