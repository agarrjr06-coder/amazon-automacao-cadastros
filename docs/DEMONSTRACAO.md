# Demonstração integrada (sem dados operacionais)

O módulo `src/pipeline.py` lê um CSV separado por ponto e vírgula, valida a categoria e campos mínimos, gera um rascunho a partir de um **template limpo fornecido pelo usuário** e registra pendências em CSV.

O arquivo `exemplos/produtos_ficticios.csv` contém dados inteiramente inventados.

## Execução

Instale a dependência necessária para os testes:

```bash
python -m pip install openpyxl==3.1.5
python -m unittest discover -s testes -v
```

Com um template autorizado, que tenha aba `Modelo` e cabeçalhos na linha 4:

```bash
python -m src.pipeline --entrada exemplos/produtos_ficticios.csv --template caminho/SHOES.xlsm --saida saida/rascunho.xlsm --relatorio saida/auditoria.csv
```

**Limites:** o exemplo não consulta bases internas, não resolve EAN, não cria relacionamentos pai-filho Amazon, não valida todos os atributos condicionais e não publica anúncios. É uma demonstração de integração, não um arquivo pronto para upload.

A validação com o template real e as bases autorizadas ainda é necessária.
