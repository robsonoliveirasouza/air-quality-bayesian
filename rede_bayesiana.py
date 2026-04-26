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
    # Lado esquerdo - Aquecimento Global e Temperatura
    ('AquecimentoGlobal', 'Temperatura'),
    ('CO2', 'AquecimentoGlobal'),
    ('Desmatamento', 'AquecimentoGlobal'),
    # Conexão entre os lados (Aquecimento Global afeta Poluição)
    ('CO2', 'Poluicao'),
    ('Desmatamento', 'Poluicao'),
    ('Temperatura', 'Umidade'),  # Temperatura afeta Umidade
    # Lado direito - Qualidade do Ar
    ('Trafego', 'Poluicao'),
    ('Industria', 'Poluicao'),
    ('Poluicao', 'QualidadeAr'),
    ('Vento', 'QualidadeAr'),
    ('Umidade', 'QualidadeAr'),
    ('QualidadeAr', 'ProblemasResp')
])

# 4. CPDs

cpd_trafego = TabularCPD('Trafego', 2, [[0.6], [0.4]])
cpd_industria = TabularCPD('Industria', 2, [[0.7], [0.3]])
cpd_vento = TabularCPD('Vento', 2, [[0.5], [0.5]])
cpd_umidade = TabularCPD(
    'Umidade', 2,
    [[0.7, 0.4],
     [0.3, 0.6]],
    evidence=['Temperatura'],
    evidence_card=[2]
)
cpd_co2 = TabularCPD('CO2', 2, [[0.5], [0.5]])
cpd_desmatamento = TabularCPD('Desmatamento', 2, [[0.7], [0.3]])
cpd_temperatura = TabularCPD(
    'Temperatura', 2,
    [[0.7, 0.3],
     [0.3, 0.7]],
    evidence=['AquecimentoGlobal'],
    evidence_card=[2]
)

cpd_poluicao = TabularCPD(
    'Poluicao', 2,
    [[0.7, 0.5, 0.4, 0.2, 0.5, 0.3, 0.2, 0.1, 0.4, 0.2, 0.15, 0.08, 0.2, 0.1, 0.05, 0.02],
     [0.3, 0.5, 0.6, 0.8, 0.5, 0.7, 0.8, 0.9, 0.6, 0.8, 0.85, 0.92, 0.8, 0.9, 0.95, 0.98]],
    evidence=['Trafego', 'Industria', 'CO2', 'Desmatamento'],
    evidence_card=[2, 2, 2, 2]
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
    [[0.9, 0.7, 0.6, 0.3],
     [0.1, 0.3, 0.4, 0.7]],
    evidence=['CO2', 'Desmatamento'],
    evidence_card=[2, 2]
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

print("\n" + "="*60)
print("ANÁLISES PROBABILÍSTICAS")
print("="*60)

print("\n1. Probabilidade de Problemas Respiratórios dado alta poluição:")
print(infer.query(variables=['ProblemasResp'], evidence={'Poluicao': 1}))

print("\n2. Probabilidade de Qualidade do Ar ruim dado alto trafego e indústria:")
print(infer.query(variables=['QualidadeAr'], evidence={'Trafego': 1, 'Industria': 1}))

print("\n3. Probabilidade de Aquecimento Global dado alto CO2 e Desmatamento:")
print(infer.query(variables=['AquecimentoGlobal'], evidence={'CO2': 1, 'Desmatamento': 1}))

print("\n4. Probabilidade de Temperatura elevada dado Aquecimento Global:")
print(infer.query(variables=['Temperatura'], evidence={'AquecimentoGlobal': 1}))

print("\n5. Probabilidade de Umidade alta dado Temperatura elevada:")
print(infer.query(variables=['Umidade'], evidence={'Temperatura': 1}))

print("\n6. Probabilidade de Problemas Respiratórios dado múltiplos fatores:")
resultado = infer.query(
    variables=['ProblemasResp'], 
    evidence={'Poluicao': 1, 'QualidadeAr': 1, 'CO2': 1, 'Desmatamento': 1}
)
print(resultado)

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
plt.savefig('rede_bayesiana.png', dpi=300, bbox_inches='tight')
print("\n✓ Rede bayesiana salva em 'rede_bayesiana.png'")
plt.show()