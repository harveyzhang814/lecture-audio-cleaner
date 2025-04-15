"""
Setup script for the Lecture Audio Cleaner package.
"""
from setuptools import setup, find_packages

setup(
    name="lecture-audio-cleaner",
    version="0.1.0",
    description="An audio processing tool for cleaning lecture recordings",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "librosa>=0.10.0",
        "soundfile>=0.12.1",
        "noisereduce>=2.0.0",
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "PyQt5>=5.15.0",
        "pydub>=0.25.1",
    ],
    entry_points={
        "console_scripts": [
            "lecture-audio-cleaner=src.main:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 