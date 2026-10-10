# Contexto do Projeto — Dashboard de Faturamento por Laboratório

## 1. Objetivo

Criar um dashboard web a partir da planilha de faturamento que mostre a **evolução do faturamento de cada laboratório mês a mês e ano a ano**, permitindo identificar rapidamente:

- quem mais fatura e quanto representa do total;
- quem está crescendo e quem está caindo;
- variações bruscas (picos e quedas) ao longo do ano;
- como o ano atual se compara com o anterior.

**Site publicado:** https://diegosimioni2026.github.io/FaturamentoMensal/
**Repositório:** https://github.com/diegosimioni2026/FaturamentoMensal

## 2. Público

Gestão comercial. O dashboard deve ser entendido sem explicação: números em reais, textos em português, leitura direta.

## 3. Estrutura do projeto

| Caminho | O que é | Editar? |
|---|---|---|
| `index.html` | O dashboard pronto: **um arquivo único** com HTML, CSS, Chart.js e os dados embutidos. É o que o GitHub Pages publica. | **Não.** É gerado automaticamente. |
| `dados/*.xlsx` | A planilha de origem (deve haver só uma). | Sim, é aqui que os dados mudam. |
| `atualizar.bat` | Clique duplo: gera o `index.html` a partir da planilha e envia ao GitHub. | Raramente. |
| `ferramentas/gerar_dashboard.py` | Lê a planilha, limpa os dados e monta o `index.html`. Só usa Python puro (nada para instalar). | Para mudar regras de leitura/limpeza. |
| `ferramentas/template.html` | Layout, estilo e lógica do dashboard (sem os dados). | Para mudar o visual ou os cálculos. |
| `ferramentas/vendor/chart.umd.min.js` | Chart.js 4.4.1, embutido no `index.html` para funcionar sem internet. | Não. |

## 4. Fonte de dados

- **Arquivo:** a planilha em `dados/` (hoje `01. FATURAMENTO MÊS A MES.xlsx`).
- **Abas lidas:** toda aba chamada `NN. BANCO DE DADOS`, onde `NN` é o ano (`24.` = 2024, `25.` = 2025, `26.` = 2026). Um ano novo entra no dashboard sozinho quando a aba dele tiver dados.
- **Colunas lidas** (cabeçalho na linha 1 da aba): `Empresa`, `Mês`, `Valor`. As demais colunas e quadros da aba (resumos, rankings) são ignorados. A `% Mensal` é recalculada pelo dashboard.
- **Situação atual:**
  - 2024: 864 registros, 103 laboratórios, R$ 14,59 milhões.
  - 2025: 1.011 registros, 120 laboratórios, R$ 15,74 milhões.
  - 2026: a aba existe, mas é uma cópia idêntica de 2025, por isso é ignorada até receber os dados reais.

### Limpeza feita automaticamente na leitura

1. Linhas vazias são descartadas.
2. Espaços extras são removidos e os nomes ficam em maiúsculas (`"Junho "` → `Junho`, `"BIOSINTETICA "` → `BIOSINTETICA`).
3. Linhas sem nome de laboratório, com mês inválido ou sem valor numérico são descartadas **e listadas em "Avisos da planilha"** no topo do dashboard.
4. O mesmo laboratório repetido no mesmo mês tem os valores **somados**.
5. Uma aba que é cópia idêntica de outro ano é ignorada.

## 5. Escopo — o que o dashboard tem

### 5.1 Filtros (uma linha no topo, valem para tudo)
- **Ano** (padrão: o mais recente), **Mês** (todos ou um), **Laboratório** (todos ou um).
- Botão **Limpar** volta ao padrão.

### 5.2 Indicadores
- **Faturamento total** do recorte, com a variação em relação ao mesmo recorte do ano anterior.
- **Maior laboratório** e a fatia dele no total. Com um laboratório filtrado, passa a mostrar a **participação no mercado** e a posição no ranking.
- **Maior queda de um mês para o seguinte** (meses consecutivos; mês sem venda conta como zero). Com um mês filtrado, compara esse mês com o anterior.
- **Média por laboratório.** Com um laboratório filtrado, mostra a **média mensal** dele.

### 5.3 Gráficos
- **Evolução mensal:**
  - Ano todo: linhas dos 8 maiores laboratórios do ano (8 é o limite da paleta de cores acessível).
  - Um mês filtrado: barras com o ranking dos 10 maiores do mês.
  - Um laboratório filtrado: uma linha por ano, para comparar a evolução dele.
- **Faturamento total por mês:** barras do ano selecionado lado a lado com o ano anterior. O mês filtrado fica em destaque.
- **Participação:** rosca com os 5 maiores e "Outros". Com um laboratório filtrado, mostra o laboratório contra o resto do mercado.
- A cor de cada laboratório é fixa dentro do ano (segue o laboratório, não a posição no gráfico).

### 5.4 Quem mais cresce (ranking de crescimento)
Tabela com os laboratórios que mais crescem (ou mais caem). Usa o ano e o mês do topo e tem filtros próprios:
- **Comparar com:**
  - **Mesmo período do ano anterior** (padrão). Com um mês filtrado, compara só aquele mês.
  - **Mês anterior.** Usa o mês filtrado ou, se nenhum estiver filtrado, o último mês com dados. Em janeiro, compara com dezembro do ano anterior.
  - **2º semestre vs 1º semestre** do ano selecionado.
- **Mostrar:** os que mais crescem ou os que mais caem.
- **Ordenar por:** variação em R$ ou em %. Na ordenação por %, laboratórios sem faturamento no período base ("novos") ficam de fora, e o rodapé informa quantos são.
- **Porte mínimo:** ignora laboratórios pequenos, que distorcem o %. O critério é o maior faturamento entre os dois períodos. Opções: Todos, R$ 10 mil, R$ 50 mil (padrão) e R$ 200 mil.
- **Quantidade:** 10, 20 ou 50.
- Colunas: posição, laboratório, valor antes, valor depois, variação em R$, variação em % e uma barra proporcional.
- Com um laboratório filtrado no topo, ele fica destacado na lista. Se estiver fora do top, aparece no fim com a posição dele.

### 5.5 Resumo comentado (até 6 cartões)
- **Mês atípico (amarelo):** total do mês abaixo da metade da mediana do ano. Sinaliza planilha incompleta.
- **Queda (vermelho):** último mês com dados menor que o primeiro.
- **Instabilidade (amarelo):** último mês 25% ou mais abaixo do pico do ano.
- **Destaque (verde):** crescimento acima de R$ 50.000 entre o primeiro e o último mês.

### 5.6 Tabela detalhada
- Colunas: Laboratório, Mês, Faturamento, % do mês e Variação vs mês anterior.
- Ordenada do maior para o menor, com 15 linhas por página.

## 6. Requisitos técnicos

- **Monolítico:** um único `index.html`, que funciona aberto direto do disco (duplo clique) **sem internet**, sem servidor e sem CDN.
- Hospedado no **GitHub Pages**, a partir da raiz da branch `main`.
- Atualização em **um passo** (`atualizar.bat`), descrita no `README.md`.
- Tema escuro, responsivo (notebook e celular), valores em `R$ 1.234,56`, meses em ordem de calendário.
- Todos os arquivos em UTF-8.

## 7. Fora do escopo

- Login, banco de dados ou servidor próprio.
- Edição dos dados pelo dashboard.
- Comparação com metas.

## 8. Critérios de pronto

- [x] `index.html` abre offline e mostra 2024 e 2025 com os 12 meses.
- [x] O total de cada ano bate com a soma da coluna `Valor` da planilha (após a limpeza).
- [x] Os filtros de ano, mês e laboratório atualizam cards, gráficos, resumo e tabela.
- [x] Nenhum texto com acento corrompido.
- [x] `atualizar.bat` regenera o dashboard e publica no GitHub.

## 9. Pontos em aberto

- **Atenção, repositório público:** o repositório e o site são públicos. Qualquer pessoa com o link vê a planilha e os valores. Se os dados forem confidenciais, torne o repositório privado. O GitHub Pages em repositório privado exige plano pago.
- **BIOSINTETICA, dezembro de 2025:** a coluna `Valor` está vazia e `22,7567` foi digitado na `% Mensal`. Pelo quadro resumo da própria planilha, o valor correto seria cerca de **R$ 292.896,10**. Corrigir a linha 937 da aba `25. BANCO DE DADOS`.
- **Junho de 2025:** soma só R$ 271 mil, contra R$ 0,85 a 1,9 milhão nos outros meses. É preciso confirmar se o mês está incompleto.
- **2024:** há 5 linhas sem nome de laboratório (R$ 117,91 no total). Completar ou apagar.
- **Grupos de laboratórios:** `EMS MARCAS`/`EMS GENERICO`, `EUROFARMA`/`EUROFARMA OTC` e `NOVAQUIMICA`/`NOVA QUIMICA GENERICO` aparecem separados. Falta decidir se devem ser agrupados.
