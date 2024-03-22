import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lgtv-rs232-zcline91",
    version="0.0.1",
    author="Zachary Cline",
    author_email="zachcline@gmail.com",
    description="A small package for controlling my LG TV through its serial port",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.example.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Unix",
    ],
)