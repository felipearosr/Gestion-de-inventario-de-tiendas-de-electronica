import requests
import streamlit as st
import pandas as pd
from fpdf import FPDF
import csv
import os
import numpy as np
from streamlit_modal import Modal
import streamlit.components.v1 as components


st.set_page_config(layout="wide")

server_url = 'http://localhost:5000' 

def get_products():
    response = requests.get(f'{server_url}/products')
    return response.json()['products']

def add_product(name, description, price, image_url, quantity, supplier_id, sales, categories, brand, model):
    data = {
        "name": name,
        "description": description,
        "price": price,
        "image_url": image_url,
        "quantity": quantity,
        "supplier_id": supplier_id,
        "sales": sales,
        "categories": categories,
        "brand": brand,
        "model": model
    }
    response = requests.post(f'{server_url}/add_product', json=data)
    return response.json()['message']

def remove_product(product_id):
    response = requests.delete(f'{server_url}/remove_product/{product_id}')
    return response.json()['message']

def update_product(product_id, name=None, description=None, price=None, image_url=None, quantity=None, supplier_id=None, sales=None, categories=None, brand=None, model=None):
    data = {}
    fields = ['name', 'description', 'price', 'image_url', 'quantity', 'supplier_id', 'sales', 'categories', 'brand', 'model']
    values = [name, description, price, image_url, quantity, supplier_id, sales, categories, brand, model]
    
    for i in range(len(fields)):
        field = fields[i]
        value = values[i]
        try:
            # For float values, round them to 2 decimal places
            if isinstance(value, float):
                value = round(value, 2)
            # If value is a list of floats, round each float to 2 decimal places
            elif isinstance(value, list) and all(isinstance(x, float) for x in value):
                value = [round(x, 2) for x in value]

            if value is not None:
                data[field] = value

        except Exception as e:
            print(f"An error occurred when handling the field {field} with value {value}")
            print(e)

    print(f"Data to be sent: {data}")  # This line is added to debug your data.
    response = requests.put(f'{server_url}/update_product/{product_id}', json=data)
    return response.json()['message']

def export_format_selector():
    export_format = st.selectbox("Select File Format", ["Select format", "CSV", "PDF"])
    if export_format != "Select format":
        if st.button(f'Export as {export_format}'):
            products = get_products()
            df = pd.DataFrame(products)
            if export_format == "CSV":
                df.to_csv('products.csv', index=False)
                with open('products.csv', 'r') as file:
                    st.download_button(
                        label=f"Download Products Report as {export_format}",
                        data=file,
                        file_name="products_report.csv",
                        mime="text/csv"
                    )
            elif export_format == "PDF":
                df.to_csv('products_temp.csv', index=False)
                pdf = FPDF()

                # Column titles
                header = list(df.columns)

                # Data loading
                data = []
                with open('products_temp.csv', 'r') as file:
                    for row in csv.reader(file):
                        data.append(row)
                data.pop(0)  # to remove column names which were already in headers

                pdf.set_font('Arial', 'B', 14)
                pdf.add_page()

                # Column widths
                col_width = pdf.w / 4.5
                row_height = pdf.font_size

                for row in data:
                    for item in row:
                        pdf.cell(col_width, row_height*2,
                                 txt=item,
                                 border=1)
                    pdf.ln(row_height*2)

                pdf.output('products.pdf')

                with open('products.pdf', 'rb') as file:
                    st.download_button(
                        label=f"Download Products Report as {export_format}",
                        data=file,
                        file_name="products_report.pdf",
                        mime="application/pdf"
                    )

                # remove temp files
                os.remove('products_temp.csv')
                os.remove('products.pdf')


st.title('Gestión de inventario de tiendas de electrónica')

products = get_products()
df = pd.DataFrame(products)
df = df.where(pd.notnull(df), None) # Replace NaNs with None

edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    column_order=[        
        "id",
        "name",
        "description",
        "model",
        "price",
        "quantity",
        "supplier_id",
        "image_url",
        "categories",
        "sales",
    ],
    column_config={
        "name": "Nombre",
        "id": "ID",
        "price": st.column_config.NumberColumn(
            "Precio (en Pesos)",
            help="The price of the product in USD",
            min_value=0,
            step=1,
            format="$%d",
        ),
        "image_url": st.column_config.ImageColumn(
            "Imagen", help="Streamlit app preview screenshots"
        ),
        "quantity": "Stock",
        "description": "Descripción",
        "brand": "Marca",
        "model": "Modelo",
        "categories": "Categorías",
        "supplier_id": "ID Proveedor",
        "sales": st.column_config.LineChartColumn(
            "Ventas (últimos 6 meses)",
            width="medium",
            help="The sales volume in the last 6 months",
            y_min=0,
            y_max=50,
         ),
    },
    disabled=["id"],
    hide_index=True,
    height=820,
)

if st.button('Enviar Cambios'):
    # convert the edited DataFrame to a list of dictionaries
    json_data = edited_df.to_dict(orient='records')

    # loop through each dictionary in the list
    for product in json_data:
        # Use the update_product function to send a request to the server
        result = update_product(product['id'], product['name'], product['description'], product['price'], product['image_url'], product['quantity'], product['supplier_id'], product['sales'], product['categories'], product['brand'], product['model'])
        print(result)

from streamlit_modal import Modal
import streamlit.components.v1 as components

modalAddProd = Modal("Añadir Producto",key="modalAddProd")
open_modalAddProd = st.button("Añadir Producto")
if open_modalAddProd:
    modalAddProd.open()

if modalAddProd.is_open():
    with modalAddProd.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Nombre")
            brand = st.text_input("Marca")
            image_url = st.text_input("URL Imagen")

        with col2:
            price = st.number_input("Precio", min_value=0, step=1)
            model = st.text_input("Modelo")
            sales = st.text_input("Ventas (separados por coma)")

        with col3:
            quantity = st.number_input("Stock", min_value=0, step=1)
            supplier_id = st.text_input("ID Proveedor")
            categories = st.text_input("Categorías (separadas por coma)")

        description = st.text_input("Descripción")

        if st.button('Añadir'):
            sales = [int(s) for s in sales.split(",") if s.strip()]
            categories = [c.strip() for c in categories.split(",") if c.strip()]
            result = add_product(name, description, price, image_url, quantity, supplier_id, sales, categories, brand, model)
            st.write(result)

modalDeleteProd = Modal("Borrar Producto",key="modalDeleteProd")
open_modalDeleteProd = st.button("Borrar Producto")
if open_modalDeleteProd:
    modalDeleteProd.open()

if modalDeleteProd.is_open():
    with modalDeleteProd.container():
        col1, col2 = st.columns(2)
        with col1:
            product_id = st.text_input("ID Producto a borrar")

        if st.button('Borrar Product'):
            result = remove_product(product_id)
            st.write(result)

modalUpdateProd = Modal("Actualizar Producto",key="modalUpdateProd")
open_modalUpdateProd = st.button("Actualizar Producto")
if open_modalUpdateProd:
    modalUpdateProd.open()

if modalUpdateProd.is_open():
    with modalUpdateProd.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            product_id_to_update = st.text_input("ID Producto a actualizar")
            name_to_update = st.text_input("Nuevo Nombre")

        with col2: 
            quantity_to_update = st.number_input("Nuevo Stock", min_value=0, step=1)
            brand_to_update = st.text_input("Nuevo Cantidad")
                
        with col3:
            price_to_update = st.number_input("Nuevo Precio", min_value=0, step=1)
            model_to_update = st.text_input("Nuevo Modelo")


        col1, col2 = st.columns([2, 1])

        with col1:
            image_url_to_update = st.text_input("Nuevo URL Imagen")
                
        with col2:
            supplier_id_to_update = st.text_input("Nuevo ID Proveedor")

        col1, col2 = st.columns(2)
        with col1:
           sales_to_update = st.text_input("Nuevas Ventas (separadas por coma)")
        with col2:
            categories_to_update = st.text_input("Nuevas Categorías (separadas por coma)")
        description_to_update = st.text_input("Nueva descripción")

        if st.button('Update Product'):
            sales_to_update = [int(s) for s in sales_to_update.split(",") if s.strip()]
            categories_to_update = [c.strip() for c in categories_to_update.split(",") if c.strip()]
            result = update_product(product_id_to_update, name_to_update, description_to_update, price_to_update, image_url_to_update, quantity_to_update, supplier_id_to_update, sales_to_update, categories_to_update, brand_to_update, model_to_update)
            st.write(result)

st.subheader('Export Report')
export_format_selector()