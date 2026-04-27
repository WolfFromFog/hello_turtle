from setuptools import setup, find_packages  # ✅ Исправленный импорт

package_name = 'hello_turtle'  # ✅ Должно совпадать с package.xml

setup(
    name=package_name,
    version='0.0.1',
    # ✅ Ищем пакеты внутри scripts/
    packages=find_packages(where='scripts', exclude=['test']),
    package_dir={'': 'scripts'},
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@example.com',
    description='Turtle chain follower for ROS2',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # ✅ Формат: 'command = module:function'
            # module — это имя файла без .py внутри scripts/
            'turtle_cmd = turtle_cmd:main',
        ],
    },
)