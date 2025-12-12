from setuptools import setup, find_packages
from typing import List

def get_requirements():
    """Read the requirements from the requirements.txt file."""
    try:
        requirements = []
        with open("requirements.txt", "r") as file:
            requirements = file.readlines()
        
        return [req.strip() for req in requirements if req.strip()]
    except Exception as e:
        print(e)

setup(
    name="Network Security",
    version="1.0.0",
    description="A machine learning project",
    author="Shri Charan",
    author_email="rshricharan29@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)