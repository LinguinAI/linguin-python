from setuptools import re, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = re.search(
    "^__version__ = \((\d+), (\d+), (\d+)\)$",
    open('linguin/__init__.py', 'r').read(),
    re.MULTILINE
).groups()

setup(
    name="linguin",
    version='.'.join(version),
    author="Jan Schwenzien",
    author_email="jan@general-scripting.com",
    description="API wrapper for the language detection as a service Linguin AI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://linguin.ai/",
    project_urls={
        "Bug Tracker": "https://github.com/LinguinAI/linguin-python/issues",
        "Documentation": "https://linguin.ai/api-docs/v2/"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["linguin"],
    python_requires=">=3.6",
    install_requires=['requests']
)
