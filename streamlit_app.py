# -*- coding: utf-8 -*-
"""App Streamlit: texto libre -> prediccion ODS."""
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Clasificador ODS", layout="centered")

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

    try:
        _ensure_nltk()
    except Exception as exc:
        # No tumbar la app si NLTK falla al descargar; se reintenta al predecir
        st.warning(f"Aviso NLTK: {exc}")
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No se encontro el modelo en {MODEL_PATH}. "
            f"Archivos en models/: {list((BASE_DIR / 'models').glob('*'))}"
        )
    return joblib.load(MODEL_PATH)


st.title("Clasificador de textos ODS")
st.write(
    "Pegue un texto en espanol y el modelo predice el Objetivo de Desarrollo "
    "Sostenible (ODS) mas relacionado. Pipeline del Microproyecto 2: "
    "TF-IDF + LSA + LinearSVC."
)

texto = st.text_area(
    "Texto a clasificar",
    height=180,
    placeholder="Ejemplo: Programas de educacion primaria y formacion docente...",
)

col1, col2 = st.columns([1, 3])
with col1:
    predecir = st.button("Predecir ODS")

if predecir:
    if not texto or not str(texto).strip():
        st.warning("Escriba o pegue un texto para predecir.")
    else:
        try:
            model = load_model()
            pred = int(model.predict([texto])[0])
            nombre = ODS_NOMBRE.get(pred, "ODS")
            st.success(f"Prediccion: ODS {pred} - {nombre}")
        except Exception as exc:
            st.exception(exc)
