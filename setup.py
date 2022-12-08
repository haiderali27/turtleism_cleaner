from setuptools import setup

package_name = 'turtlesim_cleaner'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sayhelloxd',
    maintainer_email='haderaliprofessional@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gotogoal = turtlesim_cleaner.gotogoal:main',
            'move =  turtlesim_cleaner.move:main',
            'rotate = turtlesim_cleaner.rotate:main',
            'gotogoal_straight = turtlesim_cleaner.gotogoal_straight:main'
        ],
    },
)
