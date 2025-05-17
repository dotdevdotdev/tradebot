from setuptools import setup, find_packages

setup(
    name="tradebot",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "SQLAlchemy>=2.0.27",
        "python-dotenv>=1.0.0",
        "anthropic>=0.8.1",
        "aiohttp>=3.9.1",
        "asyncio>=3.4.3",
    ],
    python_requires=">=3.8",
) 