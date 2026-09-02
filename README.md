# Análise LHE no CERN SWAN

Este repositório é um exemplo público de análise de eventos em nível de gerador
para o canal `pp → H → γγ`, comparado ao fundo contínuo `pp → γγ` sem Higgs.
Ele foi preparado a partir do template FIS01214 e contém um notebook integrado
com `pandas.DataFrame`.

## Execução no CERN SWAN

1. No GitHub, use **Code → Download ZIP** para baixar este repositório e baixe
   também `notebooks/analise-consolidada-dataframe.ipynb`.
2. Abra o notebook no SWAN e envie o `.ipynb` e o ZIP para o mesmo ambiente de
   arquivos. O ZIP é o arquivo de dados da análise.
3. Na seção `0. Preparação no Google Colab` (o título é mantido para tornar o
   fluxo compatível com os notebooks do curso), peça ao agente para localizar e
   descompactar o ZIP, entrar na pasta extraída e inflar
   `data/sinal.lhe.gz` e `data/fundo.lhe.gz` com `gzip`, sem apagar os `.gz`.
4. Execute a primeira célula específica do SWAN. Ela verifica `numpy`, `pandas`,
   `matplotlib` e `IPython` e tenta instalar apenas o que estiver ausente. Se a
   política do serviço bloquear a instalação, use o ambiente/projeto autorizado
   e execute a célula novamente.
5. Execute as demais células na ordem. Os caminhos esperados apontam para
   `../data/` a partir da pasta `notebooks/`.

O notebook cobre leitura tabular, seleção, cutflow, massas invariantes,
normalização e estimativa simplificada de seção de choque.

## Física e limitações

Os arquivos `sinal.lhe.gz` e `fundo.lhe.gz` correspondem a `pp → H → γγ` e ao
contínuo `pp → γγ` sem Higgs. O pico de massa invariante dos fótons ilustra a
assinatura do Higgs. Como são eventos no nível de gerador, não há reconstrução,
resolução de detector, trigger, pileup ou calibração; a estimativa de seção de
choque é, portanto, didática e depende das hipóteses de aceitação, eficiência e
luminosidade.
