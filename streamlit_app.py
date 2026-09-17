# -*- coding: utf-8 -*-
"""App Streamlit E3: atlas ODS + prediccion con score relativo."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import streamlit as st

from ods_meta import ODS_BLURB, ODS_COLOR, ODS_NOMBRE, icon_svg

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "modelo_ods.joblib"
LOGO_PATH = BASE_DIR / "assets" / "logo_uniandes.png"

EXAMPLES = {
    "Educacion": "Programas de educacion primaria y formacion docente en zonas rurales",
    "Salud": "Acceso a hospitales, vacunacion y atencion en salud mental",
    "Genero": "Igualdad de genero, empoderamiento de mujeres y prevencion de violencia",
    "Clima": "Mitigacion del cambio climatico y reduccion de emisiones de gases",
    "Justicia": "Justicia, transparencia institucional y lucha contra la corrupcion",
}

st.set_page_config(
    page_title="Clasificador ODS",
    page_icon="assets/logo_uniandes.png" if LOGO_PATH.exists() else None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,600&family=Source+Sans+3:wght@400;500;600&display=swap');
  /* Forzar aspecto claro (entrega academica Uniandes) */
  html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #ffffff !important;
    color: #161616 !important;
  }
  [data-testid="stHeader"] { background: #ffffff !important; }
  html, body, [class*="css"]  {
    font-family: "Source Sans 3", "Segoe UI", sans-serif;
  }
  h1, h2, h3, .serif {
    font-family: "Source Serif 4", Georgia, serif !important;
    font-weight: 600 !important;
    color: #161616 !important;
  }
  .block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1180px; }
  #MainMenu, footer, header { visibility: hidden; }
  .stTextArea textarea {
    background-color: #fafaf8 !important;
    color: #333 !important;
  }
  .color-strip { display: flex; height: 5px; margin: 0 0 1rem 0; }
  .color-strip span { flex: 1; }
  .brand-row { display: flex; align-items: center; gap: 0.85rem; margin-bottom: 0.35rem; }
  .brand-row img { height: 46px; width: auto; }
  .brand-meta { line-height: 1.25; }
  .brand-uni { color: #001a70; font-size: 0.9rem; font-weight: 600; }
  .brand-authors { color: #666; font-size: 0.8rem; }
  .atlas-box {
    background: #f3f2ee; border: 1px solid #e2dfd8;
    padding: 0.9rem 0.75rem 0.85rem; height: 100%;
  }
  .atlas-label {
    font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase;
    color: #777; margin: 0 0 0.2rem;
  }
  .atlas-title {
    font-family: "Source Serif 4", Georgia, serif; font-size: 1.05rem;
    margin: 0 0 0.7rem; color: #161616;
  }
  .atlas-grid {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px;
  }
  .atlas-grid img, .atlas-grid svg { width: 100%; height: auto; display: block; }
  .atlas-item { line-height: 0; opacity: 0.9; transition: opacity .2s; }
  .atlas-item.dim { opacity: 0.28; }
  .atlas-item.active {
    opacity: 1; outline: 2px solid var(--accent, #001a70); outline-offset: 2px;
  }
  .atlas-note { margin: 0.75rem 0 0; font-size: 0.72rem; color: #888; line-height: 1.35; }
  .empty-box {
    border: 1px solid #e2dfd8; background: #faf9f6; padding: 1.35rem 1rem;
    text-align: center; color: #888; font-size: 0.9rem;
  }
  .ficha {
    border: 1px solid var(--accent, #e2dfd8); border-left: 4px solid var(--accent, #001a70);
    background: #fff; padding: 1rem 1.05rem;
  }
  .ficha-row { display: flex; gap: 0.95rem; align-items: flex-start; }
  .ficha h3 { margin: 0 0 0.15rem; font-size: 1.25rem; }
  .ficha .name { margin: 0 0 0.35rem; font-size: 0.98rem; color: #222; }
  .ficha .blurb { margin: 0 0 0.7rem; font-size: 0.84rem; color: #666; line-height: 1.35; }
  .conf-row { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem; }
  .conf-label { font-size: 0.75rem; color: #666; min-width: 5.2rem; }
  .conf-track { flex: 1; height: 8px; background: #eceae4; overflow: hidden; }
  .conf-track i { display: block; height: 100%; background: var(--accent, #001a70); }
  .conf-pct { font-size: 0.82rem; font-weight: 600; min-width: 2.6rem; text-align: right; }
  .score-note { margin: 0; font-size: 0.72rem; color: #999; }
  .top3 { margin-top: 0.85rem; padding-top: 0.7rem; border-top: 1px solid #eceae4; }
  .top3-title {
    margin: 0 0 0.45rem; font-size: 0.68rem; letter-spacing: 0.06em;
    text-transform: uppercase; color: #888; font-weight: 500;
  }
  .top-item { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem; }
  .top-meta {
    flex: 1; display: grid; grid-template-columns: 3.2rem 1fr 2.3rem;
    gap: 0.35rem; align-items: center; font-size: 0.78rem; color: #555;
  }
  .top-bar { height: 4px; background: #eceae4; overflow: hidden; }
  .top-bar i { display: block; height: 100%; }
  .foot { margin-top: 0.85rem; font-size: 0.72rem; color: #9a9a9a; }
  div[data-testid="stHorizontalBlock"] button {
    border: 1px solid #ccc7bc !important;
    background: #faf9f6 !important;
    color: #333 !important;
  }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model():
    import joblib
    from text_preprocess import _ensure_nltk

    _ensure_nltk()
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"No se encontro: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


def relative_scores(model, texto: str):
    """Softmax sobre decision_function (score relativo, no probabilidad calibrada)."""
    scores = np.asarray(model.decision_function([texto])[0], dtype=float)
    classes = np.asarray(model.classes_)
    shifted = scores - scores.max()
    exp = np.exp(shifted)
    probs = exp / exp.sum()
    order = np.argsort(probs)[::-1]
    ranked = [(int(classes[i]), float(probs[i])) for i in order]
    return ranked


def atlas_html(active: int | None = None) -> str:
    cells = []
    for n in range(1, 17):
        cls = "atlas-item"
        if active is not None:
            cls += " active" if n == active else " dim"
        cells.append(f'<div class="{cls}">{icon_svg(n, 56)}</div>')
    accent = ODS_COLOR.get(active or 1, "#001a70")
    return f"""
    <div class="atlas-box" style="--accent:{accent}">
      <p class="atlas-label">Agenda 2030</p>
      <p class="atlas-title">Atlas de objetivos</p>
      <div class="atlas-grid">{''.join(cells)}</div>
      <p class="atlas-note">
        Corpus del microproyecto: ODS 1–16 (sin el 17 Alianzas).
        Al predecir, se resalta solo el objetivo elegido.
      </p>
    </div>
    """


def ficha_html(pred: int, conf: float, top3: list[tuple[int, float]]) -> str:
    accent = ODS_COLOR.get(pred, "#001a70")
    pct = int(round(conf * 100))
    tops = []
    for ods, score in top3:
        sp = int(round(score * 100))
        tops.append(
            f"""<div class="top-item">
              {icon_svg(ods, 34)}
              <div class="top-meta">
                <span>ODS {ods}</span>
                <span class="top-bar"><i style="width:{sp}%;background:{ODS_COLOR.get(ods, '#888')}"></i></span>
                <span style="text-align:right">{sp}%</span>
              </div>
            </div>"""
        )
    return f"""
    <div class="ficha" style="--accent:{accent}">
      <div class="ficha-row">
        {icon_svg(pred, 92)}
        <div>
          <h3>ODS {pred}</h3>
          <p class="name">{ODS_NOMBRE.get(pred, '')}</p>
          <p class="blurb">{ODS_BLURB.get(pred, '')}</p>
          <div class="conf-row">
            <span class="conf-label">Score relativo</span>
            <span class="conf-track"><i style="width:{pct}%"></i></span>
            <span class="conf-pct">{pct}%</span>
          </div>
          <p class="score-note">Derivado de decision_function (no es probabilidad calibrada).</p>
        </div>
      </div>
      <div class="top3">
        <p class="top3-title">Top 3</p>
        {''.join(tops)}
      </div>
    </div>
    """


# --- Cabecera ---
strip = "".join(
    f'<span style="background:{ODS_COLOR[n]}"></span>' for n in range(1, 17)
)
st.markdown(f'<div class="color-strip">{strip}</div>', unsafe_allow_html=True)

if LOGO_PATH.exists():
    import base64

    b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    logo_img = f'<img src="data:image/png;base64,{b64}" alt="Escudo Uniandes" />'
else:
    logo_img = ""

st.markdown(
    f"""
    <div class="brand-row">
      {logo_img}
      <div class="brand-meta">
        <div class="brand-uni">Universidad de los Andes</div>
        <div class="brand-authors">Walter Henao / Duvan Duque · Grupo 39 · MLNS</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("## Clasificador de textos ODS")
st.caption("Escribe un texto libre en espanol o elige un ejemplo rapido.")

if "pred_result" not in st.session_state:
    st.session_state.pred_result = None
if "texto" not in st.session_state:
    st.session_state.texto = ""


def _clear_form() -> None:
    st.session_state.texto = ""
    st.session_state.pred_result = None


def _set_example(sample: str) -> None:
    st.session_state.texto = sample
    st.session_state.pred_result = None


# Chips (on_click corre antes de recrear el text_area)
chip_cols = st.columns(len(EXAMPLES))
for col, (label, sample) in zip(chip_cols, EXAMPLES.items()):
    col.button(
        label,
        key=f"chip_{label}",
        use_container_width=True,
        on_click=_set_example,
        args=(sample,),
    )

left, right = st.columns([0.92, 1.55], gap="large")

with right:
    st.text_area(
        "Texto a clasificar",
        height=140,
        placeholder="Ejemplo: Programas de educacion primaria y formacion docente...",
        key="texto",
    )
    b1, b2 = st.columns([1, 1])
    predict = b1.button("Predecir ODS", type="primary", use_container_width=True)
    b2.button(
        "Limpiar",
        use_container_width=True,
        on_click=_clear_form,
    )

    if predict:
        txt = str(st.session_state.get("texto", "")).strip()
        if not txt:
            st.warning("Escriba o pegue un texto para predecir.")
        else:
            try:
                model = load_model()
                ranked = relative_scores(model, txt)
                pred, conf = ranked[0]
                st.session_state.pred_result = {
                    "pred": pred,
                    "conf": conf,
                    "top3": ranked[:3],
                }
            except Exception as exc:
                st.error("No se pudo predecir. Detalle tecnico:")
                st.exception(exc)

    result = st.session_state.pred_result
    if result is None:
        st.markdown(
            '<div class="empty-box">El objetivo predicho aparecera aqui<br/>'
            "con logo, score relativo y top 3.</div>",
            unsafe_allow_html=True,
        )
        active = None
    else:
        st.markdown(
            ficha_html(result["pred"], result["conf"], result["top3"]),
            unsafe_allow_html=True,
        )
        active = result["pred"]

    st.markdown(
        '<p class="foot">Pipeline exportado con joblib · TF-IDF + LSA + LinearSVC · Python 3.10</p>',
        unsafe_allow_html=True,
    )

with left:
    st.markdown(atlas_html(active), unsafe_allow_html=True)
