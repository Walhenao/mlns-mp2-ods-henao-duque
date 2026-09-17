# -*- coding: utf-8 -*-
"""Entrena LinearSVC (misma receta del notebook) y guarda pipe_clf con joblib."""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from text_preprocess import text_preprocess

ROOT = Path(__file__).resolve().parent
MP2 = ROOT.parent
DATA = MP2 / "Datos_textosODS.xlsx"
OUT = ROOT / "models" / "modelo_ods.joblib"


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(DATA)
    X = df["textos"].astype(str)
    y = df["ODS"].astype(int)

    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.2, random_state=0, stratify=y
    )
    train_df = pd.DataFrame({"textos": X_train.astype(str), "ODS": y_train.astype(int)})
    train_df = train_df.dropna().drop_duplicates(subset=["textos"]).reset_index(drop=True)
    X_train = train_df["textos"]
    y_train = train_df["ODS"]

    pipe_clf = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    preprocessor=text_preprocess,
                    min_df=2,
                    max_df=0.9,
                    ngram_range=(1, 1),
                ),
            ),
            ("svd", TruncatedSVD(n_components=100, random_state=0)),
            ("clf", LinearSVC(C=2.0, random_state=0, dual="auto", max_iter=3000)),
        ]
    )
    print(f"Fitting on {len(X_train)} texts...", flush=True)
    pipe_clf.fit(X_train, y_train)
    joblib.dump(pipe_clf, OUT)
    print(f"Saved: {OUT} ({OUT.stat().st_size / 1024:.1f} KB)", flush=True)
    # smoke
    pred = pipe_clf.predict(["La educacion de calidad mejora el aprendizaje en las escuelas."])[0]
    print("Smoke pred ODS:", int(pred), flush=True)


if __name__ == "__main__":
    main()
