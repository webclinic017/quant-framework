from setuptools import setup, find_packages

setup(
    name='quant-framework',
    version='0.0.2',
    author='Brendan Geck',
    author_email='bpgeck@gmail.com',
    url='https://github.com/brendangeck/quant-framework',
    description='A basic framework for backtesting and going live with quant strategies',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    scripts=[],
    entry_points={
        'console_scripts': [
            'quant_framework=quant_framework.main:main'
        ],
    },
    install_requires=[
        'SQLAlchemy==1.3.23'
    ]
)