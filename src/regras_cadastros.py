#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regras reutilizáveis de triagem para calçados. Sem acesso a rede ou publicação."""
from __future__ import annotations
import re
import unicodedata
from dataclasses import dataclass


def normalizar_texto(valor: object) -> str:
    texto = unicodedata.normalize("NFKD", str(valor or ""))
    return "".join(c for c in texto if not unicodedata.combining(c)).strip().lower()


def sku_como_texto(valor: object) -> str:
    return str(valor or "").strip().upper().replace("–", "-").replace("—", "-")


def sku_pai_interno(sku: str) -> str:
    """Extrai quatro dígitos iniciais, sem afirmar vínculo com SKU pai Amazon."""
    encontrado = re.match(r"^(\d{4})", sku_como_texto(sku))
    return encontrado.group(1) if encontrado else ""


def recuperar_sku_convertido_em_data(valor: str, pai: str) -> tuple[str, str]:
    """Sugere recuperação somente quando o 'ano' da data coincide com o pai.
    A decisão ainda requer conferência cruzada com a fonte original.
    """
    bruto = sku_como_texto(valor)
    pai = sku_como_texto(pai)
    encontrado = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", bruto)
    if not encontrado or encontrado.group(3) != pai:
        return bruto, "ORIGINAL"
    dia, mes = int(encontrado.group(1)), int(encontrado.group(2))
    if not 1 <= dia <= 31 or not 1 <= mes <= 12:
        return bruto, "ORIGINAL"
    return f"{pai}-{mes:02d}-{dia:02d}", "SUGESTAO_REQUER_CONFERENCIA"


def validar_ean(valor: str) -> tuple[str, str]:
    bruto = sku_como_texto(valor)
    if not bruto:
        return "", "AUSENTE"
    if re.search(r"[Ee][+-]?\d+", bruto) or "," in bruto:
        return "", "NOTACAO_CIENTIFICA_OU_DECIMAL"
    limpo = re.sub(r"[\s.\-]", "", bruto)
    if not limpo.isdigit() or len(limpo) not in (8, 12, 13, 14):
        return "", "FORMATO_INVALIDO"
    digitos = [int(c) for c in limpo]
    soma = sum(n * (3 if i % 2 == 0 else 1)
               for i, n in enumerate(reversed(digitos[:-1])))
    if (10 - soma % 10) % 10 != digitos[-1]:
        return "", "DIGITO_VERIFICADOR_INVALIDO"
    return limpo, "VALIDO"


def classificar_categoria(valor: str) -> str:
    """Não deduz categoria a partir do título do produto."""
    categoria = normalizar_texto(valor)
    if categoria in {"calcados", "calcado", "shoes"}:
        return "CALCADOS"
    if not categoria:
        return "INDEFINIDA"
    return "OUTRA_CATEGORIA"


@dataclass(frozen=True)
class ResultadoTriagem:
    sku: str
    sku_pai_interno: str
    categoria: str
    status: str


def triar_produto(sku: str, categoria: str) -> ResultadoTriagem:
    sku_limpo = sku_como_texto(sku)
    pai = sku_pai_interno(sku_limpo)
    classe = classificar_categoria(categoria)
    if not pai:
        status = "SKU_PAI_INVALIDO"
    elif classe == "CALCADOS":
        status = "ELEGIVEL_PARA_CONFERENCIA"
    elif classe == "INDEFINIDA":
        status = "CATEGORIA_NAO_INFORMADA"
    else:
        status = "CATEGORIA_RETIDA"
    return ResultadoTriagem(sku_limpo, pai, classe, status)


def atributos_propostos(dados: dict[str, str]) -> dict[str, str]:
    """Retorna apenas valores de origem; não preenche exemplos ou campos não confirmados."""
    mapa = {
        "SKU": "sku",
        "Nome da marca": "marca",
        "Nome do item": "nome",
        "Número do modelo": "modelo",
        "Descrição do Produto": "descricao",
        "Cor": "cor",
        "Tamanho do calçado": "tamanho",
    }
    return {campo: str(dados[origem]).strip()
            for campo, origem in mapa.items()
            if dados.get(origem) is not None and str(dados[origem]).strip()}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Triagem de calçados, sem publicação Amazon")
    parser.add_argument("--sku", required=True)
    parser.add_argument("--categoria", required=True)
    args = parser.parse_args()
    print(triar_produto(args.sku, args.categoria))
