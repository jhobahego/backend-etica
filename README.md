# Backend Software Contable

Este proyecto es un sistema de backend para la gestión de empleados en una empresa, implementado con FastAPI y MongoDB.

El sistema permite la creación, actualización y eliminación de empleados, así como la autenticación de usuarios mediante JWT. Además, se implementa un control de acceso basado en roles (RBAC) para garantizar la seguridad y privacidad de los datos.


## Pasos necesarios

### Entorno virtual
```bash
pip install virtualenv
```


### Creación del entorno virtual
- Luego de descargar virtualenv en su computador, dentro de la carpeta del proyecto
```bash
virtualenv venv
```

- También puedes usar el modulo venv de Python
```bash
python -m venv venv
```


### Activar el entorno
En visual studio code presione f1 y escribe Python y selecciona 'seleccionar interprete'

Tambien puedes usar los siguientes comandos
- En linux
```bash
source venv/bin/activate
```
- En windows
```bash
venv\Scripts\activate
```

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Crear un archivo .env en la raiz del proyecto y agrega las variables de entorno
```bash
# .env
MONGODB_URL=your_mongodb_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Inicia la api
```bash
uvicorn main:app --reload
```

## Autenticación y Roles

El sistema implementa un control de acceso basado en roles (RBAC) con dos tipos de roles:
- `usuario`: Rol por defecto, puede ver y modificar solo sus propios datos
- `admin`: Rol administrativo, tiene acceso completo al sistema

### Configuración del Superusuario

Para establecer un superusuario, agregue las siguientes variables al archivo `.env`:

```
SUPER_USER_CEDULA=123456789  # Número de cédula del superusuario
SUPER_USER_PASSWORD=your_secure_password  # Contraseña del superusuario (sin hash)
```

Cuando un usuario se registre o inicie sesión con estas credenciales, automáticamente será promovido a administrador. Este enfoque permite mantener las credenciales del superusuario seguras y fuera del control de versiones.

### Flujo de Autenticación

1. **Iniciar Sesión**
   ```
   POST /token
   ```
   - Request body (form-data):
     - username: número de cédula
     - password: contraseña
   - Response: Token JWT

2. **Usar el Token**
   - Incluir el token en el header de todas las peticiones:
   ```
   Authorization: Bearer {token}
   ```

### Permisos por Endpoint

- `GET /empleados`: Solo administradores
- `GET /empleados/{num_cedula}`: Admin o el propio usuario
- `POST /empleados`: Público (registro de usuarios)
- `PUT /empleados/{usuario_id}`: Admin o el propio usuario
- `DELETE /empleados/{usuario_id}`: Solo administradores
