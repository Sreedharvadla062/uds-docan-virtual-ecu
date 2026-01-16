"""Setup configuration for uds-docan-virtual-ecu"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="uds-docan-virtual-ecu",
    version="0.1.0",
    author="Sreedharvadla",
    description="UDS (ISO 14229) client/server diagnostics over DoCAN (ISO 15765-2) using SocketCAN",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sreedharvadla062/uds-docan-virtual-ecu",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Topic :: Communications",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-can>=3.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.900",
        ],
    },
)
