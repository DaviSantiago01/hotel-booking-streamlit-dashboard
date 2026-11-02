"""Estrutura inicial dos dashboards de Hotel Booking Demand."""

from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Hotel Booking | Dashboards",
    page_icon="🏨",
    layout="wide",
)

CAMINHO_DADOS = Path(__file__).resolve().parent / "data" / "hotel_bookings.csv"


@st.cache_data
def carregar_dados():
    """Lê a base de reservas que acompanha o projeto."""
    return pd.read_csv(CAMINHO_DADOS)


df = carregar_dados()

st.title("Hotel Booking Demand")
st.caption("Análise de reservas e cancelamentos de hotéis")

with st.expander("Conferir os dados carregados"):
    st.write(f"{len(df):,} reservas e {len(df.columns)} colunas.".replace(",", "."))
    st.dataframe(df.head(), hide_index=True)

laboratorio, gestao = st.tabs(["Laboratório de análise", "Visão gerencial"])

with laboratorio:
    st.header("Distribuição e correlação")
    st.info("Em construção: seleção de variáveis, filtro de intervalo, histogramas e mapa de correlação.")

with gestao:
    st.header("Indicadores de reservas")
    st.info("Em construção: indicadores e visuais para gestores de reservas e planejamento hoteleiro.")
