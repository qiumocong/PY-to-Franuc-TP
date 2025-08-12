"""
Setup script for PY-to-Franuc-TP package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="py-to-franuc-tp",
    version="1.0.0",
    author="PY-to-Franuc-TP Project",
    description="Python library for writing Fanuc robot teach pendant programs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Manufacturing",
        "Topic :: Scientific/Engineering :: Automation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    keywords="fanuc robot automation teach pendant programming",
    project_urls={
        "Bug Reports": "https://github.com/qiumocong/PY-to-Franuc-TP/issues",
        "Source": "https://github.com/qiumocong/PY-to-Franuc-TP",
    },
)