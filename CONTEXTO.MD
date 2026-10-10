# CONTEXTO DO PROJETO — Dashboard de Faturamento por Laboratório

> Documento único do projeto. Reúne objetivo, dados, regras de cálculo, arquitetura, publicação, manutenção, histórico e pendências.
> Quem for mexer no projeto (pessoa ou IA) deve ler este arquivo antes.

---

## 1. Visão geral

| Item | Valor |
|---|---|
| **O que é** | Dashboard web da evolução do faturamento por laboratório (indústria), mês a mês e ano a ano |
| **Site publicado** | https://diegosimioni2026.github.io/FaturamentoMensal/ |
| **Repositório** | https://github.com/diegosimioni2026/FaturamentoMensal (branch `main`) |
| **Pasta local** | `C:\Users\diego\OneDrive\Documentos\AULA IA` |
| **Fonte dos dados** | Planilha Excel em `dados/` (`01. FATURAMENTO MÊS A MES.xlsx`) |
| **Público** | Gestão comercial |
| **Idioma** | Português (Brasil), valores em `R$ 1.234,56` |
| **Origem** | Projeto de aula ("AULA IA"). Pedido inicial: *"quero um dashboard dessa planilha mostrando as evoluções por laboratórios"* |

### 1.1 Objetivo

Mostrar, sem precisar de explicação:

- quem mais fatura e quanto representa do total;
- **quem mais cresce e quem mais cai**, em R$ e em %;
- picos e quedas ao longo do ano;
- como o ano atual se compara com o anterior;
- problemas na planilha (meses incompletos, linhas inválidas).

---

## 2. Estrutura de arquivos

```
AULA IA/
├── index.html                      ← dashboard final (GERADO, não editar)
├── atualizar.bat                   ← clique duplo: gera o dashboard e publica
├── README.md                       ← instruções curtas de uso
├── CONTEXTO.MD                     ← este documento
├── SPRINTS.md                      ← planejamento de execução (sprints)
├── .gitignore / .gitattributes
├── dados/
│   └── 01. FATURAMENTO MÊS A MES.xlsx   ← planilha de origem (a única .xlsx)
└── ferramentas/
    ├── gerar_dashboard.py          ← lê a planilha, limpa e monta o index.html
    ├── template.html               ← layout, estilo e lógica do dashboard (sem dados)
    └── vendor/
        └── chart.umd.min.js        ← Chart.js 4.4.1 (embutido no index.html)
```

| Arquivo | Quando editar |
|---|---|
| `dados/*.xlsx` | Sempre que os números mudarem |
| `ferramentas/template.html` | Para mudar visual, textos, gráficos ou cálculos do dashboard |
| `ferramentas/gerar_dashboard.py` | Para mudar como a planilha é lida ou limpa |
| `index.html` | **Nunca à mão.** É sobrescrito a cada geração |
| `atualizar.bat` | Raramente (fluxo de publicação) |

### 2.1 Fora do Git (ficam só no computador)

O `.gitignore` exclui: `*.exe`, `*.dll`, `*.zip`, `*.iso`, `MinGit/`, `PortableGit/`, `~$*` (arquivo temporário do Excel aberto), `__pycache__/`, `.vscode/` e `.idea/`.
Os instaladores (`MinGit.zip`, `PortableGit.exe`, `python_installer.exe`) continuam na pasta local, mas não vão para o GitHub.

---

## 3. Arquitetura e fluxo

```
 dados/*.xlsx ──► ferramentas/gerar_dashboard.py ──► index.html ──► git push ──► GitHub Pages
                         ▲            ▲
        ferramentas/template.html   ferramentas/vendor/chart.umd.min.js
```

1. O `gerar_dashboard.py` abre o `.xlsx` como ZIP/XML, **só com a biblioteca padrão do Python** (sem openpyxl ou pandas).
2. O script lê as abas de dados, limpa e agrega os valores e gera a lista de avisos.
3. No `template.html`, ele troca dois marcadores:
   - `/*__CHARTJS__*/` → o código do Chart.js;
   - `/*__DADOS__*/null` → o JSON com os dados.
4. O resultado é gravado no `index.html` da raiz: **um arquivo único**, que funciona offline, sem servidor e sem CDN.
5. O `atualizar.bat` faz `git add -A`, `commit` e `push`. O GitHub Pages publica a raiz da `main` em 1 a 2 minutos.

### 3.1 Requisitos técnicos (decisões fixas)

- **Monolítico:** tudo em um `index.html`, sem nenhuma requisição externa.
- **Sem dependências de build:** só Python 3 (biblioteca padrão) e Git.
- **Tema escuro**, layout responsivo (notebook e celular).
- Arquivos em **UTF-8**. Foi um acento corrompido (`MÃªs`) que quebrou a primeira versão.
- Meses sempre em ordem de calendário.
- Nomes vindos da planilha são inseridos na tela com `textContent` (nunca `innerHTML`).

### 3.2 Formato dos dados embutidos

```json
{
  "geradoEm": "10/10/2026 16:12",
  "fonte": "01. FATURAMENTO MÊS A MES.xlsx",
  "labs": ["3B INDUSTRIA", "ABL", "..."],
  "linhas": [[2024, 1, 0, 1234.56], "..."],
  "avisos": ["Aba \"25. BANCO DE DADOS\", linha 937: ..."]
}
```

Cada item de `linhas` é `[ano, mês (1–12), índice do laboratório em labs, valor]`. A `% Mensal` da planilha **não** é usada: o dashboard recalcula a participação.

---

## 4. Fonte de dados

### 4.1 A planilha

- Fica em `dados/` e deve ser a **única** `.xlsx` da pasta. Se houver zero ou mais de uma, o script para com erro.
- O script lê **toda aba cujo nome segue o padrão `NN. BANCO DE DADOS`**, com `NN` = ano (`24.` = 2024, `25.` = 2025, `26.` = 2026).
- Em cada aba, a **linha 1** precisa ter os cabeçalhos `Empresa`, `Mês` e `Valor`. As colunas são achadas pelo nome, não pela posição.
- Tudo o mais nas abas é ignorado: quadros de resumo, quadrimestre, trimestre, rankings e a coluna `% Mensal`.
- A aba `MÊS ATUAL vs MÊS ANTERIOR` não é lida.

### 4.2 Situação atual dos dados

| Ano | Registros | Laboratórios | Meses | Total |
|---|---|---|---|---|
| 2024 | 864 | 103 | Jan–Dez | R$ 14.587.560,79 |
| 2025 | 1.011 | 120 | Jan–Dez | R$ 15.739.153,32 |
| 2026 | — | — | — | Aba existe, mas é cópia idêntica de 2025, por isso é ignorada |

### 4.3 Limpeza automática

| Situação | O que acontece | Gera aviso? |
|---|---|---|
| Linha totalmente vazia | Descartada | Não |
| Espaços extras, minúsculas (`"Junho "`, `"BIOSINTETICA "`) | Nomes normalizados, em maiúsculas | Não |
| Mês com ou sem acento (`Março`/`MARCO`) | Reconhecido | Não |
| Linha sem nome de laboratório | Descartada | Sim (mostra mês e valor) |
| Mês inválido | Descartada | Sim |
| `Valor` vazio ou não numérico | Descartada | Sim |
| Mesmo laboratório repetido no mesmo mês | Valores **somados** | Sim (quantidade) |
| Aba idêntica à de outro ano | Aba ignorada (os avisos dela também) | Sim |

Os avisos aparecem no terminal ao gerar e no topo do dashboard, numa caixa recolhível chamada **"Avisos da planilha"**.

---

## 5. O dashboard (funcionalidades e regras de cálculo)

### 5.1 Filtros do topo (valem para a página inteira)

- **Ano:** padrão é o mais recente. Trocar o ano recarrega as listas de meses e de laboratórios daquele ano.
- **Mês:** todos ou um.
- **Laboratório:** todos ou um.
- **Limpar:** volta ao ano mais recente, todos os meses e todos os laboratórios.

O **recorte** é o conjunto de registros do ano escolhido, filtrado por mês e laboratório quando houver.

### 5.2 Indicadores (cards)

| Card | Regra |
|---|---|
| **Faturamento total** | Soma do recorte. Compara com o mesmo recorte do ano anterior, usando só os meses que existem no ano atual: ▲/▼ % e o valor do ano anterior |
| **Maior laboratório** | Laboratório de maior soma no recorte, com valor e % do total |
| ↳ com laboratório filtrado | Vira **Participação no mercado**: fatia do laboratório no total do período e posição no ranking |
| **Maior queda de um mês para o seguinte** | Maior redução em R$ entre **meses consecutivos com dados** no ano. Mês sem venda conta como R$ 0. Com mês filtrado, compara aquele mês com o anterior |
| **Média por laboratório** | Total ÷ laboratórios com faturamento no recorte |
| ↳ com laboratório filtrado | Vira **Média mensal**: total ÷ meses com faturamento |

### 5.3 Gráficos

| Gráfico | Comportamento |
|---|---|
| **Evolução mensal** (ano todo) | Linhas dos **8 maiores** laboratórios do recorte no ano. O limite de 8 é o da paleta acessível |
| ↳ com mês filtrado | Barras horizontais: **ranking dos 10 maiores** do mês |
| ↳ com laboratório filtrado | **Uma linha por ano** para aquele laboratório, com o ano selecionado mais grosso |
| **Faturamento total por mês** | Barras do ano escolhido (azul) lado a lado com o ano anterior (cinza). O mês filtrado fica em destaque e os demais esmaecidos. Respeita o filtro de laboratório |
| **Participação** | Rosca com os 5 maiores do recorte mais "Outros (n)" |
| ↳ com laboratório filtrado | O laboratório contra "Demais laboratórios" |

**Regras visuais:**
- Paleta categórica fixa (modo escuro): `#3987e5`, `#d95926`, `#199e70`, `#c98500`, `#d55181`, `#008300`, `#9085e9`, `#e66767`.
- Os 8 maiores laboratórios do ano recebem as cores nessa ordem. **A cor segue o laboratório**, não a posição no gráfico.
- Na rosca, um laboratório fora dos 8 recebe uma cor ainda não usada. Cinza (`#5f5e5a`) é só para "Outros" e "ano anterior".
- Tooltips em R$ completo, eixos abreviados ("R$ 1,2 mi", "R$ 50 mil").

### 5.4 Quem mais cresce (ranking de crescimento)

Tabela que responde **quais indústrias mais crescem (ou mais caem)**. Usa o ano, o mês e o laboratório do topo e tem filtros próprios:

| Filtro | Opções | Regra |
|---|---|---|
| **Comparar com** | Mesmo período do ano anterior *(padrão)* | Ano escolhido contra o ano anterior, nos mesmos meses. Com mês filtrado, só aquele mês |
| | Mês anterior | Mês filtrado (ou o último mês com dados) contra o mês anterior. Janeiro compara com dezembro do ano anterior |
| | 2º semestre vs 1º semestre | Jul–Dez contra Jan–Jun do ano escolhido. Aqui o filtro de mês não se aplica |
| **Mostrar** | Os que mais crescem / Os que mais caem | Variação > 0 ou < 0 |
| **Ordenar por** | R$ / % | Na ordenação por %, laboratórios sem faturamento no período base ("novos") ficam fora, e o rodapé informa quantos são |
| **Porte mínimo** | Todos, R$ 10 mil, **R$ 50 mil** *(padrão)*, R$ 200 mil | Considera o maior faturamento entre os dois períodos. Serve para impedir que laboratórios minúsculos dominem o ranking por % |
| **Quantidade** | 10, 20, 50 | Linhas exibidas |

- **Colunas:** posição, laboratório, valor antes, valor depois, variação em R$ (▲/▼), variação em % ("novo" quando a base é zero) e barra proporcional (azul = cresce, vermelho = cai).
- **Laboratório filtrado no topo:** fica destacado. Se estiver fora do top N, aparece no fim com a posição real.
- **Sem dados para comparar** (ex.: não existe ano anterior): mostra uma mensagem explicando.

### 5.5 Resumo comentado (até 6 cartões)

Considera o ano escolhido e o filtro de laboratório (o filtro de mês é ignorado aqui).

| Cartão | Regra |
|---|---|
| ⚠ **Mês atípico** (amarelo) | Total do mês abaixo de 50% da mediana dos meses do ano (exige 3 meses ou mais). Indica possível planilha incompleta |
| ▼ **Queda** (vermelho) | Último mês com dados menor que o primeiro (com primeiro > 0) |
| ⚠ **Instabilidade** (amarelo) | Último mês 25% ou mais abaixo do pico do ano (pico > R$ 20 mil) |
| ▲ **Destaque** (verde) | Crescimento acima de R$ 50.000 entre o primeiro e o último mês |

Ordem de prioridade: mês atípico, quedas (maiores primeiro), instabilidades e destaques. No máximo 2 de cada tipo antes de completar com os demais.

### 5.6 Tabela detalhada

- Registros do recorte, do maior para o menor, com 15 por página.
- **Colunas:**
  - Laboratório, Mês e Faturamento.
  - **% do mês:** participação no total do mês, considerando todos os laboratórios.
  - **Var. vs mês anterior:** compara com o mês anterior dentro do mesmo ano. Mostra "novo no mês" se o laboratório não vendeu no mês anterior e "-" no primeiro mês do ano.

### 5.7 Outros elementos

- Cabeçalho fixo com a data e a hora da geração dos dados e os anos disponíveis.
- Rodapé com o nome da planilha de origem.

---

## 6. Como usar e manter

### 6.1 Atualizar os dados (rotina)

1. Edite ou substitua a planilha em `dados/`. Ela deve ser a **única** `.xlsx` da pasta. Feche o Excel antes.
2. Dê **dois cliques em `atualizar.bat`**.
3. Leia o resumo na tela (registros e total por ano, mais os avisos).
4. Aguarde 1 a 2 minutos e recarregue o site.

O `.bat` só envia ao GitHub se a geração der certo. Se não houver mudança, ele avisa e não faz commit.

### 6.2 Começar um ano novo (ex.: 2026)

Preencha a aba `26. BANCO DE DADOS` com as colunas `Empresa`, `Mês` e `Valor` (cabeçalho na linha 1). Assim que os dados forem diferentes dos de 2025, o ano aparece sozinho no filtro e vira o padrão.

### 6.3 Alterar o dashboard

1. Edite `ferramentas/template.html` (HTML, CSS e JavaScript ficam juntos nele).
2. Gere localmente com `py ferramentas/gerar_dashboard.py` e abra o `index.html` para conferir.
3. Rode `atualizar.bat` para publicar.

Não remova os marcadores `/*__CHARTJS__*/` e `/*__DADOS__*/null` do template.

### 6.4 Requisitos da máquina

- **Python 3:** o `.bat` usa `py -3` ou, se não houver, `python`. Hoje está instalado o Python 3.11.9, acessível pelo `py`.
- **Git for Windows** em `C:\Program Files\Git`. Ele não está no PATH do `cmd`, então o `.bat` acrescenta `%ProgramFiles%\Git\cmd` automaticamente.
- **Login no GitHub** salvo no Gerenciador de Credenciais do Windows.
- A identidade de commit está configurada **só neste repositório**: `Diego Simioni <diego@simioni.com>`.

### 6.5 Problemas comuns

| Sintoma | Causa provável / solução |
|---|---|
| "a pasta dados/ deve ter exatamente 1 planilha" | Há mais de uma `.xlsx`, ou o Excel está aberto (arquivo `~$...`). Feche o Excel ou remova a sobra |
| "cabeçalho Empresa/Mês/Valor não encontrado" | A linha 1 da aba foi alterada. Restaure os cabeçalhos |
| Ano novo não aparece | O nome da aba fora do padrão `NN. BANCO DE DADOS`, ou a aba é cópia de outro ano |
| Erro no `git push` | Sem internet ou login do GitHub expirado. Rode `git push` de novo e faça login |
| Site não mudou | O Pages leva 1 a 2 minutos. Recarregue com Ctrl+F5 |
| Acentos estranhos (`Ã`) | Algum arquivo foi salvo fora de UTF-8 |

### 6.6 Como foi testado

- O total por ano bate com a soma da coluna `Valor` (2024 também bate com o quadro "24. Resultado" da planilha, menos as 5 linhas sem nome).
- Telas renderizadas no Edge sem janela (headless) nos cenários: padrão, laboratório filtrado (TEUTO), mês filtrado (Junho) e ranking por R$ e por %.
- O site publicado foi conferido após cada envio.

---

## 7. Histórico

| Data | Versão | O que mudou |
|---|---|---|
| 10/10/2026 | `8410cdd`, `8590d7f` | Primeira versão: `index.html` com Tailwind/Chart.js via CDN e dados copiados do `data.js`. Os meses saíam vazios por causa do acento corrompido (`MÃªs`). Instaladores foram versionados por engano |
| 10/10/2026 | `497a114` | Reestruturação: dashboard monolítico e offline, leitura direta da planilha (2024 e 2025), filtro de ano, comparação anual, `atualizar.bat`, README, instaladores fora do Git, `data.js` removido |
| 10/10/2026 | `c226778` | Seção **"Quem mais cresce"** com filtros de comparação, direção, métrica, porte mínimo e quantidade |

### 7.1 Decisões tomadas

- **Python puro no gerador:** evita instalar bibliotecas na máquina da aula.
- **Dados embutidos no HTML:** é o pedido de "HTML único que roda 100% sozinho". O `data.js` separado foi abandonado.
- **Tailwind removido:** o CSS foi escrito à mão, porque o Tailwind exigia CDN.
- **`% Mensal` da planilha ignorada:** é recalculada, porque a planilha tinha valor digitado errado nessa coluna.
- **Duplicados somados**, não descartados.
- **Histórico do Git não reescrito:** os instaladores saíram do repositório, mas continuam no histórico (cerca de 130 MB). Apagar exige force push e só será feito se pedido.

### 7.2 Resultados de referência (2025 contra 2024)

- **Maior crescimento em R$:** FORTLIFE (+R$ 461 mil, +89%), PRUDENCE (+R$ 417 mil, +79%) e BIOSINTETICA (ACHE) (+R$ 355 mil, +37%).
- **Maior crescimento em %** (porte ≥ R$ 50 mil): BLAU e BELLIZ (+11.000%; faturavam cerca de R$ 2,6 mil em 2024) e PHARLAB (+4.094%).
- **Total do ano:** +7,9% (R$ 15,74 mi contra R$ 14,59 mi).

---

## 8. Fora do escopo

- Login, banco de dados ou servidor próprio.
- Edição de dados pelo dashboard.
- Comparação com metas.
- Atualização automática sem rodar o `atualizar.bat`.

---

## 9. Pendências e pontos de atenção

1. **Repositório público:** qualquer pessoa com o link vê a planilha e os valores. Se forem confidenciais, torne o repositório privado. O GitHub Pages em repositório privado exige plano pago.
2. **BIOSINTETICA, dezembro de 2025** (aba `25. BANCO DE DADOS`, linha 937): a coluna `Valor` está vazia e `22,7567` foi digitado na `% Mensal`. Pelo quadro resumo da planilha, o valor correto é cerca de **R$ 292.896,10**. Enquanto não for corrigido, dezembro aparece como queda de 100% para ela.
3. **Junho de 2025:** soma só R$ 270.899,38, contra R$ 0,85 a 1,9 mi nos outros meses. O mês provavelmente está incompleto e distorce quedas e rankings de maio para junho.
4. **2024:** há 5 linhas sem nome de laboratório (linhas 261, 399, 479, 552 e 628; R$ 117,91 no total). Completar ou apagar.
5. **Duplicados:** 10 casos em 2025 e 2 em 2024 (ex.: NATIVITA). Confirmar se são o mesmo laboratório ou se devem ter nomes distintos.
6. **Grupos de laboratórios:** `EMS MARCAS`/`EMS GENERICO`, `EUROFARMA`/`EUROFARMA OTC` e `NOVAQUIMICA`/`NOVA QUIMICA GENERICO` aparecem separados. Falta decidir se devem ser agrupados.
7. **Aba 2026:** hoje é cópia de 2025. Preencher com os dados reais quando houver.
8. **Pasta `PortableGit/` local:** sumiu do computador. Dá para recuperar pelo `PortableGit.exe`, mas não é necessária, porque o Git está instalado em `C:\Program Files\Git`.
