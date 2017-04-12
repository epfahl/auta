from setuptools import setup, find_packages

setup(
    name='auta',
    version='0.1',
    description='finite state machine library for time series data',
    url='https://github.com/epfahl/auta',
    author='Eric Pfahl',
    packages=find_packages(),
    install_requires=[
        'toolz',
        'decorator',
        'cerberus',
        'python-dateutil'])
