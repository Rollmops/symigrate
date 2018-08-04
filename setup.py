from setuptools import setup, find_packages

from symigrate import __version__, __description__, __author__, __author_email__

setup(
    name="symigrate",
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__author_email__,
    license="Apache2",
    classifiers=[
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console"
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "symigrate=symigrate.main.symigrate:main"
        ]
    },
    install_requires=[
        "tabulate"
    ]
)
