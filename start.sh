#!/bin/bash

echo "🚀 Запуск проекта трасс скалодрома"
echo "=================================="

# Проверка наличия Docker
if command -v docker &> /dev/null; then
    echo "✅ Docker найден"
    
    # Проверка наличия docker-compose
    if command -v docker-compose &> /dev/null; then
        echo "✅ Docker Compose найден"
        echo "🐳 Запуск через Docker Compose..."
        docker-compose up --build
    else
        echo "🐳 Запуск через Docker..."
        docker build -t climbing-routes .
        docker run -p 8000:8000 climbing-routes
    fi
else
    echo "❌ Docker не найден"
    echo "📋 Попробуйте следующие варианты:"
    echo ""
    echo "1. Установите Docker Desktop: https://www.docker.com/products/docker-desktop"
    echo "2. Установите инструменты разработки: xcode-select --install"
    echo "3. Используйте Homebrew: brew install python"
    echo ""
    echo "📖 Подробные инструкции в файле SETUP.md"
fi
