from setuptools import setup, find_packages

setup(
    name="automaweb", # Nome que será usado no 'pip install'
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "selenium",
        # tkinter e os já vêm com o Python, não precisa listar
    ],
    author="João Braga",
    description="Biblioteca para automação Web e gerenciamento de arquivos",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
)