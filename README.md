# Automação de Cadastros Amazon — Calçados

Projeto em Python para apoiar a preparação, o preenchimento e a auditoria de templates Excel de cadastro de **calçados** na Amazon Brasil.

> **Status:** protótipo em homologação. Não publica produtos automaticamente e nenhum rascunho deve ser enviado à Amazon sem conferência.

## Problema
O cadastro manual de variações de calçados exige cruzar dados de diferentes fontes, conferir SKU, atributos, famílias e vocabulários aceitos pelo template, preservando sua estrutura original.

## Solução em desenvolvimento
1. Ler uma lista de SKUs e bases de referência autorizadas.
2. Localizar informações de produtos e classificar os itens elegíveis ao template de calçados.
3. Normalizar identificadores com rastreabilidade, sem conversões arbitrárias.
4. Preencher somente atributos sustentados pelas fontes e regras validadas.
5. Gerar um rascunho `.xlsm` e relatórios de pendências para revisão humana.

## Histórico documentado
- Template SHOES: **304 colunas** na aba Modelo.
- Execução real v7 em 15/10/2026: **21 SKUs solicitados, 19 calçados, 2 retidos**; aviso sobre leitura de fonte Asics.
- A v7 preenchia sete campos por SKU quando disponíveis; a auditoria identificou lacunas adicionais.
- A documentação registra uma v8 de auditoria conservadora, mas o código dessa versão ainda precisa ser incorporado e validado neste repositório.
- EAN/GTIN permanece para preenchimento e validação manual, sem inferências.

## Estrutura
- `src/`: código-fonte (a incorporar após revisão de segurança e dependências).
- `docs/`: contexto, arquitetura, regras e homologação.
- `exemplos/`: somente exemplos sintéticos, sem dados operacionais.
- `testes/`: testes automatizados a acrescentar.
- `requirements.txt`: dependências conhecidas do ambiente.
- `.gitignore`: proteção básica contra inclusão acidental de arquivos internos.

## Segurança e limites
Este repositório é público. Não inclua bases da empresa, planilhas de clientes, caminhos internos, identificadores comerciais, credenciais, arquivos de produção ou templates de distribuição restrita. Exemplos devem ser fictícios. A saída gerada não é homologação nem publicação automática.

## Fontes de referência
Documentação privada do projeto mantida no Google Drive do responsável. Os scripts originais e arquivos reais devem permanecer em ambiente autorizado até a revisão de confidencialidade.

## Próximos passos
- Auditar o código existente e suas dependências.
- Incorporar versão segura e executável dos scripts.
- Cobrir atributos obrigatórios e condicionais sem copiar a linha de exemplos do template.
- Validar regras de variação e relacionamento pai-filho.
- Adicionar testes com dados sintéticos e preservar formatação do Excel.
