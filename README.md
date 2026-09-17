# Clasificador ODS - Microproyecto 2 (MLNS)

App Streamlit para predecir el ODS de un texto en español.
Modelo: pipeline TF-IDF + TruncatedSVD + LinearSVC (Walter Henao / Duvan Duque).

## URLs

- Repo: https://github.com/Walhenao/mlns-mp2-ods-henao-duque
- App Streamlit: desplegar en https://share.streamlit.io (cuenta Community, repo público, main file `streamlit_app.py`, Python 3.10)

## Correr en local

```bash
cd deploy_ods
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy en Streamlit Cloud

1. Entrar a https://share.streamlit.io e iniciar sesión con GitHub
2. New app / Deploy from GitHub
3. Repo: `Walhenao/mlns-mp2-ods-henao-duque`
4. Branch: `main`
5. Main file: `streamlit_app.py`
6. Advanced: Python 3.10
7. Copiar la URL pública de la app al notebook (sección 7)
