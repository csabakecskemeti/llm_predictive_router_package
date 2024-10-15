from setuptools import setup, find_packages

setup(
    name='llm-predictive-router',
    version='0.1',
    description='A package to route chat requests between LLMs based on prompt classification',
    author='Csaba Kecskemeti - devquasar.com',
    packages=find_packages(),
    install_requires=[
        'openai',
        'datasets',
        'transformers'
    ],
    python_requires='>=3.7',
)

