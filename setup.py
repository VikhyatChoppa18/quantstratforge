from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quantstratforge",
    version="0.2.1",
    author="Venkata Vikhyat Choppa",
    author_email="",
    description="Privacy-preserving agentic SLM for quant strategy forging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VikhyatChoppa18/QuantStratForge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.12",
    install_requires=[
        "torch>=2.0.0,<3.0.0",
        "transformers>=4.38.0,<5.0.0",
        "datasets>=2.14.0,<3.0.0",
        "accelerate>=0.21.0,<1.0.0",
        "peft>=0.5.0,<1.0.0",
        "bitsandbytes>=0.41.0,<1.0.0",
        "fastapi>=0.95.0,<1.0.0",
        "uvicorn>=0.22.0,<1.0.0",
        "huggingface_hub>=0.17.0,<1.0.0",
        "flower>=2.0.0,<3.0.0",
        "flwr>=1.8.0,<2.0.0",
        "yfinance>=0.2.0,<1.0.0",
        "pandas-ta>=0.4.67b0,<1.0.0",
        "websockets>=12.0.0,<16.0.0",
    ],
    extras_require={
        "demo": [
            "streamlit>=1.28.0,<2.0.0",
            "plotly>=5.15.0,<6.0.0",
            "seaborn>=0.12.0,<1.0.0",
            "matplotlib>=3.7.0,<4.0.0",
        ],
        "dev": [
            "pytest>=8.4.2,<9.0.0",
            "black>=25.9.0,<26.0.0",
            "ruff>=0.13.3,<0.14.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "quantstratforge=quantstratforge.cli:main",
        ],
    },
    keywords="quantitative,trading,ai,machine-learning,finance,privacy,federated-learning",
)
