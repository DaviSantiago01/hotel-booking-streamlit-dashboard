"""Estrutura inicial dos dashboards de Hotel Booking Demand."""

from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Hotel Booking | Dashboards",
    page_icon="🏨",
    layout="wide",
)

CAMINHO_DADOS = Path(__file__).resolve().parent / "data" / "hotel_bookings_tratado.csv"


@st.cache_data
def carregar_dados():
    """Lê a base tratada exportada pelo notebook da EDA."""
    return pd.read_csv(CAMINHO_DADOS, low_memory=False)


df = carregar_dados()

st.title("Hotel Booking Demand")
st.caption("Análise de reservas e cancelamentos de hotéis")

visao_geral, analise_detalhada = st.tabs(["Visão geral", "Análise detalhada"])

with visao_geral:
    st.header("Reservas e cancelamentos")
    st.caption("Indicadores de todas as reservas da base histórica.")

    total_reservas = len(df)
    taxa_cancelamento = (df["booking_status"] == "Canceled").mean() * 100
    antecedencia_mediana = df["lead_time"].median()
    diaria_media = df.loc[df["booking_status"] == "Not Canceled", "adr"].mean()

    coluna_total, coluna_cancelamento, coluna_antecedencia, coluna_diaria = st.columns(4)

    coluna_total.metric(
        "Total de reservas",
        f"{total_reservas:,}".replace(",", "."),
        help="Quantidade de reservas registradas na base, incluindo as canceladas.",
    )
    coluna_cancelamento.metric(
        "Taxa de cancelamento",
        f"{taxa_cancelamento:.1f}%".replace(".", ","),
        help="Reservas canceladas divididas pelo total de reservas, em porcentagem.",
    )
    coluna_antecedencia.metric(
        "Antecedência mediana",
        f"{antecedencia_mediana:.0f} dias",
        help="Valor central dos dias entre a realização da reserva e a chegada. Metade das reservas tem antecedência até esse valor.",
    )
    coluna_diaria.metric(
        "Diária média",
        f"{diaria_media:.2f}".replace(".", ","),
        help="Média do ADR (valor médio diário) apenas das reservas não canceladas. Cada reserva tem o mesmo peso; não é receita total.",
    )
    st.caption("Diária média: apenas reservas não canceladas.")

with analise_detalhada:
    st.header("Distribuição e correlação")
    st.info("Em construção: escolha das informações, filtro de valores e gráficos para investigar as reservas.")
