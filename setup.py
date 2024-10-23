import setuptools
import os

this_folder = os.path.dirname(os.path.realpath(__file__))
requirements_file = this_folder + '/requirements.txt'
install_requires = []

if os.path.isfile(requirements_file):
    with open(requirements_file) as f:
        install_requires = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='flippydot',
     version='0.1.1',
     author="Chris Hemmings",
     description="A package that can be used to control AlfaZeta FlipDots",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/chrishemmings/flipPyDot",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     python_requires='>=3.6',
     install_requires=install_requires,
     license_file='LICENSE'
 )
