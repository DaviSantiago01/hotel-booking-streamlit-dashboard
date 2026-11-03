"""Painéis de reservas e cancelamentos de hotéis."""

# [IA] Codex — apoio na estrutura da aplicação.
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Hotel Booking", page_icon="🏨", layout="wide")

CAMINHO_DADOS = Path(__file__).resolve().parent / "data" / "hotel_bookings_tratado.csv"

VARIAVEIS = {
    "lead_time": "Antecedência (dias)",
    "stays_in_weekend_nights": "Noites no fim de semana",
    "stays_in_week_nights": "Noites na semana",
    "adr": "Diária média",
    "total_of_special_requests": "Pedidos especiais",
}

HOTEIS = {"Todos": "Todos os hotéis", "City Hotel": "Hotel urbano", "Resort Hotel": "Resort"}


# [IA] Codex — apoio na formatação dos valores.
def numero_br(valor, casas=0):
    return f"{valor:,.{casas}f}".replace(",", "_").replace(".", ",").replace("_", ".")


# [IA] Codex — apoio no carregamento dos dados.
@st.cache_data(show_spinner="Carregando reservas…")
def carregar_dados(caminho, modificacao):
    """Valida o CSV; a data de modificação renova o cache quando o arquivo muda."""
    dados = pd.read_csv(caminho, low_memory=False)
    obrigatorias = set(VARIAVEIS) | {"hotel", "booking_status"}
    if not obrigatorias.issubset(dados.columns):
        raise ValueError("A base não contém todas as colunas necessárias. Exporte novamente a versão tratada pelo notebook.")
    if dados.empty or dados[list(obrigatorias)].isna().any().any():
        raise ValueError("A base está vazia ou tem ausências nas informações usadas pelo painel.")
    if not dados["booking_status"].isin(["Canceled", "Not Canceled"]).all():
        raise ValueError("O status das reservas é inválido. Use a base tratada exportada pelo notebook.")
    if not dados["hotel"].isin(["City Hotel", "Resort Hotel"]).all():
        raise ValueError("A base contém tipos de hotel não reconhecidos.")
    for coluna in VARIAVEIS:
        if not pd.api.types.is_numeric_dtype(dados[coluna]) or not np.isfinite(dados[coluna]).all():
            raise ValueError("A base contém valores numéricos inválidos. Confira a exportação no notebook.")
    for coluna in set(VARIAVEIS) - {"adr"}:
        if (dados[coluna] < 0).any() or (dados[coluna] % 1 != 0).any():
            raise ValueError("Antecedência, noites e pedidos precisam ser números inteiros não negativos.")
    return dados


# [IA] Codex — apoio na limpeza dos filtros.
def limpar_filtros():
    st.session_state["hotel"] = "Todos"
    st.session_state["variavel_filtro"] = "lead_time"
    for coluna in VARIAVEIS:
        st.session_state.pop(f"intervalo_{coluna}", None)


# [IA] Codex — apoio no tratamento de erros.
try:
    df = carregar_dados(CAMINHO_DADOS, CAMINHO_DADOS.stat().st_mtime_ns)
except FileNotFoundError:
    st.error("Base tratada não encontrada. Gere data/hotel_bookings_tratado.csv pelo notebook da EDA.")
    st.stop()
except (OSError, pd.errors.ParserError):
    st.error("Não foi possível ler o CSV. Confira o arquivo exportado pelo notebook.")
    st.stop()
except ValueError as erro:
    st.error(str(erro))
    st.stop()

# [IA] Codex — apoio nos controles de filtro.
with st.sidebar:
    st.header("Filtrar reservas")
    st.caption("Os resultados das duas abas usam estes filtros.")

    hotel = st.selectbox(
        "Hotel",
        options=["Todos", "City Hotel", "Resort Hotel"],
        format_func=HOTEIS.get,
        key="hotel",
    )
    variavel_filtro = st.selectbox(
        "Filtrar por",
        options=list(VARIAVEIS),
        format_func=VARIAVEIS.get,
        key="variavel_filtro",
    )

    if variavel_filtro == "adr":
        minimo = float(df[variavel_filtro].min())
        maximo = float(df[variavel_filtro].max())
        passo = 0.01
    else:
        minimo = int(df[variavel_filtro].min())
        maximo = int(df[variavel_filtro].max())
        passo = 1

    intervalo = st.slider(
        VARIAVEIS[variavel_filtro],
        min_value=minimo,
        max_value=maximo,
        value=(minimo, maximo),
        step=passo,
        key=f"intervalo_{variavel_filtro}",
    )
    st.button("Limpar filtros", on_click=limpar_filtros)

# Um único recorte alimenta os dois painéis.
# [IA] Codex — apoio na aplicação dos filtros.
df_filtrado = df.loc[df[variavel_filtro].between(*intervalo)]
if hotel != "Todos":
    df_filtrado = df_filtrado.loc[df_filtrado["hotel"] == hotel]

# [IA] Codex — apoio na organização da interface.
st.title("Reservas e cancelamentos de hotéis")
st.write("Acompanhe os indicadores e explore o perfil das reservas.")
casas = 2 if variavel_filtro == "adr" else 0
rotulo_filtro = "Antecedência" if variavel_filtro == "lead_time" else VARIAVEIS[variavel_filtro]
unidade = " dias" if variavel_filtro == "lead_time" else ""
contagem = f"{numero_br(len(df_filtrado))} reservas"
if len(df_filtrado) != len(df):
    contagem = f"{numero_br(len(df_filtrado))} de {numero_br(len(df))} reservas"
st.caption(
    f"{HOTEIS[hotel]} · {rotulo_filtro} de "
    f"{numero_br(intervalo[0], casas)} a {numero_br(intervalo[1], casas)}{unidade} · {contagem}"
)

visao_geral, analise_detalhada = st.tabs(["Visão geral", "Análise detalhada"])

# [IA] Codex — apoio no cálculo e na apresentação dos indicadores.
with visao_geral:
    total_reservas = len(df_filtrado)
    taxa_cancelamento = (df_filtrado["booking_status"] == "Canceled").mean() * 100
    antecedencia_mediana = df_filtrado["lead_time"].median()
    diaria_media = df_filtrado.loc[
        df_filtrado["booking_status"] == "Not Canceled", "adr"
    ].mean()

    antecedencia_texto = "—"
    if pd.notna(antecedencia_mediana):
        casas_decimais = 0 if antecedencia_mediana % 1 == 0 else 1
        antecedencia_texto = f"{numero_br(antecedencia_mediana, casas_decimais)} dias"

    coluna_total, coluna_cancelamento, coluna_antecedencia, coluna_diaria = st.columns(4)

    coluna_total.metric(
        "Reservas",
        numero_br(total_reservas),
        help="Total de reservas do recorte, incluindo as canceladas.",
    )
    coluna_cancelamento.metric(
        "Cancelamentos",
        f"{numero_br(taxa_cancelamento, 1)}%" if pd.notna(taxa_cancelamento) else "—",
        help="Porcentagem de reservas canceladas dentro do recorte.",
    )
    coluna_antecedencia.metric(
        "Antecedência",
        antecedencia_texto,
        help="Mediana dos dias entre a reserva e a chegada: metade das reservas tem antecedência até esse valor.",
    )
    coluna_diaria.metric(
        "Diária média",
        numero_br(diaria_media, 2) if pd.notna(diaria_media) else "—",
        help="Média do ADR apenas das reservas não canceladas. Cada reserva tem o mesmo peso; não representa receita total.",
    )
    if df_filtrado.empty:
        st.warning("Nenhuma reserva encontrada. Amplie a faixa de valores ou escolha outro hotel.")

with analise_detalhada:
    st.header("Distribuição e correlação")
    st.caption(f"{numero_br(len(df_filtrado))} reservas selecionadas pelos filtros da lateral.")
    st.info("Em construção: histogramas e correlação das informações selecionadas.")
