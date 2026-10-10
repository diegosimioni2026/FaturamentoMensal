# SPRINTS — Planejamento de execução do projeto

> Plano de execução do **Dashboard de Faturamento por Laboratório**: o que já foi entregue e o que falta, em ordem.
> O escopo completo e as regras de cálculo estão no [CONTEXTO.MD](CONTEXTO.MD).
>
> **Site:** https://diegosimioni2026.github.io/FaturamentoMensal/
> **Repositório:** https://github.com/diegosimioni2026/FaturamentoMensal

---

## Como ler este plano

- **Sprint:** bloco curto de trabalho com um objetivo único e uma entrega verificável.
- **Status:** ✅ concluída · 🔄 em andamento · ⏳ planejada · 💤 backlog (sem data)
- **Quem:**
  - **Dono:** Diego (dono da planilha e das decisões de negócio).
  - **Dev:** quem mexe no código (pessoa ou IA).
- **Pronto quando:** critérios objetivos. A sprint só fecha com **todos** marcados.
- **Duração sugerida:** 1 semana por sprint. As sprints de dados (3 e 4) dependem só do Dono e podem andar em paralelo com as de código.

## Resumo

| # | Sprint | Status | Quem | Depende de |
|---|---|---|---|---|
| 0 | Descoberta e escopo | ✅ | Dev | — |
| 1 | Dashboard monolítico + publicação | ✅ | Dev | 0 |
| 2 | Ranking "Quem mais cresce" + documentação | ✅ | Dev | 1 |
| 3 | Decisões de privacidade e repositório | ⏳ | Dono + Dev | — |
| 4 | Correção da planilha | ⏳ | Dono | — |
| 5 | Validação automática dos dados | ⏳ | Dev | 1 |
| 6 | Agrupamento de laboratórios | ⏳ | Dono + Dev | 4 |
| 7 | Entrada de 2026 e rotina mensal | ⏳ | Dono | 4, 5 |
| 8 | Melhorias de uso | 💤 | Dev | 5 |

---

## ✅ Sprint 0 — Descoberta e escopo

**Objetivo:** entender o que existia e definir exatamente o que o projeto deve entregar.
**Período:** 10/10/2026

**Tarefas**
- [x] Analisar o `index.html` inicial, o `data.js` e a planilha.
- [x] Diagnosticar por que o dashboard não funcionava: o acento corrompido (`MÃªs` × `Mês`) deixava os meses vazios.
- [x] Mapear os problemas da planilha: linhas vazias, `"Junho "` com espaço, duplicados e o valor da BIOSINTETICA digitado na coluna errada.
- [x] Descobrir as abas por ano (`24.`, `25.` e `26. BANCO DE DADOS`) e que a aba 2026 é cópia de 2025.
- [x] Reescrever o `CONTEXTO.MD` com objetivo, escopo, critérios de pronto e pontos em aberto.

**Entrega:** `CONTEXTO.MD` com o escopo completo.

---

## ✅ Sprint 1 — Dashboard monolítico e publicação

**Objetivo:** dashboard em um único HTML, funcionando offline e publicado no GitHub Pages, com atualização em um clique.
**Período:** 10/10/2026 · **Commit:** `497a114`

**Tarefas**
- [x] Religar a pasta local ao repositório do GitHub, preservando o histórico.
- [x] Criar o `ferramentas/gerar_dashboard.py`:
  - [x] lê o `.xlsx` só com Python puro;
  - [x] lê toda aba `NN. BANCO DE DADOS`;
  - [x] limpa os dados, soma duplicados e ignora abas copiadas;
  - [x] gera os avisos da planilha.
- [x] Criar o `ferramentas/template.html`:
  - [x] CSS próprio, sem Tailwind;
  - [x] Chart.js embutido;
  - [x] filtros de ano, mês e laboratório;
  - [x] cards, 3 gráficos, resumo comentado e tabela paginada.
- [x] Gerar o `index.html` monolítico, sem nenhuma requisição externa.
- [x] Criar o `atualizar.bat`: gera, faz commit e push, e acha o Git fora do PATH.
- [x] Mover a planilha para `dados/` e remover o `data.js`.
- [x] Tirar do Git os instaladores (MinGit, PortableGit, instalador do Python).
- [x] Criar o `README.md`, o `.gitignore` e o `.gitattributes`.
- [x] Testar no Edge sem janela (headless): padrão, laboratório filtrado e mês filtrado.
- [x] Publicar e conferir o site no ar.

**Pronto quando**
- [x] O `index.html` abre com duplo clique, sem internet.
- [x] Os totais de 2024 e 2025 batem com a soma da coluna `Valor`.
- [x] Nenhum acento corrompido.
- [x] O site publicado mostra a versão nova.

---

## ✅ Sprint 2 — Ranking "Quem mais cresce" e documentação

**Objetivo:** responder **quais indústrias mais crescem**, com filtros próprios.
**Período:** 10/10/2026 · **Commits:** `c226778`, `e682306`

**Tarefas**
- [x] Criar a seção "Quem mais cresce" com estes filtros:
  - [x] **Comparar com:** ano anterior, mês anterior ou semestre;
  - [x] **Mostrar:** os que mais crescem ou os que mais caem;
  - [x] **Ordenar por:** R$ ou %;
  - [x] **Porte mínimo** e **Quantidade**.
- [x] Tratar os laboratórios "novos" (base zero) na ordenação por %.
- [x] Destacar o laboratório filtrado no topo e mostrar a posição dele mesmo fora do top N.
- [x] Testar a ordenação por R$ e por %.
- [x] Reescrever o `CONTEXTO.MD` como documento único do projeto.
- [x] Criar este `SPRINTS.md`.

**Pronto quando**
- [x] O ranking mostra FORTLIFE, PRUDENCE e BIOSINTETICA no topo em R$ (2025 contra 2024).
- [x] Ao mudar qualquer filtro, a tabela se recalcula sem erro.
- [x] O CONTEXTO.MD descreve todas as regras de cálculo.

---

## ⏳ Sprint 3 — Decisões de privacidade e repositório

**Objetivo:** garantir que os dados de faturamento só estejam visíveis para quem deve vê-los.
**Quem:** Dono decide, Dev executa.
**Por que agora:** o repositório e o site são **públicos**. Hoje qualquer pessoa com o link vê a planilha e os valores.

**Decisões do Dono**
- [ ] Os dados podem ficar públicos? (sim / não)
- [ ] Se **não**, escolher uma saída:
  - [ ] **A:** tornar o repositório privado. O GitHub Pages em repositório privado exige plano pago (GitHub Pro ou equivalente).
  - [ ] **B:** repositório privado sem Pages. O dashboard passa a ser distribuído como arquivo `index.html` (por e-mail, OneDrive ou Teams). Ele já funciona offline.
  - [ ] **C:** manter público, mas tirar a planilha do repositório. **Não resolve sozinha:** o `index.html` publicado continua com todos os valores dentro.
- [ ] Apagar os instaladores (cerca de 130 MB) também do **histórico** do Git? Isso exige reescrever o histórico e fazer um envio forçado (*force push*).

**Tarefas do Dev** (conforme a decisão)
- [ ] Alterar a visibilidade do repositório e o Pages.
- [ ] Se for o caso, limpar o histórico com `git filter-repo` e fazer o force push, avisando antes quem tiver cópia do repositório.
- [ ] Ajustar o `atualizar.bat`, o README e o CONTEXTO.MD ao novo fluxo.

**Pronto quando**
- [ ] A decisão está registrada no CONTEXTO.MD (seção 9, item 1).
- [ ] O acesso real confere com a decisão (testado numa janela anônima).

---

## ⏳ Sprint 4 — Correção da planilha

**Objetivo:** zerar os avisos da planilha e confirmar os números que hoje distorcem o dashboard.
**Quem:** Dono. Corrige em `dados/01. FATURAMENTO MÊS A MES.xlsx` e roda o `atualizar.bat`.

**Tarefas**
- [ ] **BIOSINTETICA, dezembro de 2025** (aba `25. BANCO DE DADOS`, linha 937):
  - [ ] colocar o valor na coluna `Valor`. Pelo quadro resumo da planilha, deve ser cerca de **R$ 292.896,10**;
  - [ ] limpar a `% Mensal` (`22,7567`).
- [ ] **Junho de 2025:** confirmar se R$ 270.899,38 é o valor real ou se faltam lançamentos. Completar se faltar.
- [ ] **2024, linhas sem laboratório:** linhas 261, 399, 479, 552 e 628 (R$ 117,91 no total). Preencher o nome ou apagar.
- [ ] **Duplicados** (10 em 2025, 2 em 2024; ex.: NATIVITA): confirmar se é o mesmo laboratório. Se não for, diferenciar os nomes.
- [ ] Rodar o `atualizar.bat` e conferir a caixa "Avisos da planilha".

**Pronto quando**
- [ ] A caixa de avisos mostra só o aviso da aba 2026 (cópia), ou nenhum aviso.
- [ ] O total de dezembro de 2025 bate com o quadro "25. Resultado" (R$ 1.287.076,11).
- [ ] O cartão "Mês atípico: Junho" some, ou foi confirmado como real.
- [ ] Os itens 2 a 5 da seção 9 do CONTEXTO.MD estão atualizados.

---

## ⏳ Sprint 5 — Validação automática dos dados

**Objetivo:** o gerador avisa sozinho quando os números do dashboard não batem com a planilha.
**Quem:** Dev.

**Tarefas**
- [ ] No `gerar_dashboard.py`, ler o quadro resumo de cada aba (colunas `F`/`G`, "NN. Resultado" por mês).
- [ ] Comparar o total de cada mês calculado com o do quadro resumo. Divergência acima de R$ 1,00 vira aviso, informando o mês e a diferença.
- [ ] Mostrar no terminal uma tabela "mês × calculado × planilha × diferença".
- [ ] Opcional: parar a publicação (não fazer o push) se a diferença passar de um limite configurável.
- [ ] Documentar no CONTEXTO.MD (seções 4.3 e 6.5).

**Pronto quando**
- [ ] Com a planilha atual, o aviso aponta a diferença de dezembro de 2025 (R$ 292.896,10). Essa é a prova de que a validação funciona.
- [ ] Com a planilha corrigida (Sprint 4), não aparece nenhuma divergência.

---

## ⏳ Sprint 6 — Agrupamento de laboratórios

**Objetivo:** permitir ver grupos econômicos somados (ex.: EMS) sem perder a visão individual.
**Quem:** Dono define os grupos, Dev implementa.

**Decisões do Dono**
- [ ] Quais laboratórios formam um grupo? Candidatos:
  - `EMS MARCAS` + `EMS GENERICO`
  - `EUROFARMA` + `EUROFARMA OTC`
  - `NOVAQUIMICA` + `NOVA QUIMICA GENERICO`
  - `CREMER` + `CREMER TOPZ`
  - `HYPERMARCAS BOZZANO` + `HYPERMARCAS MONANGE`
  - `GLOBO` + `GLOBO NUTRICEUTICOS`?
- [ ] A visão padrão deve ser por laboratório ou por grupo?

**Tarefas do Dev**
- [ ] Criar o `dados/grupos.csv` (`laboratorio;grupo`), editável no Excel.
- [ ] O gerador lê o arquivo e embute o mapa no `index.html`.
- [ ] Novo filtro no topo, **Visão: Laboratório / Grupo**, que vale para cards, gráficos, ranking e tabela.
- [ ] Documentar no CONTEXTO.MD e no README.

**Pronto quando**
- [ ] Na visão por grupo, "EMS" aparece somado e o total geral não muda.
- [ ] Mudar o `grupos.csv` e rodar o `atualizar.bat` reflete no site.

---

## ⏳ Sprint 7 — Entrada de 2026 e rotina mensal

**Objetivo:** colocar 2026 no ar e deixar a atualização mensal como rotina.
**Quem:** Dono.

**Tarefas**
- [ ] Preencher a aba `26. BANCO DE DADOS` com os dados reais (Empresa, Mês e Valor na linha 1).
- [ ] Rodar o `atualizar.bat` e conferir:
  - [ ] o ano 2026 aparece no filtro e vira o padrão;
  - [ ] o card total compara com 2025 nos mesmos meses;
  - [ ] o ranking "Quem mais cresce" compara 2026 com 2025.
- [ ] Definir a rotina, por exemplo: **todo dia 5, atualizar a planilha e rodar o `atualizar.bat`**.
- [ ] Registrar a rotina no README.

**Pronto quando**
- [ ] O site mostra 2024, 2025 e 2026.
- [ ] A atualização de um mês leva menos de 5 minutos, de ponta a ponta.

---

## 💤 Sprint 8 — Melhorias de uso (backlog)

**Objetivo:** melhorias opcionais, para priorizar conforme o uso real. Escolher no máximo 3 por sprint.

| Ideia | Valor | Esforço |
|---|---|---|
| Exportar a tabela e o ranking para CSV/Excel | Alto: levar números para reuniões | Baixo |
| Busca por nome de laboratório na tabela detalhada | Médio | Baixo |
| Ordenar a tabela clicando no cabeçalho | Médio | Baixo |
| Ranking "Quem mais cresce" em gráfico de barras, além da tabela | Médio | Baixo |
| Filtro de período personalizado (ex.: Mar–Ago) | Médio | Médio |
| Modo claro / impressão em PDF | Baixo | Médio |
| Ficha do laboratório: página com histórico completo, ranking e participação | Alto | Médio |
| Alerta de laboratórios que pararam de comprar (faturavam e zeraram) | Alto | Baixo |

**Pronto quando:** cada item escolhido vira uma sprint própria, com tarefas e critérios.

---

## Fora do plano (decidido)

- Login, servidor ou banco de dados próprio.
- Edição de dados pelo dashboard.
- Comparação com metas.
- Atualização automática sem rodar o `atualizar.bat`.

## Definição de pronto (vale para toda sprint de código)

- [ ] `py ferramentas/gerar_dashboard.py` roda sem erro.
- [ ] O `index.html` abre offline e não tem erro no console do navegador.
- [ ] Os cenários padrão, laboratório filtrado e mês filtrado foram conferidos visualmente.
- [ ] O CONTEXTO.MD foi atualizado (escopo, regras e histórico).
- [ ] Publicado com o `atualizar.bat` e conferido no site.
