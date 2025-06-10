"""
Setup script for the IQ Option Startup Project.
"""
from setuptools import setup, find_packages

setup(
    name="iqoption_startup",
    version="0.1.0",
    description="A Python package for automated trading on the IQ Option platform",
    author="IQ Option Startup Team",
    author_email="example@example.com",
    packages=find_packages(),
    install_requires=[
        # Use the GitHub repository for iqoptionapi
        "iqoptionapi @ git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git@master#egg=iqoptionapi",
        "python-dotenv>=0.21.1",
        "pandas>=1.5.3",
        "numpy>=1.24.3",
        "urllib3>=1.26.16,<2.0.0",
        "requests>=2.28.2",
        "websocket-client>=1.5.1",
        "python-dateutil>=2.8.2",
        "pytz>=2023.3",
    ],
    entry_points={
        "console_scripts": [
            "iqoption-trade=iqoption_startup.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)
