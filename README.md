# Tema 5 – Aplicaciones de Analítica de Datos y Proyecto Práctico

**Asignatura:** Programación Avanzada (GAB-2402)  
**Institución:** Tecnológico de Estudios Superiores de Chalco  
**Material creado por el Prof. Fabián Soberanes Martín**

---

## Descripción

Tema de cierre e **integración** de toda la asignatura:

| Tema | Qué se reutiliza en la práctica |
|------|----------------------------------|
| 1 | Limpieza, Pandas, features |
| 2 | Visualizaciones Seaborn/Plotly en notebook y app |
| 3 | t-test, regresión, clasificación, métricas, joblib |
| 4 | Exportación a SQLite y consultas |
| 5 | App Streamlit + presentación del proyecto |

---

## Estructura

```
tema5-aplicaciones-analitica/
├── index.html
├── 01-apps-analitica.html
├── 02-integracion-viz.html
├── 03-proyecto-practico.html
├── practica.html
├── css/styles.css
├── data/empleados_ventas.csv
├── notebooks/practica_tema5_integradora.ipynb
├── app/app.py
├── models/                 # se crea al entrenar en el notebook
├── requirements.txt
└── README.md
```

---

## Cómo ejecutar

```bash
cd tema5-aplicaciones-analitica
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Análisis
jupyter lab   # notebooks/practica_tema5_integradora.ipynb

# Aplicación
streamlit run app/app.py
```

Sitio teórico local:

```bash
python -m http.server 8000
```

---

## Entregables del proyecto integrador

1. Notebook completo (limpieza → modelo → SQLite).
2. Modelo guardado en `models/`.
3. App Streamlit con filtros, KPIs, gráficos y predicción.
4. README del proyecto con problema, método, resultados y limitaciones.

---

**Prof. Fabián Soberanes Martín** · Listo para GitHub Pages.
