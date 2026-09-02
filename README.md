# Análise LHE no CERN SWAN

Este repositório é um exemplo público de análise de eventos em nível de gerador
para o canal `pp → H → γγ`, comparado ao fundo contínuo `pp → γγ` sem Higgs.
Ele foi preparado a partir do template FIS01214 e contém um notebook integrado
com `pandas.DataFrame`.

## Execução

Abra `notebooks/analise-consolidada-dataframe.ipynb` em um kernel Python do CERN
SWAN. Faça upload do notebook e do ZIP deste repositório, descompacte o ZIP e
confirme `data/sinal.lhe.gz` e `data/fundo.lhe.gz`. A primeira célula específica
do SWAN verifica `numpy`, `pandas`, `matplotlib` e `IPython`; se algum pacote
estiver ausente, tenta instalá-lo no kernel atual. Se a política do serviço
bloquear a instalação, instale os pacotes no projeto/ambiente autorizado e
execute novamente a célula.

Depois, execute as células na ordem para ver a leitura, seleção, cutflow, massas
invariantes, normalização e estimativa simplificada de seção de choque.

## Física e limitações

Os eventos são simulados no nível de gerador. O pico de massa invariante dos
fótons ilustra a assinatura do Higgs, mas não representa uma medida experimental
com detector real: não há reconstrução, resolução, trigger, pileup ou
calibração. Os resultados servem como demonstração didática reproduzível.
