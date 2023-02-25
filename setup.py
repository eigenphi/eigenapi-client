# !/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import codecs
import os.path

with open("README.md", "r") as fh:
  long_description = fh.read()

def read(rel_path):
  here = os.path.abspath(os.path.dirname(__file__))
  with codecs.open(os.path.join(here, rel_path), 'r') as fp:
    return fp.read()

def get_version(rel_path):
  print("rel_path: " + rel_path)
  for line in read(rel_path).splitlines():
    if line.startswith('__version__'):
      delim = '"' if '"' in line else "'"
      return line.split(delim)[1]
  raise RuntimeError("Unable to find version string.")

setup(
  name="eigenapi_client",
  version=get_version("eigenapi_client/__init__.py"),
  author="David",
  author_email="david@eigenphi.com",
  description="EigenAPI Client",
  long_description_content_type="text/markdown",
  long_description=long_description,
  license="MIT",
  url="https://github.com/eigenphi/eigenapi-client",
  packages=['eigenapi_client','eigenapi_client/endpoints'],
  install_requires=[
    "setuptools >= 60.8.3",
    "wheel==0.36.2",
    "requests==2.24.0",
    "websockets==10.4"
  ],
  classifiers=[
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Topic :: Text Processing :: Indexing",
    "Topic :: Utilities",
    "Topic :: Internet",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
  ],
)
