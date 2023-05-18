## Pasos necesarios

### Entorno virtual
```
pip install virtualenv
```


### Creación del entorno virtual
- Luego de descargar virtualenv en su computador, dentro de la carpeta del proyecto
```
virtualenv 'nombre-del-entorno'
```

### Activar el entorno
- En visual studio code presione f1 y escribe Python y selecciona 'seleccionar interprete'

### Instalar dependencias
```
pip install -r requirements.txt
```

### Inicia la api
```
uvicorn main:app --reload
```