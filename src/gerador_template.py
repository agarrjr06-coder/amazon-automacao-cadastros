"""Gera rascunho de calçados em XLSM preservando as partes do arquivo original."""
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
q = lambda tag: "{" + MAIN + "}" + tag


def coluna(numero):
    resultado = ""
    while numero:
        numero, resto = divmod(numero - 1, 26)
        resultado = chr(65 + resto) + resultado
    return resultado


def numero_coluna(letras):
    numero = 0
    for letra in letras:
        numero = numero * 26 + ord(letra) - 64
    return numero


def _valor(celula, compartilhadas):
    if celula.get("t") == "inlineStr":
        return "".join(t.text or "" for t in celula.iter(q("t")))
    v = celula.find(q("v"))
    if v is None:
        return ""
    return compartilhadas[int(v.text)] if celula.get("t") == "s" else (v.text or "")


def gerar_rascunho(template, destino, registros):
    """Registros: lista de dicionários {nome visível do campo: valor validado}."""
    import posixpath
    template, destino = Path(template), Path(destino)
    if template.resolve() == destino.resolve():
        raise ValueError("Nunca sobrescrever o template original")
    if not registros:
        raise ValueError("Nenhum registro fornecido")

    with zipfile.ZipFile(template) as zin:
        workbook = ET.fromstring(zin.read("xl/workbook.xml"))
        relations = ET.fromstring(zin.read("xl/_rels/workbook.xml.rels"))
        relmap = {r.get("Id"): r.get("Target") for r in relations.findall("{" + PKG + "}Relationship")}
        aba = next((s for s in workbook.find(q("sheets")) if s.get("name") == "Modelo"), None)
        if aba is None:
            raise ValueError("Aba Modelo não encontrada")
        target = relmap[aba.get("{" + REL + "}id")]
        target = posixpath.normpath(target.lstrip("/") if target.startswith("/") else "xl/" + target)
        xml = zin.read(target)
        root = ET.fromstring(xml)
        linhas = {int(r.get("r")): r for r in root.findall(".//" + q("sheetData") + "/" + q("row"))}
        if any(numero >= 7 for numero in linhas):
            raise ValueError("Template contém registros a partir da linha 7; use uma cópia limpa")
        if 4 not in linhas:
            raise ValueError("Cabeçalhos da linha 4 não encontrados")

        compartilhadas = []
        if "xl/sharedStrings.xml" in zin.namelist():
            ss = ET.fromstring(zin.read("xl/sharedStrings.xml"))
            compartilhadas = ["".join(t.text or "" for t in si.iter(q("t"))) for si in ss.findall(q("si"))]
        titulos = {}
        for celula in linhas[4].findall(q("c")):
            rotulo = _valor(celula, compartilhadas).strip().casefold()
            if rotulo:
                titulos.setdefault(rotulo, numero_coluna(re.match(r"[A-Z]+", celula.get("r")).group()))
        estilos = {}
        for linha in (6, 5):
            if linha in linhas:
                for celula in linhas[linha].findall(q("c")):
                    indice = numero_coluna(re.match(r"[A-Z]+", celula.get("r")).group())
                    if celula.get("s") is not None:
                        estilos.setdefault(indice, celula.get("s"))
        novas_linhas = []
        total = 0
        for linha, registro in enumerate(registros, 7):
            celulas = []
            for rotulo, valor in registro.items():
                if valor is None or not str(valor).strip():
                    continue
                indice = titulos.get(rotulo.strip().casefold())
                if indice is None:
                    raise ValueError("Campo não encontrado no template: " + rotulo)
                estilo = ' s="' + estilos[indice] + '"' if indice in estilos else ""
                conteudo = escape(str(valor), {'"': '&quot;', "'": '&apos;'})
                celulas.append((indice, f'<c r="{coluna(indice)}{linha}"{estilo} t="inlineStr"><is><t>{conteudo}</t></is></c>'))
                total += 1
            novas_linhas.append(f'<row r="{linha}">' + "".join(c for _, c in sorted(celulas)) + "</row>")
        if xml.count(b"</sheetData>") != 1:
            raise ValueError("Estrutura XML inesperada")
        modificado = xml.replace(b"</sheetData>", "".join(novas_linhas).encode("utf-8") + b"</sheetData>", 1)
        def dimensao(match):
            ultima_coluna = re.findall(r"[A-Z]+", match.group(1).decode())[-1]
            return f'<dimension ref="A1:{ultima_coluna}{6 + len(registros)}"'.encode()
        modificado = re.sub(rb'<dimension ref="([A-Z0-9:]+)"', dimensao, modificado, count=1)
        destino.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(destino, "w") as zout:
            for parte in zin.infolist():
                zout.writestr(parte, modificado if parte.filename == target else zin.read(parte.filename))
    return {"registros": len(registros), "celulas_preenchidas": total, "arquivo": str(destino)}
