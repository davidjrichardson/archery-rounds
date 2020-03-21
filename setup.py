"""This setup.py was derived from the PiPY sample project, available here:
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md")) as f:
    long_description = f.read()

setup(
    name="archery-rounds",
    verison="0.1.0",
    description="A Python 3 library providing standard archery round definitions and operations on them",
    url="https://github.com/davidjrichardson/archery-rounds",
    author="David Richardson",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="archery rounds scoring",
    packages=find_packages(),
    python_requires=">=3.5",
    install_requires=["numpy"],
    extras_require={"test": ["coverage", "pytest", "black"],},
)
