from setuptools import setup, find_packages

setup(
    name='yfinance_utils',
    version='0.0.4',
    description='a few utilities to help with tech analysis and plotting',
    license='GPL 2.0',
    packages=find_packages(),
    install_requires=['yfinance', 'pandas', 'finta', 'plotly'],
    author='Lehi Gracia',
    author_email='dev@glgracia.com',
    keywords=['utils', 'technical analysis', 'finance'],
    url='https://github.com/devglg/yfinance_utils'
)