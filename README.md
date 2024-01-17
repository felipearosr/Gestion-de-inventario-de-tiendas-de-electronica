## Gestión de inventario de tiendas de electrónica 

Este código es un sistema de gestión de inventario para tiendas de electrónica utilizando Flask para el servidor backend y Streamlit para la interfaz de usuario. Para el ramo Arquitecturade Software.

### Prerrequisitos

Necesitarás tener instalados los siguientes módulos de Python:
- Flask
- SQLAlchemy
- requests
- pandas
- fpdf
- streamlit
- streamlit_modal

Puedes instalarlos usando pip:

```shell
pip install Flask SQLAlchemy requests pandas fpdf streamlit streamlit_modal
```

### Cómo ejecutar

1. Ejecute `server.py` con el comando `python server.py`para iniciar el servidor Flask. Este servidor se iniciará en http://localhost:5000
2. Ejecute `client.py` con el comando `streamlit run client.py` para iniciar la aplicación Streamlit. Esta aplicación se conectará al servidor Flask para realizar todas las operaciones CRUD en la base de datos.

### Funcionalidades

La aplicación permite a los usuarios realizar las siguientes operaciones en la base de datos:

1. Agregar productos: Para agregar un producto, complete los campos proporcionados y haga clic en el botón "Añadir Producto". Los campos proporcionados incluyen nombre, descripción, precio, url de la imagen, cantidad, ID del proveedor, ventas, categorías, marca y modelo.

2. Actualizar productos: Los productos existentes pueden ser actualizados seleccionando el producto correspondiente, editando los campos deseados y haciendo clic en el botón "Actualizar Producto".

3. Eliminar productos: Para eliminar un producto, simplemente seleccione el producto correspondiente y haga clic en el botón "Borrar Producto".

4. Ver todos los productos: Todos los productos se muestran en un formato tabular, lo que permite una fácil visualización y manipulación de los datos.

5. Exportar los datos: Los datos se pueden exportar como un archivo CSV o PDF. Seleccione el formato que desea exportar como y haga clic en el botón "Exportar como".

### API

El servidor Flask proporciona la siguiente API RESTful para manipular los datos de los productos:

1. POST /add_product: Añade un nuevo producto a la base de datos.
2. PUT /update_product/{product_id}: Actualiza un producto existente en la base de datos.
3. DELETE /remove_product/{product_id}: Elimina un producto existente de la base de datos.
4. GET /products: Recupera todos los productos de la base de datos.
5. PUT /add_category/{product_id}: Añade una nueva categoría a un producto existente.
6. PUT /update_all_products: Actualiza todos los productos con los mismos datos nuevos.

El servidor utiliza SQLite para la base de datos, y SQLAlchemy para ORM (Object Relational Mapping).

### Populate

Utilizar el script `populate.py` para popular su base de datos con datos ficticios.

## Requisitos

Antes de poder utilizar este script, asegúrese de haber instalado las siguientes bibliotecas de Python:

- faker
- requests
- random

Puede instalar estas bibliotecas utilizando el siguiente comando:

```
pip install faker requests
```

## Uso

El script `populate.py` tiene el objetivo de crear productos ficticios y agregarlos a su base de datos. El código se compone de tres funciones principales:

- `add_product()`: Esta función toma varios parámetros, crea un diccionario de datos de producto y envía una solicitud POST al servidor para agregar el producto a la base de datos.

- `generate_product()`: Esta función utiliza la biblioteca `faker` para generar datos ficticios para cada campo del producto. Luego llama a la función `add_product()` para agregar el producto a la base de datos.

- `populate_database()`: Esta función llama a `generate_product()` un número determinado de veces para generar múltiples productos. Puede controlar la cantidad de productos que se generarán cambiando el parámetro `num_products`.

Para popular la base de datos, simplemente ejecute el script en su terminal con el siguiente comando:

```
python populate.py
```

El código incluye una llamada a `populate_database(30)` al final, lo que significa que se generarán y agregarán 30 productos a la base de datos cuando se ejecute el script. Puede cambiar este número según sus necesidades.

## Personalización

Puede personalizar la forma en que se generan los productos editando la función `generate_product()`. Por ejemplo, puede cambiar el rango de precios o la cantidad de categorías que se generarán para cada producto. Por favor, siéntase libre de adaptar el script a sus necesidades.

Recuerde que si cambia la estructura de los datos del producto en `add_product()`, también deberá hacer los cambios correspondientes en su servidor y base de datos para aceptar los nuevos datos.

## Finalmente

Este script es una excelente forma de popular rápidamente su base de datos con datos de productos ficticios para pruebas y desarrollo. Esperamos que le sea de utilidad.
