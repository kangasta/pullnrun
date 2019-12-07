#!/usr/bin/python3

import setuptools

with open("README.md", "r") as f:
	long_description = f.read()

setuptools.setup(
	name="pullnrun",
	version="0.0.0",
	author="Toni Kangas",
	description="A simple python app for running a set of commands from remote sources and pushing result files to remote targets.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/kangasta/pull-n-run",
	packages=setuptools.find_packages(),
	package_data={
		'pullnrun': ['schema.json']
	},
	scripts=["bin/pullnrun"],
	install_requires=[
		"importlib_resources; python_version<'3.7'",
		"jsonschema",
		"requests"
	],
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	)
)