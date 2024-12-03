from setuptools import setup, find_packages

setup(
    name='yfinance_utils',
    version='0.0.3',
    description='a few methods to help with tech analysis and plotting',
    license='GPL 2.0',
    packages=find_packages(),
    install_requires=['yfinance', 'pandas', 'matplotlib', 'PyQt6', 'numpy', 'requests_cache'],
    author='Lehi Gracia',
    author_email='dev@glgracia.com',
    keywords=['utils', 'technical analysis', 'finance'],
    url='https://github.com/devglg/yfinance_utils'
)