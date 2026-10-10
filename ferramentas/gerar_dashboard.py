"""Gera o index.html (dashboard monolítico) a partir da planilha em dados/.

Uso:  py ferramentas/gerar_dashboard.py

- Lê toda aba chamada "NN. BANCO DE DADOS" (NN = ano, ex.: "25." = 2025),
  usando as colunas Empresa / Mês / Valor da tabela que começa na linha 1.
- Limpa os dados (linhas vazias, espaços, duplicados, valores inválidos).
- Junta template.html + Chart.js + dados em um único index.html na raiz.

Só usa a biblioteca padrão do Python: não precisa instalar nada.
"""

import datetime
import glob
import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_DADOS = os.path.join(RAIZ, "dados")
TEMPLATE = os.path.join(RAIZ, "ferramentas", "template.html")
CHARTJS = os.path.join(RAIZ, "ferramentas", "vendor", "chart.umd.min.js")
SAIDA = os.path.join(RAIZ, "index.html")

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
NS_REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
NS_PKG = "{http://schemas.openxmlformats.org/package/2006/relationships}"

ABA_DADOS = re.compile(r"^\s*(\d{2})\.\s*BANCO DE DADOS\s*$", re.IGNORECASE)
MESES = ["JANEIRO", "FEVEREIRO", "MARCO", "ABRIL", "MAIO", "JUNHO", "JULHO",
         "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def limpar_nome(texto):
    return re.sub(r"\s+", " ", str(texto)).strip().upper()


def reais(valor):
    return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def coluna_e_linha(ref):
    m = re.match(r"([A-Z]+)(\d+)", ref)
    col = 0
    for letra in m.group(1):
        col = col * 26 + ord(letra) - 64
    return col, int(m.group(2))


def ler_planilha(caminho):
    """Devolve {nome_da_aba: {linha: {coluna: valor}}} só das abas de dados."""
    z = zipfile.ZipFile(caminho)
    textos = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(NS + "si"):
            textos.append("".join(t.text or "" for t in si.iter(NS + "t")))

    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).iter(NS_PKG + "Relationship")}
    abas = {}
    for aba in ET.fromstring(z.read("xl/workbook.xml")).iter(NS + "sheet"):
        nome = aba.get("name")
        if not ABA_DADOS.match(nome):
            continue
        alvo = rels[aba.get(NS_REL + "id")].lstrip("/")
        arquivo = alvo if alvo.startswith("xl/") else "xl/" + alvo
        grade = {}
        for c in ET.fromstring(z.read(arquivo)).iter(NS + "c"):
            v = c.find(NS + "v")
            tipo = c.get("t")
            if tipo == "inlineStr":
                valor = "".join(t.text or "" for t in c.iter(NS + "t"))
            elif v is None:
                continue
            elif tipo == "s":
                valor = textos[int(v.text)]
            elif tipo in ("str", "e", "b"):
                valor = v.text
            else:
                valor = float(v.text)
            col, lin = coluna_e_linha(c.get("r"))
            grade.setdefault(lin, {})[col] = valor
        abas[nome] = grade
    return abas


def extrair_registros(nome_aba, grade, avisos):
    """Lê a tabela Empresa/Mês/Valor da aba e devolve {(mes, empresa): valor}."""
    cabecalho = {sem_acento(str(v)).strip().upper(): c for c, v in grade.get(1, {}).items()}
    try:
        c_emp, c_mes, c_val = cabecalho["EMPRESA"], cabecalho["MES"], cabecalho["VALOR"]
    except KeyError:
        avisos.append(f'Aba "{nome_aba}": cabeçalho Empresa/Mês/Valor não encontrado na linha 1. Aba ignorada.')
        return {}

    registros, duplicados = {}, 0
    for lin in sorted(grade):
        if lin == 1:
            continue
        linha = grade[lin]
        empresa, mes, valor = linha.get(c_emp), linha.get(c_mes), linha.get(c_val)
        if empresa in (None, "") and mes in (None, "") and valor in (None, ""):
            continue
        empresa = limpar_nome(empresa or "")
        mes_txt = sem_acento(str(mes or "")).strip().upper()
        if not empresa:
            detalhe = f" ({mes}, {reais(valor)})" if isinstance(valor, float) else ""
            avisos.append(f'Aba "{nome_aba}", linha {lin}: sem nome de laboratório{detalhe}. Linha ignorada.')
            continue
        if mes_txt not in MESES:
            avisos.append(f'Aba "{nome_aba}", linha {lin}: mês inválido ({mes!r}) para {empresa}. Linha ignorada.')
            continue
        if not isinstance(valor, float):
            avisos.append(f'Aba "{nome_aba}", linha {lin}: {empresa} em {mes_txt.title()} está sem valor numérico na coluna Valor. Linha ignorada.')
            continue
        chave = (MESES.index(mes_txt) + 1, empresa)
        if chave in registros:
            duplicados += 1
        registros[chave] = registros.get(chave, 0.0) + valor
    if duplicados:
        avisos.append(f'Aba "{nome_aba}": {duplicados} laboratório(s) repetido(s) no mesmo mês. Os valores foram somados.')
    return registros


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    planilhas = sorted(p for p in glob.glob(os.path.join(PASTA_DADOS, "*.xlsx")) if not os.path.basename(p).startswith("~$"))
    if len(planilhas) != 1:
        sys.exit(f"ERRO: a pasta dados/ deve ter exatamente 1 planilha .xlsx (encontradas: {len(planilhas)}).")
    planilha = planilhas[0]
    print(f"Lendo {os.path.relpath(planilha, RAIZ)} ...")

    avisos = []
    por_ano = {}
    abas = ler_planilha(planilha)
    for nome in sorted(abas, key=lambda n: ABA_DADOS.match(n).group(1)):
        ano = 2000 + int(ABA_DADOS.match(nome).group(1))
        avisos_aba = []
        registros = extrair_registros(nome, abas[nome], avisos_aba)
        copia_de = next((a for a, r in por_ano.items() if r == registros), None)
        if copia_de:
            avisos.append(f'Aba "{nome}" é uma cópia idêntica dos dados de {copia_de}. Ignorada até receber os dados de {ano}.')
            continue
        avisos.extend(avisos_aba)
        if registros:
            por_ano[ano] = registros
    if not por_ano:
        sys.exit('ERRO: nenhuma aba "NN. BANCO DE DADOS" com dados válidos.')

    labs = sorted({emp for regs in por_ano.values() for (_, emp) in regs})
    indice = {emp: i for i, emp in enumerate(labs)}
    linhas = [[ano, mes, indice[emp], round(valor, 2)]
              for ano in sorted(por_ano)
              for (mes, emp), valor in sorted(por_ano[ano].items())]

    dados = {
        "geradoEm": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "fonte": os.path.basename(planilha),
        "labs": labs,
        "linhas": linhas,
        "avisos": avisos,
    }
    json_dados = json.dumps(dados, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    with open(TEMPLATE, encoding="utf-8") as f:
        html = f.read()
    with open(CHARTJS, encoding="utf-8") as f:
        chartjs = f.read()
    for marcador in ("/*__CHARTJS__*/", "/*__DADOS__*/null"):
        if html.count(marcador) != 1:
            sys.exit(f"ERRO: o template deve ter exatamente 1 marcador {marcador}.")
    html = html.replace("/*__CHARTJS__*/", chartjs).replace("/*__DADOS__*/null", json_dados)
    with open(SAIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)

    print()
    for ano in sorted(por_ano):
        regs = por_ano[ano]
        meses = sorted({m for (m, _) in regs})
        total = sum(regs.values())
        print(f"  {ano}: {len(regs)} registros, {len({e for (_, e) in regs})} laboratórios, "
              f"meses {meses[0]} a {meses[-1]}, total {reais(total)}")
    if avisos:
        print("\nAvisos (corrija na planilha se necessário):")
        for a in avisos:
            print("  - " + a)
    print(f"\nOK: index.html gerado ({os.path.getsize(SAIDA) // 1024} KB).")


if __name__ == "__main__":
    main()
