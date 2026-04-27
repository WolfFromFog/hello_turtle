FROM ros:humble-ros-base

# Установка зависимостей
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    ros-humble-turtlesim \
    ros-humble-geometry-msgs \
    ros-humble-std-msgs \
    ros-humble-rqt \
    ros-humble-rqt-common-plugins \
    python3-pip \
    vim \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочего пространства (единый путь везде!)
RUN mkdir -p /ros2_ws/src/hello_world
WORKDIR /ros2_ws

# Копирование файлов проекта (БЕЗ shell-операторов в COPY!)
COPY scripts/ /ros2_ws/src/hello_world/hello_world/
COPY package.xml /ros2_ws/src/hello_world/
COPY setup.py /ros2_ws/src/hello_world/
COPY setup.cfg /ros2_ws/src/hello_world/
COPY CMakeLists.txt /ros2_ws/src/hello_world/

# Установка прав на скрипты
RUN chmod +x /ros2_ws/src/hello_world/hello_world/*.py

# Сборка проекта
RUN bash -c "source /opt/ros/humble/setup.bash && \
    colcon build --symlink-install --packages-select hello_world"

# Копирование entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]