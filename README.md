# Hotel Booking — Dashboards em Streamlit

Projeto acadêmico em Streamlit para explorar dados de reservas de hotéis, com base na análise exploratória do dataset **Hotel Booking Demand**.

## Dashboards

1. **Visão geral:** primeira aba, com indicadores e gráficos sobre reservas e cancelamentos para gestores e equipes de reservas de hotéis.
2. **Análise detalhada:** filtros, histogramas e correlações para investigar as informações das reservas.

A Visão geral corresponde ao Dashboard 2 do enunciado; a Análise detalhada corresponde ao Dashboard 1, o laboratório de distribuição e correlação.

Os dois esboços estão em [`entregas/`](entregas/): [Visão geral](entregas/rascunho_dashboard_2.png) e [Análise detalhada](entregas/rascunho_dashboard_1.png). As imagens mostram a organização planejada, com gráficos ilustrativos.

## Análise exploratória

A pasta [`notebooks/`](notebooks/) contém o notebook [`eda_hotel_booking.ipynb`](notebooks/eda_hotel_booking.ipynb), com a análise da estrutura dos dados, distribuições, valores ausentes, outliers e relações entre variáveis. Ele serve de referência para os dashboards.

## Dados

O arquivo [`data/hotel_bookings.csv`](data/hotel_bookings.csv) contém a base pública [Hotel Booking Demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand), a mesma utilizada na EDA: 119.390 reservas e 32 colunas.

O CSV original foi preservado. O notebook exporta a versão tratada em [`data/hotel_bookings_tratado.csv`](data/hotel_bookings_tratado.csv), usada automaticamente pelo aplicativo, sem upload pelo usuário. Ela contém o tratamento das ausências e o status legível das reservas, mantendo todas as linhas e os valores extremos.

## Executar localmente

Com Python 3.11 ou superior, execute os comandos abaixo na pasta do projeto:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

Abra o endereço informado no terminal. O app carrega o CSV automaticamente. Os filtros da lateral selecionam as reservas usadas nas duas abas.

A **Visão geral** mostra quatro indicadores, cancelamentos por tipo de hotel, cancelamentos por faixa de antecedência e volume por mês e ano de chegada. As taxas são calculadas dentro de cada grupo. O volume mensal inclui canceladas e não canceladas; a base cobre julho/2015 a agosto/2017.

Na **Análise detalhada**, você escolhe as informações e vê histogramas interativos e a correlação de Spearman. O zoom só muda a visualização, enquanto os filtros alteram o conjunto de reservas. O mapa mostra N/D quando uma informação não varia e orienta a seleção de pelo menos duas informações.

O slider permite escolher o intervalo de valores, e “Limpar filtros” retorna à base completa. O nível de detalhe ajusta as faixas dos histogramas de antecedência e diária; noites e pedidos mantêm uma barra por valor inteiro. A opção “Um gráfico por linha” amplia os histogramas. As opções “Ver valores dos gráficos” e “Ver correlações em tabela” permitem consultar os resultados numéricos.

## Uso de IA

Utilizei o Codex, da OpenAI, como apoio no desenvolvimento e na compreensão das análises, revisando as sugestões antes de aplicá-las.
