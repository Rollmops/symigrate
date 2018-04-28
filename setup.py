from setuptools import setup, find_packages

from symigrate import __version__

setup(name="symigrate",
      version=__version__,
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
