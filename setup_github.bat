@echo off
chcp 65001 >nul
echo ========================================
echo  PPT Translator GitHub 上传工具
echo ========================================
echo.

:: 检查 gh CLI
gh --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未安装 GitHub CLI
    echo 正在尝试安装...
    winget install --id GitHub.cli
    echo 请重新运行此脚本
    pause
    exit /b 1
)

echo [1/4] 检查 GitHub 认证状态...
gh auth status >nul 2>&1
if errorlevel 1 (
    echo [提示] 需要登录 GitHub
    echo 请在浏览器中完成授权...
    gh auth login --web
    echo.
    echo 登录完成后，按任意键继续...
    pause >nul
)

echo [2/4] 创建 GitHub 仓库...
echo 仓库名称: PPT-Translator-Formatting-Intact-with-LLMs
echo 可见性: public
echo.

gh repo create PPT-Translator-Formatting-Intact-with-LLMs --public --source=. --remote=origin --push

if errorlevel 1 (
    echo [错误] 创建仓库失败
    echo 尝试添加远程仓库...
    git remote add origin https://github.com/%USERNAME%/PPT-Translator-Formatting-Intact-with-LLMs.git 2>nul
    git push -u origin main
)

echo.
echo ========================================
echo  完成！
echo ========================================
echo.
echo 仓库地址: https://github.com/YOUR_USERNAME/PPT-Translator-Formatting-Intact-with-LLMs
echo.
pause
