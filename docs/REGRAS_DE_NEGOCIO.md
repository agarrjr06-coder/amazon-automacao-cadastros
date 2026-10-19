# Regras de negócio e cautelas

1. O produto deve ser identificado como **calçado** nas fontes antes de entrar no template SHOES.
2. SKU e códigos relacionados são **texto**, nunca datas ou números a serem formatados automaticamente.
3. Conversões suspeitas de SKU para data exigem cruzamento com outras colunas e preservação do valor bruto.
4. O SKU pai do sistema de origem não comprova a existência de um SKU pai no catálogo Amazon.
5. EAN/GTIN deve ser informado e validado manualmente; nunca reconstruir valores truncados ou em notação científica.
6. Não usar a linha de **exemplos** do template como dado real do produto.
7. Preencher somente atributos sustentados pelas fontes ou por regras de negócio verificadas.
8. Confirmar os valores permitidos no template, inclusive marca, tamanho, tipo de produto e tema de variação.
9. Preservar abas, cabeçalhos, validações, estilos e estrutura do arquivo original; trabalhar sempre em cópias.
10. Nenhum rascunho é considerado apto para publicação sem homologação.

## Campos em revisão
Ação de oferta, tipo de produto, SKU pai Amazon, tema de variação, gênero, faixa etária, sistema de tamanho, mapa de cores e atributos obrigatórios/condicionais.

**Observação:** propostas de preenchimento automático precisam ser validadas contra o template e a fonte efetiva. Não assumir valores por analogia.
