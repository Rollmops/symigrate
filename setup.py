from setuptools import setup, find_packages

from symigrate import __version__

DESCRIPTION = """A flyway-like tool that allows migration of scripts to a system."""

setup(
    name="symigrate",
    version=__version__,
    description=DESCRIPTION,
    author="Erik Tuerke",
    author_email="etuerke@googlemail.com",
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
