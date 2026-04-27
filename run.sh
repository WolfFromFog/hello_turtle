#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Запуск ROS2 Humble в Docker ===${NC}"

# Проверка доступа к X-серверу
if [ "$OSTYPE" = "linux-gnu"* ]; then
    echo "Настройка доступа к X-серверу..."
    xhost +local:docker 2>/dev/null || echo "Предупреждение: не удалось настроить xhost"
    export DISPLAY=:0
fi

# Для macOS
if [ "$OSTYPE" = "darwin"* ]; then
    export DISPLAY=host.docker.internal:0
fi

# Сборка и запуск контейнера
echo "Сборка образа..."
docker compose up -d --build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Контейнер запущен!${NC}"
    echo ""
    echo "Для подключения к контейнеру:"
    echo "  docker exec -it hello_world_container bash"
    echo ""
    echo "Полезные команды внутри контейнера:"
    echo "  ros2 run turtlesim turtlesim_node  - запуск симулятора"
    echo "  ros2 run hello_world turtle_commander.py  - запуск вашей ноды"
    echo "  ros2 launch hello_world first_launcher.launch.py  - запуск launch-файла"
    echo "  ros2 topic list              - список топиков"
    echo "  rqt_graph                  - визуализация графа узлов"
    echo ""
    echo "Для остановки:"
    echo "  docker compose down"
else
    echo -e "${RED}Ошибка запуска контейнера!${NC}"
    exit 1
fi
