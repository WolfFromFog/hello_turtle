#! /usr/bin/env python3
"""
Код, отвечающий за управлением черепахами для ROS 2
"""
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from hello_turtle.ros_math import def_angl, def_distance

#Класс управления

class TurtleCommander(Node):
    """
    Узел управления черепахой.
    Подписывается на топик-позу целевой черепахи, вычисляет угол поворота и скорость,
    публикует команды скорости в топик управляемой черепахи.
    """

    def __init__(self):
        super().__init__('turtle_commander')

        # Параметры узла
        self.declare_parameter('name', 'turtle2')
        self.declare_parameter('target', 'turtle1')
        self.declare_parameter('spawn_x', 0.0)
        self.declare_parameter('spawn_y', 0.0)
        self.declare_parameter('spawn_theta', 0.0)
        self.declare_parameter('speed', 1.0)

        self.name = self.get_parameter('name').value
        self.target = self.get_parameter('target').value
        self.spawn_x = self.get_parameter('spawn_x').value
        self.spawn_y = self.get_parameter('spawn_y').value
        self.spawn_theta = self.get_parameter('spawn_theta').value
        self.speed = self.get_parameter('speed').value

        # Позы черепах
        self.self_pose = None
        self.target_pose = None

        # Создать черепаху, если её нет
        self.create_turtle()

        # Публикатор команды скорости
        self.cmd_pub = self.create_publisher(Twist, f'/{self.name}/cmd_vel', 10)

        # Подписчики на позы
        self.target_sub = self.create_subscription(
            Pose, f'/{self.target}/pose', self.callback_target, 10
        )
        self.self_sub = self.create_subscription(
            Pose, f'/{self.name}/pose', self.callback_self, 10
        )

    def create_turtle(self):
        """Вызов сервиса /spawn для создания черепахи."""
        spawn_client = self.create_client(Spawn, '/spawn')
        while not spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Ожидание сервиса /spawn...')

        request = Spawn.Request()
        request.x = self.spawn_x
        request.y = self.spawn_y
        request.theta = self.spawn_theta
        request.name = self.name

        future = spawn_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            self.get_logger().info(f'Черепаха {self.name} создана')
        else:
            self.get_logger().info(
                f'Черепаха {self.name} уже существует (или ошибка): {future.exception()}'
            )

    def callback_target(self, msg):
        """Обработчик позы целевой черепахи."""
        self.target_pose = msg
        self.get_logger().info(
            f'Получена позиция цели: x={msg.x:.2f}, y={msg.y:.2f}'
        )

    def callback_self(self, msg):
        """Обработчик позы управляемой черепахи."""
        self.self_pose = msg
        self.get_logger().info(
            f'Получена позиция своя: x={msg.x:.2f}, y={msg.y:.2f}, t={msg.theta:.2f}'
        )



def main(args=None):
    rclpy.init(args=args)
    node = TurtleCommander()

    msg = Twist()
    # Даём время на появление черепах и получение первых поз
    time.sleep(1)

    while rclpy.ok():
        # Обработка колбэков подписчиков
        rclpy.spin_once(node, timeout_sec=0)

        if node.target_pose is not None and node.self_pose is not None:
            # Вычисление угла и расстояния
            angl = def_angl(
                node.target_pose.x, node.target_pose.y,
                node.self_pose.x, node.self_pose.y,
                node.self_pose.theta
            )
            dc = def_distance(
                node.target_pose.x, node.target_pose.y,
                node.self_pose.x, node.self_pose.y
            )

            if dc <= 1.0:
                msg.linear.x = 0.0
                msg.angular.z = 0.0
            else:
                msg.linear.x = node.speed
                msg.angular.z = angl

            node.cmd_pub.publish(msg)

        # Пауза 1 секунда
        #time.sleep(1)

    rclpy.shutdown()


if __name__ == '__main__':
    main()