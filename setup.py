from setuptools import setup, find_packages

setup(
    name="KinLuv",  
    version="1.0.0",  
    py_modules=["main"],
    packages=find_packages(),  
    install_requires=[
        "numpy==1.21.0",  
        "sympy==1.5.1",  
        "colorama==0.4.4",  
        "art==6.4",         
        "scipy==1.7.3",  
        "matplotlib==3.5.3",  
    ],
    entry_points={
        'console_scripts': [
            'kinluv = main:main',  # command line, you can run 'kinluv' from the terminal
        ],
    },
    description="A Python Toolkit for Modeling Multistate Kinetics in Thermally Activated Delayed Fluorescence (TADF) Systems.",  
    long_description=open('README.md').read(),  
    long_description_content_type="text/markdown",  
    author="Yue(Steven) He, Daniel Escudero",  
    author_email="daniel.escudero@kuleuven.be",  
    url="https://github.com/stevenuoa/KinLuv.git",  
    classifiers=[  
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",  
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.3',  
)

