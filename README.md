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

Abra o endereço informado no terminal. O app carrega o CSV automaticamente e apresenta os indicadores na aba Visão geral. Os filtros e gráficos serão implementados nas próximas etapas.

## Uso de IA

O Codex, da OpenAI, apoiou pontos específicos do desenvolvimento e ajudou a compreender as alternativas de implementação.
