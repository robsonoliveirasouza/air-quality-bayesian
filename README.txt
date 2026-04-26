PROJETO: REDES BAYESIANAS PARA ANÁLISE DE IMPACTO AMBIENTAL
========================================================

UNIVERSIDADE ESTADUAL DE MARINGÁ
Departamento de Informática
Disciplina: Aprendizagem de Máquina e Modelagem de Conhecimento Incerto
Professor: Wagner Igarashi
Tema: Redes Bayesianas

DESCRIÇÃO DO PROJETO
====================

Este projeto implementa uma Rede Bayesiana para modelar as relações de dependência
probabilística entre fatores ambientais e sua influência na qualidade do ar e
problemas respiratórios.

ARQUIVOS DO PROJETO
===================

1. rede_bayesiana.py
   - Script principal que constrói e executa a rede bayesiana
   - Realiza 6 análises probabilísticas diferentes
   - Gera visualização da rede em PNG
   - Usa biblioteca pgmpy (Python Library for Probabilistic Graphical Models)

2. Relatorio_Tecnico_Redes_Bayesianas.docx
   - Relatório técnico completo (~4 páginas)
   - Contém: problema, dataset, estrutura, resultados, conclusões e referências
   - Inclui descrição de todas as 11 variáveis
   - Explica as 6 análises probabilísticas realizadas

3. Slides_Redes_Bayesianas.pptx
   - Apresentação com 15 slides
   - Estrutura: Título, Introdução, Fundamentação, Metodologia, Resultados, Conclusões e Referências
   - Duração estimada: 10-15 minutos
   - Inclui diagramas e explicações das análises

4. air_quality.csv
   - Dataset real obtido do Kaggle
   - Dados de qualidade do ar de várias regiões dos EUA
   - Contém medições de poluentes (NO2) em ppb

5. rede_bayesiana.png
   - Visualização da rede bayesiana gerada
   - Mostra graficamente all 11 nós e suas relações

COMO EXECUTAR
=============

Pré-requisitos:
- Python 3.8+
- pip (gerenciador de pacotes)

Instalação de dependências:
  pip install pandas numpy pgmpy matplotlib networkx

Executar o código:
  python rede_bayesiana.py

Saída:
- Exibição das análises probabilísticas no console
- Arquivo rede_bayesiana.png com a visualização
- Confirmação: "✓ Rede bayesiana salva em 'rede_bayesiana.png'"

ESTRUTURA DA REDE BAYESIANA
===========================

Variáveis (11 nós):
- Trafego: Volume de tráfego veicular (0=baixo, 1=alto)
- Industria: Atividades industriais (0=ausente, 1=presente)
- CO2: Dióxido de carbono (0=baixo, 1=alto)
- Desmatamento: Taxa de desmatamento (0=baixo, 1=alto)
- AquecimentoGlobal: Aquecimento global (0=não, 1=sim)
- Temperatura: Temperatura ambiente (0=baixa, 1=elevada)
- Vento: Ventos favoráveis (0=ausente, 1=presente)
- Umidade: Umidade relativa (0=baixa, 1=alta)
- Poluicao: Nível de poluição atmosférica (0=baixa, 1=média, 2=alta)
- QualidadeAr: Qualidade do ar (0=boa, 1=ruim)
- ProblemasResp: Problemas respiratórios (0=não, 1=sim)

Relacionamentos causais:
- CO2 + Desmatamento → AquecimentoGlobal
- AquecimentoGlobal → Temperatura
- Temperatura → Umidade
- Trafego + Industria + CO2 + Desmatamento → Poluicao
- Poluicao + Vento + Umidade → QualidadeAr
- QualidadeAr → ProblemasResp

ANÁLISES REALIZADAS
===================

1. P(ProblemasResp=1 | Poluição=1) = 52.07%
   → Problemas respiratórios com alta poluição

2. P(QualidadeAr=1 | Trafego=1, Industria=1) = 53.62%
   → Qualidade do ar ruim com alto tráfego e indústria

3. P(AquecimentoGlobal=1 | CO2=1, Desmatamento=1) = 70.00%
   → Aquecimento global com alto CO2 e desmatamento

4. P(Temperatura=1 | AquecimentoGlobal=1) = 70.00%
   → Temperatura elevada com aquecimento global

5. P(Umidade=1 | Temperatura=1) = 60.00%
   → Umidade alta com temperatura elevada

6. P(ProblemasResp=1 | múltiplos fatores) = 70.00%
   → Problemas respiratórios com fatores combinados

TECNOLOGIAS UTILIZADAS
=======================

- Python 3.14.3
- pgmpy (Probabilistic Graphical Models in Python)
- pandas (manipulação de dados)
- numpy (computação numérica)
- matplotlib (visualização)
- networkx (análise de grafos)
- python-docx (geração de relatórios)
- python-pptx (geração de slides)

CONCLUSÕES
==========

A rede bayesiana permite modelar com sucesso as relações de causalidade entre
fatores ambientais e sua influência na saúde pública. As análises realizadas
demonstram que:

1. Fatores antrópicos (tráfego, indústria) são determinantes na qualidade do ar
2. Mudanças climáticas (CO2, desmatamento) influenciam a temperatura local
3. A probabilidade de problemas respiratórios aumenta exponencialmente com
   múltiplos fatores negativos combinados
4. A rede fornece um modelo viável para simulação de cenários e apoio a
   decisões de políticas ambientais

REFERÊNCIAS
===========

1. Pearl, J. (1988). Probabilistic Reasoning in Intelligent Systems: Networks 
   of Plausible Inference. Morgan Kaufmann.

2. Korb, K. B., & Nicholson, A. E. (2010). Bayesian Artificial Intelligence 
   (2nd ed.). CRC Press.

3. Ankan, A., & Panda, S. (2015). pgmpy: Probabilistic Graphical Models using 
   Python. In Proceedings of the 14th Python in Science Conference (pp. 6-11).

4. UCI Machine Learning Repository. (2023). Air Quality Dataset.

5. Kaggle. (2023). Air Quality Datasets.

AUTOR(ES)
=========

Trabalho realizado como avaliação da disciplina AMMCI (S2)
Universidade Estadual de Maringá
2026

============================================================
FIM DO README
============================================================
