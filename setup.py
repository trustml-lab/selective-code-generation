import os

import pkg_resources
from setuptools import setup, find_packages

setup (
    name="selective_code_generation",
    py_modules=["selective_code_generation"],
    version="1.0",
    description="",
    author="Jaewoo Jeong",
    packages=find_packages(),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ]
)
