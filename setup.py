from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='yueutils',
    version='0.2.0',
    author='Alex',
    description='Common utility functions for Python projects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='afl-3.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.8',
    install_requires=[
        "toml>=0.10.0",
        "jsonlines>=3.0.0",
        "polars>=1.4.1,<2.0.0",
        "datasets>=2.21.0,<3.0.0",
        "loguru>=0.6.0",
        "pandas>=1.3.0",
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.950',
        ],
        'deeplearning': [
            'torch>=2.0.0',
            'deepspeed>=0.10.0',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Academic Free License (AFL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)