# Análise LHE no CERN SWAN

Este repositório é um exemplo público de análise de eventos em nível de gerador
para o canal `pp → H → γγ`, comparado ao fundo contínuo `pp → γγ` sem Higgs.
Ele foi preparado a partir do template FIS01214 e contém um notebook integrado
 com `pandas.DataFrame`.

Há duas versões do notebook:

- `notebooks/analise-consolidada-dataframe.ipynb`: referência completa, com código;
- `notebooks/analise-consolidada-dataframe-estudante.ipynb`: roteiro para o aluno, cujas células analíticas devem ser preenchidas com código solicitado a um agente.

## Execução no CERN SWAN

1. Na interface do SWAN, use a opção de clonar um repositório Git e informe a
   URL HTTPS `https://github.com/FIS01214/analise-swan.git`.
2. Abra `notebooks/analise-consolidada-dataframe.ipynb` a partir do clone.
3. Execute a primeira célula específica do SWAN. Ela verifica `numpy`, `pandas`,
   `matplotlib` e `IPython` e tenta instalar apenas o que estiver ausente. Se a
   política do serviço bloquear a instalação, use o ambiente/projeto autorizado
   e execute a célula novamente.
4. Execute as demais células na ordem. Os caminhos esperados apontam para
   `../data/` a partir da pasta `notebooks/`.

O notebook de referência cobre leitura tabular, seleção, cutflow, massas
invariantes, emulação paramétrica de eficiência em função de `pT` e `eta`,
turn-on curve, normalização e estimativa simplificada de seção de choque.

A seleção deste exemplo exige dois fótons no estado final e reconstrói a massa
invariante \(m_{\gamma\gamma}\) do canal \(H\to\gamma\gamma\).

## Física e limitações

Os arquivos `sinal.lhe.gz` e `fundo.lhe.gz` correspondem a `pp → H → γγ` e ao
contínuo `pp → γγ` sem Higgs. O pico de massa invariante dos fótons ilustra a
assinatura do Higgs. A Parte 2 acrescenta uma resposta detectora paramétrica e
aleatória, dependente de `pT` e `eta`, apenas para fins didáticos. Ela não
substitui reconstrução, resolução, trigger, pileup ou calibrações reais do CMS;
a estimativa de seção de choque depende das hipóteses de aceitação, eficiência e
luminosidade.
