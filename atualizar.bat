@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo  Atualizando o dashboard de faturamento
echo ============================================
echo.

rem Git instalado mas fora do PATH: usa o caminho padrao do Git for Windows
where git >nul 2>nul || set "PATH=%ProgramFiles%\Git\cmd;%PATH%"
where py >nul 2>nul && (set "PY=py -3") || (set "PY=python")
%PY% ferramentas\gerar_dashboard.py
if errorlevel 1 (
  echo.
  echo ERRO ao gerar o dashboard. Nada foi enviado ao GitHub.
  pause
  exit /b 1
)

echo.
echo Enviando para o GitHub...
git add -A
git diff --cached --quiet && (
  echo Nenhuma alteracao para enviar.
  pause
  exit /b 0
)
git commit -q -m "Atualiza dados do dashboard (%date%)"
git push
if errorlevel 1 (
  echo.
  echo ERRO ao enviar para o GitHub. Verifique a internet e o login no GitHub.
  pause
  exit /b 1
)
echo.
echo Pronto! O site atualiza em 1 a 2 minutos:
echo https://diegosimioni2026.github.io/FaturamentoMensal/
pause
