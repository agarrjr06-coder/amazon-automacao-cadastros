# Arquitetura — situação documentada

## Fluxo confirmado
Lista de SKUs → leitura de bases autorizadas → triagem de categoria → preenchimento conservador do template SHOES → relatórios de homologação → conferência humana.

## Implementação histórica
A v7 usa dependências das versões v6, v4 e v3. O fluxo registrado utiliza planilhas Excel e arquivos de referência locais. **Não há confirmação de uso da SP-API nem publicação automática.**

## Artefatos da v7
- TRIAGEM_SHOES_v7.csv
- ATRIBUTOS_PREENCHIDOS.csv
- CHECKLIST_HOMOLOGACAO.csv
- PROPOSTA_FAMILIAS.csv
- FONTES_PROCESSADAS.csv
- ERROS_LEITURA.csv
- RASCUNHO_SHOES_V7_*.xlsm

Os arquivos de saída não são publicados neste repositório.

## Evolução
A documentação do projeto registra a v8 como camada de auditoria adicional, incluindo ação de oferta, tipo de produto, variações e vocabulário de atributos. O código correspondente precisa ser verificado antes de sua incorporação.
