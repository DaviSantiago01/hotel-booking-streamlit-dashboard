# Hotel Booking — Dashboards em Streamlit

Projeto acadêmico em Streamlit para explorar dados de reservas de hotéis, com base na análise exploratória do dataset **Hotel Booking Demand**.

## Dashboards

1. **Laboratório de análise:** exploração das distribuições e correlações entre variáveis.
2. **Visão gerencial:** indicadores e gráficos sobre reservas e cancelamentos para apoiar a gestão hoteleira.

## Análise exploratória

A pasta [`notebooks/`](notebooks/) contém o notebook [`eda_hotel_booking.ipynb`](notebooks/eda_hotel_booking.ipynb), com a análise da estrutura dos dados, distribuições, valores ausentes, outliers e relações entre variáveis. Ele serve de referência para os dashboards.

## Dados

O arquivo [`data/hotel_bookings.csv`](data/hotel_bookings.csv) contém a base pública [Hotel Booking Demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand), a mesma utilizada na EDA: 119.390 reservas e 32 colunas.

O CSV foi mantido com os valores originais, incluindo ausências e linhas idênticas. Ele acompanhará o aplicativo para permitir o carregamento automático, sem upload pelo usuário.

## Executar localmente

Com Python 3.11 ou superior, execute os comandos abaixo na pasta do projeto:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

Abra o endereço informado no terminal. O app carrega o CSV automaticamente e permite conferir uma amostra dos dados. As duas abas estão disponíveis; os filtros, gráficos e indicadores serão implementados nas próximas etapas.

## Uso de IA

O Codex, da OpenAI, apoiou pontos específicos do desenvolvimento e ajudou a compreender as alternativas de implementação.
