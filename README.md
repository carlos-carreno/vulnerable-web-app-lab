# Aplicación Web Vulnerable - Laboratorio

**ADVERTENCIA: Esta aplicación contiene vulnerabilidades intencionales. NO DESPLEGAR EN ENTORNOS DE PRODUCCIÓN.**

Esta aplicación web ha sido diseñada específicamente para contener vulnerabilidades comunes que pueden ser detectadas por herramientas como Dynatrace. Su propósito es educativo y de pruebas de seguridad controladas.

## Vulnerabilidades Implementadas

1. **Inyección SQL**: Consultas SQL construidas dinámicamente con entradas del usuario sin sanitización.
2. **Inyección de Comandos**: Ejecución de comandos del sistema operativo directamente con entrada del usuario.
3. **Validación de Entrada Incorrecta**: Formularios que no validan adecuadamente las entradas.
4. **SSRF (Server-Side Request Forgery)**: Solicitudes a URLs externas o internas sin restricciones.

## Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno
- Terminal/línea de comandos

## Instalación

### Clonar el repositorio

```bash
# Clonar el repositorio
git clone https://github.com/carlos-carreno/vulnerable-web-app-lab.git
cd vulnerable-web-app-lab
```

### Crear un entorno virtual

**En sistemas Unix/Linux/MacOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Inicializar la base de datos

```bash
python init_db.py
```

### Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## Uso del laboratorio

### Credenciales predefinidas

La aplicación viene con usuarios predefinidos:

- **Administrador**: usuario: `admin`, contraseña: `admin123`
- **Usuario común 1**: usuario: `user1`, contraseña: `password123`
- **Usuario común 2**: usuario: `user2`, contraseña: `password456`

### Acceso a las vulnerabilidades

Desde la página principal, puedes acceder a todas las funcionalidades vulnerables:

1. **Inyección SQL:**
   - Formulario de login (`/login`)
   - Búsqueda de productos (`/search`)

2. **Inyección de Comandos:**
   - Herramienta de red (`/network_tool`)
   - Lector de archivos (`/file_reader`)

3. **Validación de Entrada Incorrecta:**
   - Formulario de registro (`/register`)
   - Comentarios de productos (`/comment/add`)

4. **SSRF:**
   - Verificador de sitios web (`/check_website`)
   - API de recursos (`/api/fetch_resource`)

## Explotación de vulnerabilidades

Para obtener detalles sobre cómo explotar cada vulnerabilidad, consulta el archivo [EXPLOTACIÓN.md](EXPLOTACIÓN.md). Allí encontrarás:

- Explicación detallada de cada vulnerabilidad
- Ejemplos de payloads maliciosos
- Instrucciones paso a paso para la explotación
- Mitigaciones recomendadas

## Mantenimiento

### Estructura del proyecto

```
vulnerable-web-app-lab/
├── app.py                # Aplicación principal Flask
├── init_db.py            # Script para inicializar la base de datos
├── requirements.txt      # Dependencias del proyecto
├── database.db           # Base de datos SQLite (generada)
├── README.md             # Este archivo
├── EXPLOTACIÓN.md        # Guía de explotación
└── templates/            # Plantillas HTML
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── search_results.html
    ├── network_tool.html
    ├── file_reader.html
    ├── check_website.html
    └── product_detail.html
```

### Modificaciones y extensiones

Si deseas añadir nuevas vulnerabilidades o modificar las existentes:

1. **Añadir rutas en `app.py`**: Define nuevas funciones con el decorador `@app.route`.
2. **Crear plantillas HTML**: Añade nuevos archivos en el directorio `templates/`.
3. **Actualizar la base de datos**: Modifica `init_db.py` si necesitas nuevas tablas o datos.

### Reiniciar la base de datos

Si necesitas reiniciar la base de datos a su estado inicial:

```bash
python init_db.py
```

Esto eliminará la base de datos existente y creará una nueva con los datos predefinidos.

## Integración con Dynatrace

Para integrar esta aplicación con Dynatrace y detectar las vulnerabilidades:

1. **Instalar el agente Dynatrace**:
   - Sigue las instrucciones de [la documentación oficial de Dynatrace](https://www.dynatrace.com/support/help/technology-support/application-software/python/install-oneagent-python)
   - Normalmente se instala el paquete `oneagent-sdk` y se configura el host de tu instancia Dynatrace

2. **Configurar el agente**:
   ```python
   # Al principio de app.py, añade:
   import dynatrace.oneagent
   dynatrace.oneagent.initialize()
   ```

3. **Ejecutar la aplicación** con el agente activado.

4. **Analizar los resultados en el panel de Dynatrace**:
   - Verifica las secciones de seguridad y vulnerabilidades
   - Revisa los informes de análisis de código y runtime

## Problemas comunes

### La aplicación no inicia
- Verifica que todas las dependencias estén instaladas: `pip install -r requirements.txt`
- Asegúrate de que el puerto 5000 no esté en uso por otra aplicación

### Error en la base de datos
- Si ves errores de SQLite, elimina el archivo `database.db` y ejecuta `python init_db.py`

### No se pueden explotar las vulnerabilidades
- Algunas técnicas de explotación pueden ser bloqueadas por protecciones del navegador
- Intenta usar herramientas como Burp Suite o Postman para manipular las peticiones

## Uso responsable

Esta aplicación debe ser utilizada únicamente en entornos controlados para fines educativos o de pruebas de seguridad. No se recomienda su despliegue en entornos de producción o accesibles públicamente.

## Soporte y recursos

- [Dynatrace Documentation](https://www.dynatrace.com/support/help/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/) - Otro proyecto educativo similar

## Licencia

Este proyecto es solo para fines educativos y de pruebas. No se ofrece garantía ni responsabilidad por su uso.