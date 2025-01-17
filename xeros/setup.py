from setuptools import setup, find_packages

setup(
    name="xeros",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "asyncio",
        "dataclasses",
        "typing",
    ],
    author="Xeros Team",
    description="Xeros - A Solana Development Assistant",
    python_requires=">=3.7",
)
