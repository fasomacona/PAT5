"""
App Streamlit — Proyecto integrador Tema 5 (GAB-2402)
Prof. Fabián Soberanes Martín

Ejecutar desde la raíz del tema:
    streamlit run app/app.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent.parent
DATA_PATH = BASE / "data" / "empleados_ventas.csv"
MODEL_PATH = BASE / "models" / "modelo_salario.joblib"
SCALER_PATH = BASE / "models" / "scaler.joblib"

st.set_page_config(
    page_title="Analítica de Empleados · GAB-2402",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Limpieza mínima para que la demo funcione aunque el notebook no se haya corrido
    df = df.drop_duplicates()
    if "edad" in df.columns:
        df["edad"] = df["edad"].fillna(df["edad"].median())
    if "salario" in df.columns and "departamento" in df.columns:
        df["salario"] = df.groupby("departamento")["salario"].transform(
            lambda s: s.fillna(s.median())
        )
        df["salario"] = df["salario"].fillna(df["salario"].median())
        # Tope suave a outliers extremos
        q99 = df["salario"].quantile(0.99)
        df.loc[df["salario"] > q99 * 1.5, "salario"] = q99
    return df


def try_load_model():
    try:
        import joblib

        if MODEL_PATH.exists():
            model = joblib.load(MODEL_PATH)
            scaler = joblib.load(SCALER_PATH) if SCALER_PATH.exists() else None
            return model, scaler
    except Exception:
        pass
    return None, None


df = load_data(DATA_PATH)

st.title("📊 Dashboard de analítica de empleados")
st.caption("Proyecto integrador · Temas 1–5 · Prof. Fabián Soberanes Martín")

# ---------------------------------------------------------------------------
# Filtros
# ---------------------------------------------------------------------------
st.sidebar.header("Filtros")
deptos = sorted(df["departamento"].dropna().unique())
ciudades = sorted(df["ciudad"].dropna().unique())

sel_dept = st.sidebar.multiselect("Departamento", deptos, default=deptos)
sel_ciudad = st.sidebar.multiselect("Ciudad", ciudades, default=ciudades)

mask = df["departamento"].isin(sel_dept) & df["ciudad"].isin(sel_ciudad)
dff = df.loc[mask].copy()

# ---------------------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Empleados", f"{len(dff):,}")
c2.metric("Salario promedio", f"${dff['salario'].mean():,.0f}" if len(dff) else "—")
c3.metric("Salario mediano", f"${dff['salario'].median():,.0f}" if len(dff) else "—")
c4.metric("Experiencia prom.", f"{dff['experiencia_anios'].mean():.1f} años" if len(dff) else "—")

tab1, tab2, tab3 = st.tabs(["Exploración", "Comparativos", "Predicción"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        fig1 = px.histogram(dff, x="salario", nbins=30, title="Distribución de salarios")
        st.plotly_chart(fig1, use_container_width=True)
    with col_b:
        fig2 = px.box(dff, x="departamento", y="salario", title="Salario por departamento")
        st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(dff.head(50), use_container_width=True)

with tab2:
    agg = (
        dff.groupby(["ciudad", "departamento"], as_index=False)["salario"]
        .mean()
        .rename(columns={"salario": "salario_promedio"})
    )
    fig3 = px.bar(
        agg,
        x="ciudad",
        y="salario_promedio",
        color="departamento",
        barmode="group",
        title="Salario promedio por ciudad y departamento",
    )
    st.plotly_chart(fig3, use_container_width=True)

    if {"experiencia_anios", "salario"}.issubset(dff.columns):
        fig4 = px.scatter(
            dff,
            x="experiencia_anios",
            y="salario",
            color="departamento",
            trendline="ols",
            title="Salario vs experiencia",
        )
        st.plotly_chart(fig4, use_container_width=True)

with tab3:
    st.subheader("Estimación de salario")
    st.write(
        "Completa las variables. Si ya entrenaste y guardaste el modelo en el notebook, "
        "se usará automáticamente; si no, se muestra una estimación lineal simple de respaldo."
    )

    e1, e2, e3 = st.columns(3)
    with e1:
        edad = st.number_input("Edad", 22, 65, 35)
        educacion = st.selectbox("Educación (1–4)", [1, 2, 3, 4], index=1)
    with e2:
        experiencia = st.number_input("Experiencia (años)", 0, 40, 8)
        horas = st.number_input("Horas extra / mes", 0, 40, 5)
    with e3:
        satisfaccion = st.slider("Satisfacción", 1, 5, 3)
        antiguedad = st.number_input("Antigüedad empresa", 0, 40, 5)

    x = np.array([[edad, experiencia, educacion, horas, satisfaccion, antiguedad]], dtype=float)
    model, scaler = try_load_model()

    if st.button("Predecir salario"):
        if model is not None:
            x_in = scaler.transform(x) if scaler is not None else x
            pred = float(model.predict(x_in)[0])
            st.success(f"Salario estimado (modelo entrenado): **${pred:,.2f}**")
        else:
            # Fallback didáctico (no sustituye al modelo del notebook)
            pred = 9000 + 280 * edad + 700 * experiencia + 2000 * educacion + 100 * horas + 300 * satisfaccion
            st.warning(
                f"Estimación de respaldo (sin archivo de modelo): **${pred:,.2f}**. "
                "Ejecuta el notebook y guarda `models/modelo_salario.joblib`."
            )

st.markdown("---")
st.caption("GAB-2402 · Programación Avanzada · Material del Prof. Fabián Soberanes Martín")
