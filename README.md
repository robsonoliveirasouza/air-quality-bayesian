PROJETO: REDES BAYESIANAS PARA ANÁLISE DO IMPACTO DA QUALIDADE DO AR
===================================================================

UNIVERSIDADE ESTADUAL DE MARINGÁ
Departamento de Informática
Disciplina: Aprendizagem de Máquina e Modelagem de Conhecimento Incerto
Professor: Wagner Igarashi
Tema: Redes Bayesianas

RESUMO
======

Este relatório técnico apresenta o desenvolvimento de uma Rede Bayesiana para
analisar relações de dependência probabilística entre variáveis ambientais e de
saúde extraídas do conjunto air_quality.csv. A rede foi estruturada com dados
reais relacionados a tráfego veicular, dióxido de nitrogênio, partículas finas,
ozônio, qualidade do ar, asma e hospitalizações respiratórias. A partir dessa
modelagem, foram realizadas inferências probabilísticas que evidenciam a relação
entre poluição atmosférica e agravamento de indicadores de saúde pública.

1. INTRODUÇÃO
=============

A qualidade do ar é um fator determinante para a saúde humana e para a dinâmica
ambiental urbana. Em regiões densamente povoadas, o tráfego veicular e a presença
de poluentes atmosféricos tendem a elevar a concentração de substâncias nocivas,
aumentando o risco de doenças respiratórias e de hospitalizações associadas.

Neste contexto, as redes bayesianas oferecem uma forma adequada de representar
relações causais e probabilísticas entre variáveis observadas. Diferentemente de
métodos puramente descritivos, essa abordagem permite estimar a probabilidade de
um evento a partir de evidências parciais, favorecendo análises interpretáveis.

2. OBJETIVO
===========

O objetivo deste trabalho é construir uma Rede Bayesiana baseada em dados reais
para modelar a influência do tráfego e de poluentes atmosféricos sobre a
qualidade do ar e seus reflexos na saúde respiratória.

De forma mais específica, o projeto busca:

1. Identificar variáveis relevantes no arquivo air_quality.csv.
2. Discretizar os dados para permitir modelagem probabilística.
3. Construir uma estrutura causal coerente com as correlações observadas.
4. Calcular distribuições condicionais e realizar inferências na rede.
5. Gerar uma visualização gráfica da estrutura resultante.

3. BASE DE DADOS
================

O arquivo air_quality.csv reúne indicadores ambientais e de saúde pública
relacionados à qualidade do ar em diferentes regiões e períodos. A análise foi
desenvolvida a partir de variáveis que apresentam associação com emissão de
poluentes e impactos respiratórios.

As variáveis utilizadas neste trabalho foram:

- Trafego: volume de tráfego veicular.
- DioxidoAzoto: concentração de dióxido de nitrogênio (NO2).
- ParticulasFinas: concentração de material particulado fino (PM2.5).
- Ozonio: concentração de ozônio (O3).
- QualidadeDoAr: índice agregado de qualidade do ar.
- AsmaPm25: registros de asma associados à poluição por PM2.5.
- HospitalizacoesRespiratorias: internações respiratórias.

4. METODOLOGIA
==============

A construção da rede seguiu as etapas abaixo:

4.1 Extração dos dados

Foram extraídos do arquivo air_quality.csv os valores associados às variáveis de
poluição, tráfego e saúde. Como os registros possuem naturezas e frequências
diferentes, foi necessário selecionar os indicadores mais consistentes para a
modelagem.

4.2 Discretização

As variáveis numéricas foram discretizadas em três estados: baixo, médio e alto.
A discretização foi baseada nos percentis 33 e 66, o que permite dividir os dados
em faixas representativas para cálculo de probabilidades condicionais.

4.3 Estrutura da rede

A rede foi definida com as seguintes relações causais:

- Trafego → DioxidoAzoto
- Trafego → ParticulasFinas
- Ozonio → QualidadeDoAr
- DioxidoAzoto → QualidadeDoAr
- ParticulasFinas → QualidadeDoAr
- QualidadeDoAr → AsmaPm25
- QualidadeDoAr → HospitalizacoesRespiratorias

Essa estrutura representa a hipótese de que o tráfego contribui para o aumento de
poluentes primários, que por sua vez afetam a qualidade do ar e, em seguida, os
indicadores de saúde respiratória.

4.4 Estimativa das probabilidades

As distribuições condicionais foram estimadas com base em frequências observadas
a partir de um conjunto amostral discretizado. Isso permitiu construir as CPDs
(Conditional Probability Distributions) necessárias para a inferência.

4.5 Inferência probabilística

Com o uso da biblioteca pgmpy, foram realizadas consultas por eliminação de
variáveis para calcular probabilidades condicionadas a evidências específicas,
como poluição elevada ou tráfego intenso.

5. ESTRUTURA DA REDE BAYESIANA
==============================

Variáveis (7 nós):
- Trafego: volume de tráfego veicular (0=baixo, 1=médio, 2=alto)
- DioxidoAzoto: dióxido de nitrogênio / NO2 (0=baixo, 1=médio, 2=alto)
- ParticulasFinas: material particulado fino / PM2.5 (0=baixo, 1=médio, 2=alto)
- Ozonio: ozônio / O3 (0=baixo, 1=médio, 2=alto)
- QualidadeDoAr: qualidade do ar (0=boa, 1=moderada, 2=ruim)
- AsmaPm25: ocorrências de asma relacionadas à poluição (0=baixa, 1=média, 2=alta)
- HospitalizacoesRespiratorias: hospitalizações respiratórias (0=baixa, 1=média, 2=alta)

Relacionamentos causais:
- Trafego → DioxidoAzoto
- Trafego → ParticulasFinas
- Ozonio → QualidadeDoAr
- DioxidoAzoto → QualidadeDoAr
- ParticulasFinas → QualidadeDoAr
- QualidadeDoAr → AsmaPm25
- QualidadeDoAr → HospitalizacoesRespiratorias

6. ANÁLISES REALIZADAS
======================

As seguintes consultas probabilísticas foram executadas na rede:

1. P(AsmaPm25=2 | QualidadeDoAr=2)
   → Probabilidade de asma alta quando a qualidade do ar está ruim.

2. P(QualidadeDoAr=2 | Trafego=2, ParticulasFinas=2)
   → Probabilidade de qualidade do ar ruim com tráfego alto e PM2.5 alto.

3. P(HospitalizacoesRespiratorias=2 | DioxidoAzoto=2)
   → Probabilidade de hospitalizações respiratórias quando o NO2 está alto.

4. P(QualidadeDoAr=2 | Ozonio=2)
   → Probabilidade de qualidade do ar ruim quando o ozônio está alto.

Essas consultas permitem verificar como diferentes evidências alteram a
probabilidade dos desfechos relacionados à saúde.

7. RESULTADOS
=============

A execução do script principal produziu uma rede válida e consistente, com
visualização em PNG e inferências probabilísticas coerentes com a estrutura
proposta.

Principais resultados observados:

1. O tráfego aparece como fonte relevante para dióxido de nitrogênio e partículas finas.
2. O ozônio foi incluído como variável adicional influenciando a qualidade do ar.
3. A piora da qualidade do ar aumenta a probabilidade de asma e hospitalizações.
4. As inferências indicam associação forte entre poluição elevada e agravamento
   dos indicadores respiratórios.

8. CONCLUSÕES
=============

A Rede Bayesiana desenvolvida neste trabalho mostrou-se adequada para representar
relações entre tráfego, poluentes atmosféricos e saúde respiratória com base em
dados reais. A modelagem probabilística permitiu incorporar dependências entre as
variáveis e realizar consultas úteis para interpretação de cenários ambientais.

Conclui-se que:

1. O tráfego contribui para o aumento de poluentes atmosféricos.
2. O ozônio também participa da explicação da qualidade do ar.
3. A piora na qualidade do ar eleva a probabilidade de eventos respiratórios
   adversos.
4. O modelo é útil como base para análises futuras e para apoio à interpretação
   de relações ambientais e de saúde pública.

9. TECNOLOGIAS UTILIZADAS
=========================

- Python 3.12
- pgmpy (Probabilistic Graphical Models in Python)
- pandas (manipulação de dados)
- numpy (computação numérica)
- matplotlib (visualização)
- networkx (análise de grafos)
- warnings (tratamento de avisos)

10. ARQUIVOS DO PROJETO
=======================

1. rede_bayesiana_final.py
   - Script principal da rede bayesiana.
   - Executa o fluxo completo: leitura, modelagem, inferência e visualização.

2. README.md
   - Relatório técnico em formato textual.
   - Pode ser adaptado posteriormente para um PDF formal.

3. air_quality.csv
   - Base de dados original utilizada para extração dos indicadores.

4. rede_bayesiana.png
   - Imagem gerada com a estrutura da rede bayesiana.

11. REFERÊNCIAS
===============

1. Pearl, J. (1988). Probabilistic Reasoning in Intelligent Systems: Networks
   of Plausible Inference. Morgan Kaufmann.

2. Korb, K. B., & Nicholson, A. E. (2010). Bayesian Artificial Intelligence
   (2nd ed.). CRC Press.

3. Ankan, A., & Panda, S. (2015). pgmpy: Probabilistic Graphical Models using
   Python. In Proceedings of the 14th Python in Science Conference (pp. 6-11).

4. Kaggle. (2023). Air Quality Dataset.

5. New York City Open Data. Indicadores de qualidade do ar e saúde ambiental.

AUTOR(ES)
=========

Trabalho realizado como avaliação da disciplina AMMCI (S2)
Universidade Estadual de Maringá
2026

============================================================
FIM DO RELATÓRIO
============================================================
