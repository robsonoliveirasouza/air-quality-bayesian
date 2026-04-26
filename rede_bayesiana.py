# REDE BAYESIANA COM DATASET (KAGGLE) - AIR QUALITY

import pandas as pd
import numpy as np
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

import matplotlib.pyplot as plt
import networkx as nx

# 1. CARREGAR DATASET

df = pd.read_csv("air_quality.csv")

print("Colunas do dataset:")
print(df.columns)

print("\nPrimeiras linhas:")
print(df.head())

# 2. CRIAR VARIÁVEIS CATEGÓRICAS

coluna_valor = "Data Value" 

def classificar_poluicao(valor):
    if valor < 20:
        return 0  # baixa
    elif valor < 40:
        return 1  # média
    else:
        return 2  # alta

df["Poluicao"] = df[coluna_valor].apply(classificar_poluicao)

np.random.seed(42)

df["Trafego"] = np.random.choice([0, 1], size=len(df))
df["Industria"] = np.random.choice([0, 1], size=len(df))
df["Vento"] = np.random.choice([0, 1], size=len(df))
df["Umidade"] = np.random.choice([0, 1], size=len(df))
df["CO2"] = np.random.choice([0, 1], size=len(df))
df["Desmatamento"] = np.random.choice([0, 1], size=len(df))
df["Temperatura"] = np.random.choice([0, 1], size=len(df))

# Derivadas
df["QualidadeAr"] = df["Poluicao"].apply(lambda x: 0 if x == 0 else 1)
df["ProblemasResp"] = df["QualidadeAr"].apply(lambda x: np.random.choice([0, 1]))
df["AquecimentoGlobal"] = np.random.choice([0, 1], size=len(df))

# 3. DEFINIÇÃO DA REDE

model = DiscreteBayesianNetwork([
    ('Trafego', 'Poluicao'),
    ('Industria', 'Poluicao'),
    ('Poluicao', 'QualidadeAr'),
    ('Vento', 'QualidadeAr'),
    ('Umidade', 'QualidadeAr'),
    ('QualidadeAr', 'ProblemasResp'),
    ('CO2', 'AquecimentoGlobal'),
    ('Desmatamento', 'AquecimentoGlobal'),
    ('Temperatura', 'AquecimentoGlobal')
])

# 4. CPDs

cpd_trafego = TabularCPD('Trafego', 2, [[0.6], [0.4]])
cpd_industria = TabularCPD('Industria', 2, [[0.7], [0.3]])
cpd_vento = TabularCPD('Vento', 2, [[0.5], [0.5]])
cpd_umidade = TabularCPD('Umidade', 2, [[0.6], [0.4]])
cpd_co2 = TabularCPD('CO2', 2, [[0.5], [0.5]])
cpd_desmatamento = TabularCPD('Desmatamento', 2, [[0.7], [0.3]])
cpd_temperatura = TabularCPD('Temperatura', 2, [[0.6], [0.4]])

cpd_poluicao = TabularCPD(
    'Poluicao', 2,
    [[0.8, 0.5, 0.4, 0.1],
     [0.2, 0.5, 0.6, 0.9]],
    evidence=['Trafego', 'Industria'],
    evidence_card=[2, 2]
)

cpd_qualidade = TabularCPD(
    'QualidadeAr', 2,
    [[0.9, 0.7, 0.6, 0.3, 0.7, 0.5, 0.4, 0.1],
     [0.1, 0.3, 0.4, 0.7, 0.3, 0.5, 0.6, 0.9]],
    evidence=['Poluicao', 'Vento', 'Umidade'],
    evidence_card=[2, 2, 2]
)

cpd_problemas = TabularCPD(
    'ProblemasResp', 2,
    [[0.8, 0.3],
     [0.2, 0.7]],
    evidence=['QualidadeAr'],
    evidence_card=[2]
)

cpd_aquecimento = TabularCPD(
    'AquecimentoGlobal', 2,
    [[0.9, 0.7, 0.6, 0.3, 0.7, 0.5, 0.4, 0.1],
     [0.1, 0.3, 0.4, 0.7, 0.3, 0.5, 0.6, 0.9]],
    evidence=['CO2', 'Desmatamento', 'Temperatura'],
    evidence_card=[2, 2, 2]
)

# 5. ADICIONAR AO MODELO

model.add_cpds(
    cpd_trafego, cpd_industria, cpd_vento, cpd_umidade,
    cpd_co2, cpd_desmatamento, cpd_temperatura,
    cpd_poluicao, cpd_qualidade, cpd_problemas, cpd_aquecimento
)

print("\nModelo válido?", model.check_model())

# 6. INFERÊNCIA

infer = VariableElimination(model)

print("\nProbabilidade de Problemas Respiratórios dado alta poluição:")
print(infer.query(variables=['ProblemasResp'], evidence={'Poluicao': 1}))

# 7. VISUALIZAÇÃO

G = nx.DiGraph()
G.add_edges_from(model.edges())

plt.figure(figsize=(10,7))
pos = nx.spring_layout(G)

nx.draw(
    G, pos,
    with_labels=True,
    node_size=3000,
    node_color="lightblue",
    font_size=10,
    font_weight="bold",
    arrows=True
)

plt.title("Rede Bayesiana - Impacto Ambiental")
plt.show()