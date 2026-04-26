PROJETO: REDES BAYESIANAS PARA ANÁLISE DO IMPACTO DA QUALIDADE DO AR
===================================================================

UNIVERSIDADE ESTADUAL DE MARINGÁ
Departamento de Informática
Disciplina: Aprendizagem de Máquina e Modelagem de Conhecimento Incerto
Professor: Wagner Igarashi
Tema: Redes Bayesianas

DESCRIÇÃO DO PROJETO
====================

Este projeto implementa uma Rede Bayesiana para modelar as relações de dependência
probabilística entre variáveis reais extraídas do conjunto air_quality.csv,
relacionando tráfego, poluentes atmosféricos, qualidade do ar e efeitos na saúde.

ARQUIVOS DO PROJETO
===================

1. rede_bayesiana_final.py
   - Script principal que constrói e executa a rede bayesiana
   - Realiza 4 análises probabilísticas diferentes
   - Gera visualização da rede em PNG
   - Usa biblioteca pgmpy (Python Library for Probabilistic Graphical Models)

2. Relatorio_Tecnico_Redes_Bayesianas.docx
   - Relatório técnico completo (~4 páginas)
   - Contém: problema, dataset, estrutura, resultados, conclusões e referências
   - Inclui descrição das 7 variáveis da rede atual
   - Explica as 4 análises probabilísticas realizadas

3. Slides_Redes_Bayesianas.pptx
   - Apresentação com 15 slides
   - Estrutura: Título, Introdução, Fundamentação, Metodologia, Resultados, Conclusões e Referências
   - Duração estimada: 10-15 minutos
   - Inclui diagramas e explicações das análises

4. air_quality.csv
   - Dataset real obtido do Kaggle
   - Dados de qualidade do ar de várias regiões dos EUA
   - Contém medições de poluentes e indicadores de saúde ambiental

5. rede_bayesiana.png
   - Visualização da rede bayesiana gerada
   - Mostra graficamente os 7 nós e suas relações

COMO EXECUTAR
=============

Pré-requisitos:
- Python 3.12+
- pip (gerenciador de pacotes)

Instalação de dependências:
  pip install pandas numpy pgmpy matplotlib networkx

Executar o código:
   python rede_bayesiana_final.py

Saída:
- Exibição das análises probabilísticas no console
- Arquivo rede_bayesiana.png com a visualização
- Confirmação: "Imagem salva: rede_bayesiana.png"

ESTRUTURA DA REDE BAYESIANA
===========================

Variáveis (7 nós):
- Trafego: Volume de tráfego veicular (0=baixo, 1=médio, 2=alto)
- DioxidoAzoto: Dióxido de azoto / NO2 (0=baixo, 1=médio, 2=alto)
- ParticulasFinas: Material particulado fino / PM2.5 (0=baixo, 1=médio, 2=alto)
- Ozonio: O3 / ozônio (0=baixo, 1=médio, 2=alto)
- QualidadeDoAr: Qualidade do ar (0=boa, 1=moderada, 2=ruim)
- AsmaPm25: Ocorrências de asma relacionadas à poluição (0=baixa, 1=média, 2=alta)
- HospitalizacoesRespiratorias: Hospitalizações respiratórias (0=baixa, 1=média, 2=alta)

Relacionamentos causais:
- Trafego → DioxidoAzoto
- Trafego → ParticulasFinas
- Ozonio → QualidadeDoAr
- DioxidoAzoto → QualidadeDoAr
- ParticulasFinas → QualidadeDoAr
- QualidadeDoAr → AsmaPm25
- QualidadeDoAr → HospitalizacoesRespiratorias

ANÁLISES REALIZADAS
===================

1. P(AsmaPm25=2 | QualidadeDoAr=2)
   → Probabilidade de asma alta com qualidade do ar ruim

2. P(QualidadeDoAr=2 | Trafego=2, ParticulasFinas=2)
   → Qualidade do ar ruim com tráfego alto e PM2.5 alto

3. P(HospitalizacoesRespiratorias=2 | DioxidoAzoto=2)
   → Hospitalizações respiratórias com NO2 alto

4. P(QualidadeDoAr=2 | Ozonio=2)
   → Qualidade do ar ruim com ozônio alto

5. Correlacao entre Trafego, DioxidoAzoto e ParticulasFinas
   → Tráfego como fonte associada ao aumento dos poluentes

6. Correlacao entre QualidadeDoAr, AsmaPm25 e HospitalizacoesRespiratorias
   → Piora da qualidade do ar associada a impactos na saúde

TECNOLOGIAS UTILIZADAS
=======================

- Python 3.12
- pgmpy (Probabilistic Graphical Models in Python)
- pandas (manipulação de dados)
- numpy (computação numérica)
- matplotlib (visualização)
- networkx (análise de grafos)
- warnings (tratamento de avisos)

CONCLUSÕES
==========

A rede bayesiana permite modelar com sucesso as relações de causalidade entre
fatores observados no conjunto air_quality.csv e sua influência na saúde pública.
As análises realizadas demonstram que:

1. O tráfego está associado ao aumento de dióxido de azoto e partículas finas
2. O ozônio entra como variável adicional na explicação da qualidade do ar
3. A piora da qualidade do ar aumenta a probabilidade de asma e internações
4. A rede fornece um modelo viável para inferência probabilística com dados reais

REFERÊNCIAS
===========

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
FIM DO README
============================================================
