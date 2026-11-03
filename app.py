"""Painéis de reservas e cancelamentos de hotéis."""

# [IA] Codex — apoio na estrutura da aplicação.
from pathlib import Path

import altair as alt
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

# [IA] Codex — apoio nos controles da análise.
with analise_detalhada:
    variaveis_selecionadas = st.multiselect(
        "O que você quer analisar?",
        options=list(VARIAVEIS),
        default=["lead_time", "stays_in_week_nights"],
        format_func=VARIAVEIS.get,
    )
    if df_filtrado.empty:
        st.warning("Nenhuma reserva encontrada. Ajuste os filtros na lateral.")
    elif not variaveis_selecionadas:
        st.info("Selecione uma informação para ver sua distribuição.")
    else:
        # [IA] Codex — apoio nos histogramas.
        st.subheader("Distribuição das reservas")
        numero_faixas = st.slider(
            "Nível de detalhe do gráfico", min_value=10, max_value=100, value=30, step=5,
            key="numero_faixas",
            disabled=not any(col in {"adr", "lead_time"} for col in variaveis_selecionadas),
            help="Controla o detalhe da antecedência e da diária. Noites e pedidos mantêm uma barra por valor inteiro.",
        )
        ampliar_graficos = st.checkbox(
            "Um gráfico por linha", value=False,
            help="Dá mais espaço a cada histograma, especialmente em telas menores.",
        )
        quantidade_colunas = 1 if ampliar_graficos or len(variaveis_selecionadas) == 1 else 2
        colunas_graficos = st.columns(quantidade_colunas)

        for indice, variavel in enumerate(variaveis_selecionadas):
            with colunas_graficos[indice % quantidade_colunas]:
                eh_contagem = variavel in {
                    "stays_in_weekend_nights",
                    "stays_in_week_nights",
                    "total_of_special_requests",
                }
                ajuda = "O eixo horizontal mostra os valores e o vertical mostra a quantidade de reservas. "
                if eh_contagem:
                    ajuda += "Cada barra corresponde a um valor inteiro. "
                else:
                    ajuda += "Cada barra reúne uma faixa de valores. O nível de detalhe controla essas faixas. "
                ajuda += (
                    "Passe o mouse para consultar as contagens. O zoom amplia a visualização, "
                    "mas não recalcula as faixas nem altera os indicadores."
                )
                st.subheader(VARIAVEIS[variavel], help=ajuda, anchor=False)
                valores = df_filtrado[variavel]
                if eh_contagem:
                    limites = np.arange(valores.min() - 0.5, valores.max() + 1.5)
                else:
                    limites = numero_faixas

                # Envia ao navegador só as contagens, sem as 119 mil linhas.
                quantidades, bordas = np.histogram(valores, bins=limites)
                distribuicao = pd.DataFrame({
                    "inicio": bordas[:-1],
                    "fim": bordas[1:],
                    "valor": (bordas[:-1] + bordas[1:]) / 2,
                    "reservas": quantidades,
                })
                distribuicao["reservas_texto"] = distribuicao["reservas"].map(numero_br)
                # O limite direito só pertence à última faixa (regra do numpy.histogram).
                faixas_texto = []
                for indice_faixa, (inicio, fim) in enumerate(zip(bordas[:-1], bordas[1:])):
                    limite_direito = "≤" if indice_faixa == len(bordas) - 2 else "<"
                    faixas_texto.append(
                        f"{numero_br(inicio, 2)} ≤ valor {limite_direito} {numero_br(fim, 2)}"
                    )
                distribuicao["faixa_texto"] = faixas_texto
                if eh_contagem:
                    dicas = [alt.Tooltip("valor:Q", title=VARIAVEIS[variavel], format=".0f")]
                else:
                    dicas = [alt.Tooltip("faixa_texto:N", title="Faixa")]
                grafico = alt.Chart(distribuicao).mark_bar(color="#56BFC4", binSpacing=0).encode(
                    x=alt.X(
                        "inicio:Q", bin="binned", title=VARIAVEIS[variavel],
                        axis=alt.Axis(
                            tickMinStep=1 if variavel != "adr" else 0.01,
                            labelExpr="replace(replace(replace(format(datum.value, ',.2~f'), ',', '_'), '.', ','), '_', '.')",
                        ),
                        scale=alt.Scale(zero=False),
                    ),
                    x2="fim:Q",
                    y=alt.Y(
                        "reservas:Q", title="Quantidade de reservas",
                        axis=alt.Axis(tickMinStep=1, labelExpr="replace(format(datum.value, ',.0f'), ',', '.')"), scale=alt.Scale(zero=True),
                    ),
                    tooltip=dicas + [alt.Tooltip("reservas_texto:N", title="Reservas")],
                ).properties(
                    height=300,
                    description=f"Histograma de {VARIAVEIS[variavel]} para {numero_br(len(df_filtrado))} reservas selecionadas.",
                ).interactive(bind_y=False)
                st.altair_chart(grafico)

                if variavel == "adr" and df_filtrado["adr"].max() > 500:
                    st.caption(
                        "Diárias muito altas alongam a escala. O filtro lateral permite observar uma faixa menor."
                    )

        # [IA] Codex — apoio na correlação e na sua apresentação.
        st.subheader(
            "Como as informações se relacionam",
            help=(
                "Correlação de Spearman: cada célula compara duas informações. "
                "Valores próximos de 1 indicam que elas tendem a crescer juntas; próximos de -1, "
                "que uma tende a diminuir quando a outra cresce. Perto de zero indica pouca relação monotônica. "
                "Isso não demonstra causa e efeito. Sem variação ou com menos de duas reservas, "
                "a correlação não pode ser calculada."
            ),
        )
        if len(variaveis_selecionadas) < 2:
            st.info("Escolha duas ou mais informações para ver a correlação.")
        elif len(df_filtrado) < 2:
            st.info("São necessárias pelo menos duas reservas para calcular a correlação.")
        else:
            correlacao = df_filtrado[variaveis_selecionadas].corr(method="spearman")
            celulas = []
            for linha in variaveis_selecionadas:
                for coluna in variaveis_selecionadas:
                    valor = correlacao.loc[linha, coluna]
                    celulas.append({
                        "linha": VARIAVEIS[linha],
                        "coluna": VARIAVEIS[coluna],
                        "correlacao": valor if pd.notna(valor) else None,
                        "rotulo": numero_br(valor, 2) if pd.notna(valor) else "N/D",
                    })

            ordem = [VARIAVEIS[col] for col in variaveis_selecionadas]
            base_mapa = alt.Chart(pd.DataFrame(celulas)).encode(
                x=alt.X("coluna:N", title=None, sort=ordem, axis=alt.Axis(labelAngle=-25, labelLimit=200)),
                y=alt.Y("linha:N", title=None, sort=ordem, axis=alt.Axis(labelLimit=200)),
                tooltip=[
                    alt.Tooltip("linha:N", title="Informação"),
                    alt.Tooltip("coluna:N", title="Comparada com"),
                    alt.Tooltip("rotulo:N", title="Spearman"),
                ],
            )
            quadrados = base_mapa.mark_rect().encode(
                color=alt.condition(
                    "isValid(datum.correlacao)",
                    alt.Color(
                        "correlacao:Q", title="Spearman",
                        scale=alt.Scale(domain=[-1, 0, 1], range=["#E7A18B", "#F0F2F4", "#79C7C9"]),
                        legend=alt.Legend(orient="bottom", direction="horizontal"),
                    ),
                    alt.value("#dedede"),
                )
            )
            rotulos = base_mapa.mark_text(fontSize=13).encode(
                text="rotulo:N",
                color=alt.value("#15272B"),
            )
            mapa = (quadrados + rotulos).properties(height=max(220, 65 * len(ordem)))
            st.altair_chart(mapa)
            st.caption("Spearman · −1: sentidos opostos · 0: pouca relação monotônica · +1: mesmo sentido. Correlação não implica causalidade.")
            if correlacao.isna().any().any():
                st.caption("N/D: alguma informação não varia neste recorte; a correlação correspondente não está definida.")
            with st.expander("Ver correlações em tabela"):
                st.dataframe(
                    correlacao.rename(index=VARIAVEIS, columns=VARIAVEIS).style.format(
                        lambda valor: numero_br(valor, 2), na_rep="N/D",
                    )
                )

st.caption("Fonte: Hotel Booking Demand — dados históricos.")
