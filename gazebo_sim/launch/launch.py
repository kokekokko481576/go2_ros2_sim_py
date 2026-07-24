import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    DeclareLaunchArgument,
    ExecuteProcess,
    RegisterEventHandler
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.event_handlers import OnProcessExit
from launch_ros.actions import SetParameter
def generate_launch_description():
    ld = LaunchDescription()

    package_name = 'gazebo_sim'
    pkg_path = get_package_share_directory(package_name)

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    ld.add_action(DeclareLaunchArgument('use_sim_time', default_value='true',
                                       description='Использовать симуляционное время'))

    # gazebo_multi_nav2_world.launch.py へパススルーする引数
    enable_rviz = LaunchConfiguration('enable_rviz', default='true')
    ld.add_action(DeclareLaunchArgument('enable_rviz', default_value='true',
                                        description='Enable rviz launch'))
    enable_nav2 = LaunchConfiguration('enable_nav2', default='true')
    ld.add_action(DeclareLaunchArgument('enable_nav2', default_value='true',
                                        description='Enable Nav2 stack launch'))
    # gui:=false で Gazebo を server only(ヘッドレス)で起動。GUI窓(iGPU描画)を止め、
    # 可視化はRViz側に任せて負荷を下げる用途(Go2_deploy #44)。
    gui = LaunchConfiguration('gui', default='true')
    ld.add_action(DeclareLaunchArgument('gui', default_value='true',
                                        description='Show Gazebo GUI (false = headless server)'))

    ld.add_action(SetParameter(name='use_sim_time', value=use_sim_time))


    world_file = os.path.join(pkg_path, 'world', 'cafe.world')
    # gui=false のとき gz sim に -s(server only) を付けてヘッドレス化する
    headless_flag = PythonExpression(["'' if '", gui, "' == 'true' else '-s '"])
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': [headless_flag, '-r -v4 ', world_file],
                          'on_exit_shutdown': 'true'}.items()
    )
    ld.add_action(gazebo)

    pause = ExecuteProcess(
        cmd=['sleep', '6'],
        output='screen'
    )
    ld.add_action(pause)


    multi_nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_path, 'launch', 'gazebo_multi_nav2_world.launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'enable_rviz': enable_rviz,
            'enable_nav2': enable_nav2,
        }.items()
    )

    launch_after_pause = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=pause,
            on_exit=[multi_nav2_launch]
        )
    )

    ld.add_action(launch_after_pause)

    return ld
