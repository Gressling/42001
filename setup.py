#!/usr/bin/env python3
"""
Setup script for ISO 42001 Bookkeeping Application
"""

from setuptools import setup, find_packages
import os

# Read version from __init__.py
version = {}
with open(os.path.join("src", "iso42001", "__init__.py")) as f:
    exec(f.read(), version)

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="iso42001-bookkeeping",
    version=version["__version__"],
    author="Gressling Consulting GmbH",
    author_email="info@gressling.de",
    description="A Dash-based application for basic ISO 42001 AI Management System bookkeeping",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gressling/42001",
    project_urls={
        "Bug Tracker": "https://github.com/Gressling/42001/issues",
        "Documentation": "https://github.com/Gressling/42001/blob/main/README.md",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Other Audience",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Dash",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "iso42001=iso42001.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "iso42001": ["*.md", "*.txt", "*.sql"],
    },
    zip_safe=False,
)