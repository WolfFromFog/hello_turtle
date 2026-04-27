# Лабораторная работа: Разработка ROS2-ноды для turtlesim

## 🎯 Цель работы
Реализовать ROS2-ноду, которая создает дополнительного движущегося объекта (черепашку) в окне `turtlesim_node`. Стартовая черепашка управляется с клавиатуры, а дополнительная должна автоматически следовать за ней.

## 📋 Технические требования

1. **Интеграция с turtlesim**
   - Нода должна работать в совокупности с `turtlesim_node` и `teleop_key` из пакета `turtlesim`.
   - Разрабатываемая нода создает дополнительного движущегося объекта в окне симуляции.

2. **Логика следования**
   - Дополнительная черепашка должна следовать за любой другой черепашкой.
   - Цель для следования указывается в момент создания дополнительной черепашки.
   - **Реализация:**
     - Считывать координаты обеих черепашек через топики `/<имя_черепашки>/pose`.
     - Вычислять трансформацию между позициями.
     - Отправлять команды управления в топик `/<имя_черепашки2>/cmd_vel`.

3. **Архитектура кода**
   - Обернуть разрабатываемую ноду в **один класс**.
   - **Запрещено** использование глобальных переменных.
   - Архитектура должна позволять создавать произвольное количество черепашек за счёт запуска произвольного количества нод.

4. **Launchfile**
   - Разработать `launchfile`, запускающий все требуемые ноды.
   - Предусмотреть входной параметр для установки **скорости черепашки-преследователя**.

5. **Разделение ответственности (Separation of Concerns)**
   - Разделить логику движения черепашки и логику взаимодействия с ROS на **два разных класса**.
   - Логика движения должна быть независима от ROS и готова к переиспользованию в следующих работах.

6. **Цепочка следования**
   - Создать несколько черепашек с произвольными координатами.
   - Каждая новосозданная черепашка должна следовать за созданной до неё.
   - **Сценарий:**
     1. Стартовая черепашка (управление с клавиатуры).
     2. Черепашка №2 (следует за стартовой).
     3. Черепашка №3 (следует за №2) и так далее.

7. **Нагрузочное тестирование**
   - Выяснить предельное количество черепашек, которые могут быть обработаны вашим компьютером без потери производительности.

## 🏆 Критерии оценки

| Оценка | Требования |
| :--- | :--- |
| **3 (Задача минимум)** | - Выполнены пункты **1-5**.<br>- Создана **1 дополнительная черепашка**.<br>- Продемонстрировано следование второй черепашки за стартовой. |
| **5 (Задача максимум)** | - Реализовано поведение черепашки **независимо от ROS**.<br>- Реализована прослойка между логикой черепашки и ROS (чтение сообщений, вызов команд).<br>- Выполнены пункты **1-7** (цепочка черепашек и нагрузочное тестирование). |


ШПАРГАЛКА
```bash

docker compose up -d

# Разрешаем Docker-контейнерам подключаться к вашему дисплею
xhost +local:docker


#Управление Затем в другом терминале (или в том же, если turtlesim запущен в фоне):

docker compose exec ros_humble bash
ros2 run turtlesim turtle_teleop_key

# Default speed (1.0)
ros2 launch hello_world first_launcher.launch.py

# Custom speed
ros2 launch hello_world first_launcher.launch.py speed:=2.0

docker compose exec ros_humble bash

source /ros2_ws/install/setup.bash
source /opt/ros/humble/setup.bash

ros2 run turtlesim turtle_teleop_key

ros2 run turtlesim turtlesim_node &

ros2 run turtlesim turtlesim_node &

ros2 run rviz2 rviz2

container
    ||
term1   term2
window1 window2

открыть несколько окон



 docker exec -it <контейнер> <команда>` - выполнение команды в запущенном контейнере в интерактивном режиме с доступом к консоли



ros2 run hello_world turtle_commander.py


docker-compose run --rm ros-humble bash
```

# QUICKSTART

## Linux

```bash
# 1. Сделать скрипты исполняемыми
chmod +x run.sh stop.sh

# 2. Запустить контейнер
./run.sh

# 3. Подключиться к контейнеру
docker exec -it hello_world_container bash

# 4. Внутри контейнера запустить ROS2
ros2 run turtlesim turtlesim_node &
ros2 run hello_world turtle_commander.py
```
### Запуск через launchfile
```bash
# В одном терминале
docker exec -it hello_world_container bash
ros2 launch hello_world first_launcher.launch.py

# В другом терминале (для teleop)
docker exec -it hello_world_container bash
ros2 run turtlesim turtle_teleop_key
```

### Работа графики
```bash
xhost +local:docker
```

## Windows

### Шаг 1: Подготовить X-сервер (для графики)
```
# Запустить VcXsrv или Xming с настройками:
# ☑ Multiple windows
# ☑ Start no client
# ☑ Disable access control (ВАЖНО!)
```

### Шаг 2. Собрать контейнер
```powershell
docker build . -t lab1:alpha
```

### Шаг 3. Запустить контейнер
```powershell
.\run.ps1
```

### Шаг 4. Внутри контейнера, запустить launch-файл
```bash
ros2 launch hello_world first_launcher.launch.py

ros2 run turtlesim turtle_teleop_key

ros2 launch hello_world first_launcher.launch.py num_turtles:=100 speed:=15.8


#rqt
source /ros2_ws/install/setup.bash
rqt_graph

```

## Основные отличия ROS2 от ROS1

| ROS1 (Noetic) | ROS2 (Humble) |
|---------------|---------------|
| `catkin_make` | `colcon build` |
| `catkin_ws/devel/setup.bash` | `ros2_ws/install/setup.bash` |
| `roscore` | Не нужен (встроен в узлы) |
| `rosrun` | `ros2 run` |
| `roslaunch` | `ros2 launch` |
| `rostopic` | `ros2 topic` |
| `rosnode` | `ros2 node` |
| `rosservice` | `ros2 service` |
| `rospy` | `rclpy` |
| XML launch files | Python launch files |


# Запуск симулятора черепахи

ros2 run turtlesim turtlesim_node

# Запуск вашей ноды (адаптируйте имя под ваш пакет)
ros2 run hello_world turtle_cmd  # если есть console_script в setup.py
# ИЛИ напрямую:
python3 /ros2_ws/src/hello_world/scripts/turtle_cmd.py

# Просмотр топиков и узлов
ros2 topic list
ros2 node list
rqt_graph  # визуализация

# Тест публикации команды
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5}, angular: {z: 0.3}}"