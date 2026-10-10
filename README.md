# Faturamento Mensal por Laboratório

Dashboard da evolução do faturamento por laboratório, mês a mês e ano a ano.

**Ver online:** https://diegosimioni2026.github.io/FaturamentoMensal/

O dashboard é um único arquivo, o `index.html`. Ele funciona com duplo clique, sem internet e sem instalar nada.

## Como atualizar os dados

1. Atualize a planilha em `dados/` e salve. Ela deve ser a única `.xlsx` da pasta.
2. Dê **dois cliques em `atualizar.bat`**.
3. Pronto. O site atualiza em 1 a 2 minutos.

O `atualizar.bat` faz três coisas:
- lê a planilha;
- gera um novo `index.html`;
- envia tudo para o GitHub.

Se a planilha tiver linhas com problema (sem nome, sem valor etc.), elas aparecem na tela e no topo do dashboard, em **"Avisos da planilha"**.

### Ano novo

Na planilha, crie (ou preencha) a aba `NN. BANCO DE DADOS`, com `NN` = os dois últimos dígitos do ano. Use as colunas `Empresa`, `Mês` e `Valor` na linha 1. O ano aparece sozinho no filtro.

## Requisitos (só para atualizar)

- [Python 3](https://www.python.org/downloads/). Não precisa de nenhuma biblioteca extra.
- [Git for Windows](https://git-scm.com/download/win), com login no GitHub já feito nesta máquina.

## Estrutura

| Caminho | O que é |
|---|---|
| `index.html` | Dashboard final, gerado automaticamente. **Não edite à mão.** |
| `dados/` | Planilha de origem |
| `atualizar.bat` | Gera o dashboard e publica |
| `ferramentas/gerar_dashboard.py` | Leitura e limpeza da planilha |
| `ferramentas/template.html` | Visual e lógica do dashboard. Edite aqui e rode `atualizar.bat`. |
| `ferramentas/vendor/` | Chart.js 4.4.1, embutido no HTML |
| `CONTEXTO.MD` | Escopo completo do projeto |
| `SPRINTS.md` | Planejamento de execução (o que foi feito e o que falta) |

Para só gerar o `index.html`, sem publicar: `py ferramentas/gerar_dashboard.py`
