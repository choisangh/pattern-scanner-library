import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PUT YOUR PACKAGE NAME", ## 소문자 영단어
    version="0.0.1", ##
    author="PUT YOUR NAME", ## ex) Sunkyeong Lee
    author_email="PUT YOUR EMAIL ADDRESS", ##
    description="PUT THE PACKAGE DESCRIPTION", ##
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="PUT YOUR GITHUB REPO LINK", ##
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)