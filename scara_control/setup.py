from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'scara_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/scara_control/launch', ['launch/joints.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rosdev',
    maintainer_email='jeremia.haapasalmi@icloud.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'joint_configuration = scara_control.joint_configuration:main',
            'end_effector_pose = scara_control.end_effector_pose:main',
            'client = scara_control.client:main',
        ],
    },
)
