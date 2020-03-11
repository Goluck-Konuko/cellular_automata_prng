import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name = "chaos",
    version = "1.0.0",
    author="Corentin Timal, Goluck konuko",
    author_email="cocotimal@gmail.com,goluckonuko@gmail.com",
    description="A PRNG using 3D cellular automata",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = ["numpy,os,itertools,operator"],
    python_requires='>=3.5',
)