"""Pipeline demonstrativo com dados sintéticos. Não publica na Amazon."""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

from src.regras_cadastros import triar_produto, atributos_propostos
from src.gerador_template import gerar_rascunho


def processar(entrada: Path, template: Path, destino: Path, relatorio: Path) -> dict:
    if not entrada.is_file() or not template.is_file():
        raise FileNotFoundError("Informe arquivos de entrada e template existentes")
    if entrada.resolve() == destino.resolve() or template.resolve() == destino.resolve():
        raise ValueError("A saída não pode sobrescrever entradas")
    with entrada.open(encoding="utf-8-sig", newline="") as f:
        leitor = csv.DictReader(f, delimiter=";")
        exigidos = {"sku", "categoria", "marca", "nome", "cor", "tamanho"}
        if not leitor.fieldnames or not exigidos.issubset(set(leitor.fieldnames)):
            raise ValueError("CSV sem colunas necessárias: " + ", ".join(sorted(exigidos)))
        produtos = list(leitor)
    if not produtos:
        raise ValueError("Lista de produtos vazia")
    auditoria = []
    aprovados = []
    vistos = set()
    for produto in produtos:
        sku = produto["sku"].strip()
        resultado = triar_produto(sku, produto["categoria"])
        pendencias = []
        if resultado.status != "ELEGIVEL_PARA_CONFERENCIA":
            pendencias.append(resultado.status)
        if sku in vistos:
            pendencias.append("SKU_DUPLICADO")
        vistos.add(sku)
        for campo in ("marca", "nome", "cor", "tamanho"):
            if not produto.get(campo, "").strip():
                pendencias.append("AUSENTE_" + campo.upper())
        # Identificadores de produto e variações não são inferidos.
        pendencias.extend(["EAN_REQUER_CONFERENCIA", "VARIACAO_REQUER_CONFERENCIA"])
        elegivel = resultado.status == "ELEGIVEL_PARA_CONFERENCIA" and not any(
            p.startswith("AUSENTE_") or p == "SKU_DUPLICADO" for p in pendencias
        )
        auditoria.append({"sku": sku, "status": "RASCUNHO" if elegivel else "RETIDO",
                          "pendencias": "|".join(pendencias)})
        if elegivel:
            aprovados.append(atributos_propostos(produto))
    # Falha de template impede a geração do relatório de sucesso.
    gerado = gerar_rascunho(template, destino, aprovados) if aprovados else None
    relatorio.parent.mkdir(parents=True, exist_ok=True)
    with relatorio.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, delimiter=";", fieldnames=["sku", "status", "pendencias"])
        w.writeheader()
        w.writerows(auditoria)
    return {"solicitados": len(produtos), "rascunhos": len(aprovados),
            "retidos": len(produtos) - len(aprovados),
            "saida": str(destino) if gerado else None, "relatorio": str(relatorio)}


def main():
    parser = argparse.ArgumentParser(description="Demonstração de triagem de calçados")
    parser.add_argument("--entrada", type=Path, required=True)
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--saida", type=Path, required=True)
    parser.add_argument("--relatorio", type=Path, required=True)
    a = parser.parse_args()
    print(json.dumps(processar(a.entrada, a.template, a.saida, a.relatorio),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
