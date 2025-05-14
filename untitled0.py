import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titel des Dashboards
st.title("Discounted Cash Flow Dashboard")

# Hochladen einer Excel-Datei (z. B. NPV.xlsx)
uploaded_file = st.file_uploader("Lade deine Excel-Datei hoch (z. B. NPV.xlsx)", type=["xlsx"])

if uploaded_file:
    # Excel-Datei einlesen
    NPV = pd.read_excel(uploaded_file)

    # Zeige die rohen Daten
    st.subheader("Vorschau der geladenen Daten")
    st.dataframe(NPV)

    # Extrahiere die relevanten Werte
    try:
        x_labels = NPV.iloc[3:15, 0]  # z. B. Jahr oder Periode
        startup_cashflows = NPV.iloc[3:15, 1]  # z. B. Spalte B
        cashcow_cashflows = NPV.iloc[3:15, 2]  # z. B. Spalte C
    except Exception as e:
        st.error(f"Fehler beim Extrahieren der Daten: {e}")
    else:
        # Zinssatz über Slider einstellen
        rate = st.slider("Zinssatz (Interest Rate)", 0.01, 0.3, 0.1, step=0.01)

        # Funktion zum Diskontieren
        def discount(cashflows, rate):
            return [cf / ((1 + rate) ** i) for i, cf in enumerate(cashflows)]

        startup_discounted = discount(startup_cashflows, rate)
        cashcow_discounted = discount(cashcow_cashflows, rate)

        # Plot erzeugen
        fig, ax = plt.subplots(figsize=(10, 5))
        x = range(len(x_labels))
        bar_width = 0.35

        ax.bar(x, startup_discounted, width=bar_width, label='Startup', color='skyblue')
        ax.bar([i + bar_width for i in x], cashcow_discounted, width=bar_width, label='Cashcow', color='navy')

        ax.set_xticks([i + bar_width / 2 for i in x])
        ax.set_xticklabels(x_labels, rotation=45)
        ax.set_ylabel("Diskontierter Wert")
        ax.set_title("Discounted Cash Flow")
        ax.legend()

        st.pyplot(fig)
