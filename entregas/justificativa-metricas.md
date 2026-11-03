# Justificativa das métricas

A Visão geral é voltada a gestores e equipes de reservas de hotéis. Os quatro indicadores resumem o volume de reservas, os cancelamentos, a antecedência e o valor das diárias na base histórica.

Os cálculos usam `data/hotel_bookings_tratado.csv` e consideram o recorte definido pelos filtros da lateral. Com todos os hotéis e o intervalo completo, os indicadores representam toda a base. Se o recorte não tiver reservas, as medidas sem valor são exibidas como um traço; a contagem fica em zero.

## Total de reservas

- **Variável e cálculo:** contagem das linhas do recorte selecionado.
- **O que mede:** quantidade de reservas, incluindo as canceladas.
- **Por que escolhi:** dá contexto aos demais indicadores e mostra o tamanho do conjunto analisado.
- **Decisão apoiada:** comparar o volume de reservas entre hotéis ou faixas de valores usando os filtros da lateral.
- **O que comunica ao público:** quantas reservas sustentam a análise. Não representa hóspedes nem quartos ocupados.

## Taxa de cancelamento

- **Variável e cálculo:** quantidade de `booking_status = Canceled` dividida pelo total de reservas, multiplicada por 100.
- **O que mede:** porcentagem de reservas canceladas.
- **Por que escolhi:** cancelamentos foram um dos principais temas investigados na EDA. A proporção permite comparar grupos de tamanhos diferentes.
- **Decisão apoiada:** identificar segmentos que merecem investigação e acompanhamento das reservas.
- **O que comunica ao público:** a frequência de cancelamento no recorte, sem explicar sua causa nem prever o resultado de uma reserva individual.

## Antecedência mediana

- **Variável e cálculo:** mediana de `lead_time`, em dias.
- **O que mede:** valor central da antecedência entre a realização da reserva e a chegada.
- **Por que escolhi:** a distribuição é assimétrica; a mediana sofre menos influência das reservas feitas com muita antecedência.
- **Decisão apoiada:** orientar a escolha de janelas de acompanhamento e comunicação antes da chegada.
- **O que comunica ao público:** com quanta antecedência as reservas costumam ser realizadas, considerando tanto canceladas quanto não canceladas.

## Diária média

- **Variável e cálculo:** média de `adr` nas reservas com `booking_status = Not Canceled`.
- **O que mede:** média dos valores médios diários registrados nas reservas não canceladas.
- **Por que escolhi:** acrescenta uma referência de preço ao panorama das reservas, sem misturar os dois status.
- **Decisão apoiada:** apoiar a comparação descritiva dos valores de diária entre recortes e levantar perguntas sobre diferenças de preço.
- **O que comunica ao público:** o valor médio diário desse grupo. Cada reserva tem o mesmo peso; o cálculo não é ponderado por noites e não representa receita total nem lucro.

## Limites da leitura

Os indicadores descrevem uma base histórica de dois hotéis, e não a operação atual de um hotel. As linhas idênticas e os valores extremos foram preservados conforme as decisões da EDA. A diária média pode ser influenciada por extremos, e diferenças observadas não demonstram causalidade.
