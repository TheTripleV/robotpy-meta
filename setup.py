#!/usr/bin/env python3

import glob
import sys

if sys.version_info < (3, 6):
    sys.stderr.write("ERROR: RobotPy requires Python 3.6+\n")
    exit(1)

import os
from os.path import dirname, exists, join
import subprocess
from setuptools import find_packages, setup
import glob

setup_dir = dirname(__file__)
git_dir = join(setup_dir, ".git")
base_package = "robotpy"
version_file = join(setup_dir, base_package, "version.py")

# Automatically generate a version.py based on the git version
if exists(git_dir):
    p = subprocess.Popen(
        ["git", "describe", "--tags", "--long", "--dirty=-dirty"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = p.communicate()
    # Make sure the git version has at least one tag
    if err:
        print("Error: You need to create a tag for this repo to use the builder")
        sys.exit(1)

    # Convert git version to PEP440 compliant version
    # - Older versions of pip choke on local identifiers, so we can't include the git commit
    v, commits, local = out.decode("utf-8").rstrip().split("-", 2)
    if commits != "0" or "-dirty" in local:
        v = "%s.post0.dev%s" % (v, commits)

    # Create the version.py file
    with open(version_file, "w") as fp:
        fp.write("# Autogenerated by setup.py\n__version__ = '{0}'".format(v))

if exists(version_file):
    with open(version_file, "r") as fp:
        exec(fp.read(), globals())
else:
    __version__ = "master"

all_reqs = set()

with open(join(setup_dir, "requirements.txt")) as requirements_file:
    install_requires = requirements_file.readlines()
    all_reqs |= set(install_requires)

extras_requires = {}

for fname in glob.glob(join(setup_dir, "*-requirements.txt")):
    key = fname[:-17]
    with open(fname) as fp:
        reqs = fp.readlines()

    extras_requires[key] = reqs
    all_reqs |= set(reqs)

extras_requires["all"] = all_reqs

with open(join(dirname(__file__), "README.md"), "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="robotpy",
    version=__version__,
    description="Meta package to make installing robotpy easier",
    long_description=long_description,
    author="RobotPy Development Team",
    author_email="robotpy@googlegroups.com",
    url="https://github.com/robotpy/robotpy-meta",
    license="BSD-3-Clause",
    packages=find_packages(),
    install_requires=install_requires,
    extras_require=extras_requires,
    requires_python=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing",
    ],
)
