from setuptools import setup, find_packages

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='llm-predictive-router',
    version='0.1',
    description='A package to route chat requests between LLMs based on prompt classification',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/csabakecskemeti/llm_predictive_router_package",
    author='Csaba Kecskemeti - devquasar.com',
    packages=find_packages(),
    install_requires=[
        "torch>=1.9.0",         # Mandatory PyTorch dependency
        "transformers>=4.0.0",  # Transformers for model and pipeline support
        "openai",               # OpenAI API client
        "datasets",             # Huggingface datasets library
    ],    
    python_requires='>=3.7',
)

