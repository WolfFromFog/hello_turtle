#!/bin/bash
set -e

# Источник переменных окружения ROS2
source /opt/ros/humble/setup.bash

# Источник переменных окружения рабочего пространства
if [ -f "/ros2_ws/install/setup.bash" ]; then
    source /ros2_ws/install/setup.bash
fi

# PYTHONPATH для ament_python пакетов
export PYTHONPATH="${PYTHONPATH}:/ros2_ws/src/hello_world"

# Переход в директорию проекта
cd /ros2_ws/src/hello_world

# Запускаем интерактивный bash
exec bash -i