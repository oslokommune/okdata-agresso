from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="okdata-agresso",
    version="0.1.0",
    author="Oslo Origo",
    author_email="dataspeilet@oslo.kommune.no",
    description="Agresso data extractor for the Origo dataplatform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oslokommune/okdata-agresso",
    packages=find_packages(),
    install_requires=[
        "aws-xray-sdk",
        "okdata-aws>=2,<3",
        "okdata-sdk>=3.1,<4",
        "requests",
    ],
    python_requires=">=3.11",
)
