from setuptools import setup, find_packages

setup(
    name='Quant Framework',
    version='0.0.1',
    packages=find_packages(),
    scripts=[],
    entry_points={
        "console_scripts": [
            "quant_framework=quant_framework.main:main"
        ],
    },
    install_requires=[]
)