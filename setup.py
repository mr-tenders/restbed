"""
setup module for restbed
"""
from setuptools import setup, find_packages

setup(
    name="restbed",
    version="0.0.1",
    description=(
        "REST API wrapper for SANE network scanners"
    ),
    keywords="scanner rest api",
    packages=find_packages(exclude=["example", "test"]),
    author="Samantha Enders",
    author_email="sammienders@outlook.com",
    entry_points={
        "console_scripts": ["restbed.restbed:main"]
    },
    install_requires=[
        "flask",
        "pyinsane"
    ]
)
