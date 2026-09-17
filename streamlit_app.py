# -*- coding: utf-8 -*-
"""App Streamlit: texto libre -> prediccion ODS (mismo pipeline del MP2)."""
from pathlib import Path

import joblib
import streamlit as st

st.set_page_config(
    page_title="Clasificador ODS",
    layout="centered",
)

ODS_NOMBRE = {
    1: "Fin de la pobreza",
    2: "Hambre cero",
    3: "Salud y bienestar",
    4: "Educacion de calidad",
    5: "Igualdad de genero",
    6: "Agua limpia",
    7: "Energia asequible",
    8: "Trabajo decente",
    9: "Industria e innovacion",
    10: "Reduccion de desigualdades",
    11: "Ciudades sostenibles",
    12: "Produccion y consumo",
    13: "Accion por el clima",
    14: "Vida submarina",
    15: "Vida de ecosistemas",
    16: "Paz y justicia",
    17: "Alianzas",
}

MODEL_PATH = Path(__file__).resolve().parent / "models" / "modelo_ods.joblib"


@st.cache_resource
def load_model():
    # NLTK se prepara al cargar el modelo (no al importar el script)
    from text_preprocess import _ensure_nltk

    _ensure_nltk()
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"No se encontro el modelo: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


st.title("Clasificador de textos ODS")
st.write(
    "Pegue un texto en espanol y el modelo predice el Objetivo de Desarrollo "
    "Sostenible (ODS) mas relacionado. Usamos el mismo pipeline del "
    "Microproyecto 2 (TF-IDF + LSA + LinearSVC)."
)

texto = st.text_area(
    "Texto a clasificar",
    height=180,
    placeholder="Ejemplo: Programas de educacion primaria y formacion docente...",
)

if st.button("Predecir ODS"):
    if not texto or not str(texto).strip():
        st.warning("Escriba o pegue un texto para predecir.")
    else:
        try:
            model = load_model()
            pred = int(model.predict([texto])[0])
            nombre = ODS_NOMBRE.get(pred, "ODS")
            st.success(f"Prediccion: ODS {pred} - {nombre}")
        except Exception as exc:
            st.error(f"Error al predecir: {exc}")
