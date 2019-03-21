from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="japscandownloader",
    version="0.0.1",
    author="Louis Daviaud",
    description="Program to download mangas from JapScan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Harkame/JapScanDownloader",
    packages=find_packages(),
    classifiers=[
        "Manga downloader",
    ],
)
