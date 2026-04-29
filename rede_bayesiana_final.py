"""Rede Bayesiana manual para risco climatico.

Bibliotecas usadas:
- itertools.product: combinacoes de estados dos pais.
- numpy: media, percentis e matrizes numericas.
- pandas: leitura e tratamento do CSV.
- pgmpy: rede bayesiana, CPDs e inferencia.
"""

from itertools import product

import numpy as np
import pandas as pd
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.models import DiscreteBayesianNetwork

DATASET_PATH = 'Beginner_Climate_Change_Dataset_20_Features_1200_Rows.csv'

COLUNAS_MODELO = {
    'consumo_combustivel_fossil': 'fossil_fuel_consumption',
    'participacao_energia_renovavel': 'renewable_energy_share',
    'taxa_desmatamento': 'deforestation_rate',
    'concentracao_co2_ppm': 'co2_concentration_ppm',
    'anomalia_temperatura': 'temperature_anomaly',
    'aumento_nivel_mar_mm': 'sea_level_rise_mm',
    'dias_onda_calor': 'heatwave_days',
    'indice_seca': 'drought_index',
    'indice_qualidade_do_ar': 'air_quality_index',
    'indice_risco_climatico': 'climate_risk_index',
}

NIVEIS_VARIAVEIS = {
    0: 'baixo',
    1: 'medio',
    2: 'alto',
}

RELACOES_CAUSAIS = [
    ('consumo_combustivel_fossil', 'concentracao_co2_ppm'),
    ('participacao_energia_renovavel', 'concentracao_co2_ppm'),
    ('taxa_desmatamento', 'concentracao_co2_ppm'),
    ('concentracao_co2_ppm', 'anomalia_temperatura'),
    ('anomalia_temperatura', 'aumento_nivel_mar_mm'),
    ('anomalia_temperatura', 'dias_onda_calor'),
    ('anomalia_temperatura', 'indice_seca'),
    ('consumo_combustivel_fossil', 'indice_qualidade_do_ar'),
    ('dias_onda_calor', 'indice_qualidade_do_ar'),
    ('aumento_nivel_mar_mm', 'indice_risco_climatico'),
    ('indice_seca', 'indice_risco_climatico'),
    ('indice_qualidade_do_ar', 'indice_risco_climatico'),
]

ESPECIFICACOES_CPDS = [
    {'nome': 'consumo_combustivel_fossil', 'tipo': 'raiz'},
    {'nome': 'participacao_energia_renovavel', 'tipo': 'raiz'},
    {'nome': 'taxa_desmatamento', 'tipo': 'raiz'},
    {'nome': 'concentracao_co2_ppm', 'tipo': 'condicional', 'evidencias': ['consumo_combustivel_fossil', 'participacao_energia_renovavel', 'taxa_desmatamento']},
    {'nome': 'anomalia_temperatura', 'tipo': 'condicional', 'evidencias': ['concentracao_co2_ppm']},
    {'nome': 'aumento_nivel_mar_mm', 'tipo': 'condicional', 'evidencias': ['anomalia_temperatura']},
    {'nome': 'dias_onda_calor', 'tipo': 'condicional', 'evidencias': ['anomalia_temperatura']},
    {'nome': 'indice_seca', 'tipo': 'condicional', 'evidencias': ['anomalia_temperatura']},
    {'nome': 'indice_qualidade_do_ar', 'tipo': 'condicional', 'evidencias': ['consumo_combustivel_fossil', 'dias_onda_calor']},
    {'nome': 'indice_risco_climatico', 'tipo': 'condicional', 'evidencias': ['aumento_nivel_mar_mm', 'indice_seca', 'indice_qualidade_do_ar']},
]

UNIDADES = {
    'fossil_fuel_consumption': '%',
    'renewable_energy_share': '%',
    'deforestation_rate': '%',
    'co2_concentration_ppm': 'ppm',
    'temperature_anomaly': 'C',
    'sea_level_rise_mm': 'mm',
    'heatwave_days': 'dias',
    'drought_index': 'indice',
    'air_quality_index': 'indice',
    'climate_risk_index': '0-100',
}


def resumo_valores(rotulo, valores, unidade=''):
    """Imprime um resumo rapido de uma variavel original do CSV."""
    valores = np.asarray(valores)
    media = np.mean(valores) if len(valores) else float('nan')
    sufixo = f' {unidade}' if unidade else ''
    print(f"  - {rotulo}: {len(valores):,} registros (media: {media:.2f}{sufixo})")


def discretizar_valores(valores):
    """Converte valores continuos em tres faixas: baixo, medio e alto.

    A divisao usa os percentis 33 e 66.
    """
    valores = np.asarray(valores, dtype=float)
    if valores.size == 0:
        return np.array([], dtype=int)

    if np.allclose(valores, valores[0]):
        return np.zeros_like(valores, dtype=int)

    percentil_33, percentil_66 = np.percentile(valores, [33, 66])
    if np.isclose(percentil_33, percentil_66):
        percentil_66 = percentil_33 + 1e-9

    return np.array([0 if valor < percentil_33 else (1 if valor < percentil_66 else 2) for valor in valores], dtype=int)


def calcular_cpd_simples(dados_rede, alvo, evidencia=None, estados=3):
    """Calcula a distribuicao de um no raiz ou de um no com um unico pai."""
    if evidencia is None:
        contagem = dados_rede[alvo].value_counts().reindex(range(estados), fill_value=0)
        total = contagem.sum()
        return np.full(estados, 1.0 / estados) if total == 0 else (contagem / total).to_numpy()

    tabela = pd.crosstab(dados_rede[evidencia], dados_rede[alvo]).reindex(index=range(estados), columns=range(estados), fill_value=0)

    matriz_probabilidades = np.zeros((estados, estados))
    for estado_evidencia in range(estados):
        contagens = tabela.loc[estado_evidencia].to_numpy(dtype=float)
        total = contagens.sum()
        matriz_probabilidades[:, estado_evidencia] = np.full(estados, 1.0 / estados) if total == 0 else contagens / total

    return matriz_probabilidades


def calcular_cpd_multi(dados_rede, alvo, evidencias, estados=3):
    """Calcula uma CPD com varios pais usando todas as combinacoes possiveis."""
    combinacoes = list(product(range(estados), repeat=len(evidencias)))
    matriz_cpd = np.zeros((estados, len(combinacoes)))
    dados_trabalho = dados_rede[evidencias + [alvo]].copy()

    for indice_coluna, combinacao in enumerate(combinacoes):
        mascara = np.ones(len(dados_trabalho), dtype=bool)
        for evidencia, estado in zip(evidencias, combinacao):
            mascara &= dados_trabalho[evidencia].to_numpy() == estado

        subconjunto = dados_trabalho.loc[mascara, alvo]
        contagem = subconjunto.value_counts().reindex(range(estados), fill_value=0)
        total = contagem.sum()
        matriz_cpd[:, indice_coluna] = np.full(estados, 1.0 / estados) if total == 0 else (contagem / total).to_numpy()

    return matriz_cpd


# -----------------------------
# Leitura e preparacao dos dados
# -----------------------------
print('=' * 75)
print('REDE BAYESIANA - RISCO CLIMATICO')
print('=' * 75)

dados_csv = pd.read_csv(DATASET_PATH)
colunas_origem = list(COLUNAS_MODELO.values())
dados_base = dados_csv[colunas_origem].dropna().copy()

if dados_base.empty:
    raise ValueError('Nao ha registros completos suficientes para as colunas do modelo.')

# Conversão de valores contínuos em estados discretos.
dados_rede = pd.DataFrame({
    nome_modelo: discretizar_valores(dados_base[nome_origem].to_numpy())
    for nome_modelo, nome_origem in COLUNAS_MODELO.items()
})

print('\nDados utilizados:')
print(f'  - Registros disponiveis: {len(dados_base):,}')

print('\nResumo das variaveis originais:')
for nome_modelo, nome_origem in COLUNAS_MODELO.items():
    resumo_valores(nome_modelo, dados_base[nome_origem].to_numpy(), UNIDADES.get(nome_origem, ''))

print('\nVariaveis discretizadas em 3 estados: 0=baixo, 1=medio, 2=alto')


modelo = DiscreteBayesianNetwork(RELACOES_CAUSAIS)

# Nos de raiz usam a distribuicao marginal.
# Nos com pais usam a distribuicao condicional observada nos dados.
cpds = []
for especificacao in ESPECIFICACOES_CPDS:
    nome = especificacao['nome']
    if especificacao['tipo'] == 'raiz':
        cpds.append(TabularCPD(nome, 3, calcular_cpd_simples(dados_rede, nome).reshape(-1, 1)))
        continue

    evidencias = especificacao['evidencias']
    matriz = calcular_cpd_multi(dados_rede, nome, evidencias)
    cpds.append(TabularCPD(nome, 3, matriz, evidence=evidencias, evidence_card=[3] * len(evidencias)))

modelo.add_cpds(*cpds)

print(f'\nModelo valido: {modelo.check_model()}')

# Este bloco imprime a estrutura para o usuario copiar para o relatorio.
print('\nRelacoes causais usadas na rede:')
for origem, destino in RELACOES_CAUSAIS:
    print(f'  - {origem} -> {destino}')

# Aqui fica a legenda usada em todo o trabalho: baixo, medio e alto.
print('\nSeparacao dos niveis das variaveis:')
for nivel, rotulo in NIVEIS_VARIAVEIS.items():
    print(f'  - {nivel} = {rotulo}')

# -----------------------------
# Inferencia probabilistica
# -----------------------------
print(f"\n{'-' * 75}")
print('INFERENCIA')
print('-' * 75)

inferencia = VariableElimination(modelo)

consultas = [
    ('1. Risco climatico alto com aumento do nivel do mar, seca e qualidade do ar ruins?', ['indice_risco_climatico'], {'aumento_nivel_mar_mm': 2, 'indice_seca': 2, 'indice_qualidade_do_ar': 2}),
    ('2. Qualidade do ar ruim com consumo alto de combustivel fossil e muitas ondas de calor?', ['indice_qualidade_do_ar'], {'consumo_combustivel_fossil': 2, 'dias_onda_calor': 2}),
    ('3. Anomalia de temperatura com CO2 alto?', ['anomalia_temperatura'], {'concentracao_co2_ppm': 2}),
    ('4. CO2 alto com consumo alto de combustivel fossil, baixa energia renovavel e desmatamento alto?', ['concentracao_co2_ppm'], {'consumo_combustivel_fossil': 2, 'participacao_energia_renovavel': 0, 'taxa_desmatamento': 2}),
]

for titulo, variaveis, evidencia in consultas:
    print(f'\n{titulo}')
    print(inferencia.query(variables=variaveis, evidence=evidencia))

print(f"\n{'=' * 75}")
print('RELACOES MODELADAS')
print('=' * 75)

print(f"\n{'=' * 75}")
print('ANALISE CONCLUIDA COM SUCESSO!')
print('=' * 75 + '\n')
