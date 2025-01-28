from setuptools import setup, find_packages

setup(
    name="snake-game-lib",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    author="Snakecm",
    author_email="tanchishecm@hotmail.com",
    description="A flexible and extensible Snake game library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Snakecm/Snake",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 