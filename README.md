# Rede Bayesiana - Risco Climatico

Este projeto implementa uma rede bayesiana manual para analisar risco climatico a partir de um dataset com 10 variaveis selecionadas do arquivo `Beginner_Climate_Change_Dataset_20_Features_1200_Rows.csv`.

O foco do trabalho nao e aprender a estrutura automaticamente. A estrutura causal, a discretizacao e as CPDs sao definidas de forma controlada para facilitar a explicacao tecnica no relatorio.

## O que o script faz

O arquivo [rede_bayesiana_final.py](rede_bayesiana_final.py) executa quatro etapas principais:

1. Le o CSV e extrai apenas as colunas usadas no modelo.
2. Converte os valores continuos em tres niveis discretos: `0=baixo`, `1=medio`, `2=alto`.
3. Monta manualmente a estrutura causal da rede bayesiana.
4. Calcula CPDs por frequencia e executa consultas de inferencia.

## Bibliotecas usadas

`itertools.product`
: gera todas as combinacoes possiveis dos estados dos pais quando uma variavel tem mais de um antecedente.

`numpy`
: calcula media, percentis e manipula vetores e matrizes numericas.

`pandas`
: carrega o CSV, filtra colunas e calcula tabelas de frequencia.

`pgmpy`
: fornece `DiscreteBayesianNetwork`, `TabularCPD` e `VariableElimination`.

## Variaveis do modelo

As variaveis internas usam nomes em portugues para facilitar a leitura:

- `consumo_combustivel_fossil`
- `participacao_energia_renovavel`
- `taxa_desmatamento`
- `concentracao_co2_ppm`
- `anomalia_temperatura`
- `aumento_nivel_mar_mm`
- `dias_onda_calor`
- `indice_seca`
- `indice_qualidade_do_ar`
- `indice_risco_climatico`

Essas variaveis sao mapeadas para as colunas originais do CSV por meio da constante `COLUNAS_MODELO`.

## Separacao dos niveis

Todas as variaveis sao transformadas em tres estados discretos:

- `0 = baixo`
- `1 = medio`
- `2 = alto`

A discretizacao usa os percentis 33 e 66. Isso cria tres faixas equilibradas para que a rede trabalhe com estados categoricos.

## Estrutura causal

A rede foi montada manualmente. As relacoes usadas sao:

- consumo de combustivel fossil -> concentracao de CO2
- participacao de energia renovavel -> concentracao de CO2
- taxa de desmatamento -> concentracao de CO2
- concentracao de CO2 -> anomalia de temperatura
- anomalia de temperatura -> aumento do nivel do mar
- anomalia de temperatura -> dias de onda de calor
- anomalia de temperatura -> indice de seca
- consumo de combustivel fossil -> indice de qualidade do ar
- dias de onda de calor -> indice de qualidade do ar
- aumento do nivel do mar -> indice de risco climatico
- indice de seca -> indice de risco climatico
- indice de qualidade do ar -> indice de risco climatico

Essa estrutura esta declarada em `RELACOES_CAUSAIS`.

## Como as CPDs sao construidas

As CPDs nao sao inventadas manualmente linha por linha. Elas sao estimadas a partir da frequencia observada no dataset discretizado.

### Nos de raiz

Variaveis sem pais usam a distribuicao marginal observada nos dados. Exemplo:

- `consumo_combustivel_fossil`
- `participacao_energia_renovavel`
- `taxa_desmatamento`

### Nos condicionais

Variaveis com pais usam tabelas condicionais calculadas por frequencia. Exemplos:

- `concentracao_co2_ppm` depende de tres pais.
- `anomalia_temperatura` depende de `concentracao_co2_ppm`.
- `indice_risco_climatico` depende de `aumento_nivel_mar_mm`, `indice_seca` e `indice_qualidade_do_ar`.

As funcoes usadas para isso sao:

- `calcular_cpd_simples`
- `calcular_cpd_multi`

## Leitura das funcoes

### `resumo_valores`
Imprime um resumo rapido da variavel original, com quantidade de registros e media.

### `discretizar_valores`
Converte valores continuos em tres estados discretos usando os percentis 33 e 66.

### `calcular_cpd_simples`
Calcula a distribuicao de uma variavel raiz ou de uma variavel com um unico pai.

### `calcular_cpd_multi`
Calcula uma CPD com varios pais. Para isso, percorre todas as combinacoes possiveis dos estados dos pais usando `product`.

## Execucao do modelo

Depois de construir a rede e adicionar as CPDs, o script:

1. valida a estrutura com `modelo.check_model()`;
2. cria o objeto `VariableElimination`;
3. executa consultas de inferencia com evidencias fixadas;
4. imprime as relacoes causais e a legenda dos estados.

## Saida esperada

Ao rodar o script, voce vera:

- um resumo dos dados usados;
- a media das variaveis originais;
- a confirmacao de que o modelo e valido;
- a lista das relacoes causais;
- a separacao dos niveis das variaveis;
- algumas consultas de inferencia probabilistica;
- um resumo final das relacoes modeladas.

## Para montar o grafo manualmente

Se voce for desenhar a rede no relatorio, a melhor ferramenta e o [diagrams.net](https://www.diagrams.net/).

Motivos:

- e gratuito;
- permite organizar os nos manualmente;
- exporta para PNG, PDF e SVG;
- funciona bem para diagramas tecnicos com setas e caixas.

## Observacao importante

O script nao gera mais imagem automaticamente. O grafo deve ser montado manualmente com base em `RELACOES_CAUSAIS` e na separacao `0/1/2` definida em `NIVEIS_VARIAVEIS`.

O arquivo CSV precisa permanecer na mesma pasta do script para que o carregamento funcione apenas com o nome do arquivo.