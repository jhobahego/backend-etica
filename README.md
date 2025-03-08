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
