# -*- coding: utf-8 -*-
"""App Streamlit: texto libre -> prediccion ODS."""
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Clasificador ODS", layout="centered")

st.title("Clasificador de textos ODS")
st.caption("Microproyecto 2 MLNS - Walter Henao / Duvan Duque")

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

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "modelo_ods.joblib"


@st.cache_resource
def load_model():
    import joblib
    from text_preprocess import _ensure_nltk

    _ensure_nltk()
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"No se encontro: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


texto = st.text_area(
    "Texto a clasificar",
    height=180,
    placeholder="Ejemplo: Programas de educacion primaria y formacion docente...",
)

if st.button("Predecir ODS"):
    if not str(texto).strip():
        st.warning("Escriba o pegue un texto para predecir.")
    else:
        try:
            model = load_model()
            pred = int(model.predict([texto])[0])
            st.success(f"Prediccion: ODS {pred} - {ODS_NOMBRE.get(pred, 'ODS')}")
        except Exception as exc:
            st.error("No se pudo predecir. Detalle tecnico:")
            st.exception(exc)
