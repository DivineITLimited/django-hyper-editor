import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='hypereditor',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='Divine IT Limited 2018',
    description='Hyper Editor Integration With Django',
    long_description=README,
    author='Shimul Chowdhury',
    author_email='shimul@divine-it.net',
    install_requires = [
    ],
    dependency_links = [
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6'
    ],
)
