# Aplicación Web Vulnerable - Laboratorio

**ADVERTENCIA: Esta aplicación contiene vulnerabilidades intencionales. NO DESPLEGAR EN ENTORNOS DE PRODUCCIÓN.**

Esta aplicación web ha sido diseñada específicamente para contener vulnerabilidades comunes que pueden ser detectadas por herramientas como Dynatrace. Su propósito es educativo y de pruebas de seguridad controladas.

## Vulnerabilidades Implementadas

1. **Inyección SQL**
2. **Inyección de Comandos**
3. **Validación de Entrada Incorrecta**
4. **SSRF (Server-Side Request Forgery)**

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/carlos-carreno/vulnerable-web-app-lab.git
cd vulnerable-web-app-lab

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Inicializar la base de datos
python init_db.py

# Ejecutar la aplicación
python app.py
```

## Uso Responsable

Esta aplicación debe ser utilizada únicamente en entornos controlados para fines educativos o de pruebas de seguridad. No se recomienda su despliegue en entornos de producción o accesibles públicamente.

## Estructura del Proyecto

- `app.py`: Aplicación principal Flask
- `init_db.py`: Script para inicializar la base de datos SQLite
- `static/`: Archivos estáticos (CSS, JavaScript)
- `templates/`: Plantillas HTML
- `database.db`: Base de datos SQLite