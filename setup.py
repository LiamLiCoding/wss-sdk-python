from setuptools import setup, find_packages

setup(
    name='wss-sdk',
    version='1.0.1',
    keywords=['IOT', 'WSS', 'websocket', 'Haozheng Li'],
    description='wss-sdk is multifunctional detection Python IoT client sdk.',
    license='MIT License',

    url='https://github.com/Haozheng-Li/wss-sdk-python',
    author='Haozheng Li',
    author_email='haozheng.l@outlook.com',

    packages=find_packages(),
    include_package_data=False,
    platforms=["any"],
    install_requires=['websocket-client'],
    python_requires='>3.8',
    entry_points={
        'console_scripts': [
            'wss = wss.client:main',
        ]
    }
)