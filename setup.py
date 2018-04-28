from setuptools import setup, find_packages

from system_migrate import __version__

setup(name="system_migrate",
      version=__version__,
      packages=find_packages(),
      entry_points={
          "console_scripts": [
              "system-migrate=system_migrate.main.system_migrate:main"
          ]
      },
      install_requires=[
          "tabulate"
      ]
      )
