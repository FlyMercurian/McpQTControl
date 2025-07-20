#!/usr/bin/env python3
"""
MCP Qt控制服务器安装配置
"""

from setuptools import setup, find_packages

with open("README_MCP_SERVER.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mcp-qt-control",
    version="1.0.0",
    author="MCP Qt Control Team",
    author_email="support@example.com",
    description="MCP服务器用于控制Qt应用",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/mcp-qt-control",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mcp-qt-server=mcp_server:main",
            "mcp-qt-start=start_server:main",
            "mcp-qt-test=test_mcp_client:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 