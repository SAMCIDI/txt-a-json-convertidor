import streamlit as st
import os
import zipfile
import json
from io import StringIO, BytesIO

st.set_page_config(page_title="Convertidor TXT a JSON", layout="centered")
st.title("📄 Convertidor de TXT a JSON")

uploaded_files = st.file_uploader(
    "Selecciona uno o varios archivos .txt o un .zip que los contenga:",
    type=["txt", "zip"],
    accept_multiple_files=True
)

def convertir_txt_a_json(nombre_archivo, contenido):
    lineas = contenido.splitlines()
    json_data = {"contenido": lineas}
    return nombre_archivo.replace(".txt", ".json"), json.dumps(json_data, indent=4)

def procesar_archivos(files):
    archivos_convertidos = []

    for file in files:
        if file.name.endswith(".zip"):
            with zipfile.ZipFile(file, 'r') as zip_ref:
                for zip_info in zip_ref.infolist():
                    if zip_info.filename.endswith(".txt"):
                        with zip_ref.open(zip_info) as f:
                            contenido = f.read().decode("utf-8")
                            nombre_json, contenido_json = convertir_txt_a_json(zip_info.filename, contenido)
                            archivos_convertidos.append((nombre_json, contenido_json))
        elif file.name.endswith(".txt"):
            stringio = StringIO(file.getvalue().decode("utf-8"))
            nombre_json, contenido_json = convertir_txt_a_json(file.name, stringio.read())
            archivos_convertidos.append((nombre_json, contenido_json))

    return archivos_convertidos

if uploaded_files:
    st.success(f"Se cargaron {len(uploaded_files)} archivo(s).")
    archivos = procesar_archivos(uploaded_files)

    if archivos:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_out:
            for nombre_json, contenido_json in archivos:
                zip_out.writestr(nombre_json, contenido_json)

        st.download_button(
            label="📦 Descargar ZIP con archivos JSON",
            data=zip_buffer.getvalue(),
            file_name="archivos_convertidos.zip",
            mime="application/zip"
        )
    else:
        st.warning("No se encontraron archivos .txt válidos en lo subido.")
