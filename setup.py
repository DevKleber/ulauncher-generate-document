from setuptools import setup, find_packages

setup(
    name='document-generator-extension',
    version='1.0.0',
    description='Extensão do Ulauncher para gerar CPF, CNPJ e dados completos de pessoa',
    author='Seu Nome',
    author_email='seu.email@example.com',
    packages=find_packages(),
    install_requires=[
        'Faker>=15.0.0'
    ],
    entry_points={
        'ulauncher.extension': [
            'document_generator = document_generator:DocumentGeneratorExtension'
        ]
    },
)
