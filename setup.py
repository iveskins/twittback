import sys
from setuptools import setup, find_packages

if sys.version_info.major < 2:
    sys.exit("Error: Please upgrade to Python3")

setup(name="twittback",
      version="0.1",
      description="Alternative twitter site",
      url="twittback.info",
      author="Dimitri Merejkowsky",
      author_email="d.merej@gmail.com",
      license="BSD",
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
        "attrs",
        "arrow",
        "feedgenerator",
        "flask",
        "path.py",
        "requests",
        "ruamel.yaml",
        "twitter",
      ],
      entry_points={
        "console_scripts": [
          "twittback = twittback.backupper:main",
        ]
      })
