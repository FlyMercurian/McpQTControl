#!/bin/bash

# QT应用控制 MCP 客户端 - Unix启动器
echo "=========================================="
echo "QT应用控制 MCP 客户端 - Unix启动器"  
echo "=========================================="
echo

# 检查Python是否可用
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ 未找到Python，请先安装Python 3.8+"
    exit 1
fi

# 确定Python命令
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
else
    PYTHON_CMD="python"
    PIP_CMD="pip"
fi

echo "✅ 使用Python: $($PYTHON_CMD --version)"

# 进入脚本目录
cd "$(dirname "$0")"

# 检查依赖
echo "🔍 检查依赖..."
if ! $PIP_CMD show python-dotenv >/dev/null 2>&1; then
    echo "📦 正在安装依赖..."
    $PIP_CMD install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
fi

# 启动客户端
echo "🚀 启动MCP客户端..."
echo
$PYTHON_CMD start.py

echo
echo "客户端已退出" 