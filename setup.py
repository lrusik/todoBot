#!/usr/bin/python3
import os, sys
from distutils.core import setup
from setuptools import setup, find_packages

with open('README.md', 'r', encoding="utf-8") as content_file:
    long_description = content_file.read()

setup(
    name="todoBot",
    version="0.1", 
    packages=find_packages(),
    install_requires=[
        'setuptools', 
        'config', 
        'py', 
        'pytest',
        'requests',
        'six',
        'wheel'
        ],
    package_data={
        'dacs': ['*.txt', '*.rst'],
    },
    scripts=["bin/todoBot", "bin/set-todoBot"], 
    author="Ruslan Yakushev", 
    author_email="yakushev.rusl101@gmail.com",
    description="Simple bot",
    long_description = long_description,
    url="https://github.com/lrusifikator/todoBot",
    license="MIT",  
    project_urls={
        "Source Code": "https://github.com/lrusifikator/todoBot",
        "Documentation": "https://github.com/lrusifikator/todoBot/docs",
    }, 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
