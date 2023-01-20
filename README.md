# AUTOMATE - An Automated Testing Framework for elPaSo 

Readme file contains necessary information for using and developing the code project. The contents are structured as per the following sections:

		[SECTION 01 - Introduction]
		[SECTION 02 - Installation]
		[SECTION 03 - Usage]
		[SECTION 04 - Software dependencies]
		[SECTION 05 - Python library dependencies]
		[SECTION 06 - Copyright information]
		

## Introduction

AUTOMATE is an automated Testing framework for elPaSo developed by Institute for Acoustics, TU Braunschweig, Germany. This project is aimed at automatically testing and verifying the proper functioning of elPaSo on every commit in a CI framework. AUTOMATE performs specific tests evaluate the update for different parameters such as accuracy, performance, etc by executing different acoustic benchmarks. The results from the different tests are then reported in various forms. Depending upon the user input, the AUTOMATE compares the results obtained with benchmarked results which can be from an old elPaSo version or results from a commercial software like ABAQUS.
   
## Installation

AUTOMATE is hosted in the PyPI package registry. Installation can be done via regular pip with command:

	python3 -m pip install automate --extra-index-url https://git.rz.tu-bs.de/api/v4/projects/3038/packages/pypi/simple

## Usage

	 For usage, run:
		python3 -m automate
		
	 Output 
	 	A complete pdf report is generated in the output folder at the end of the run and contains useful information on:
		 Summary of individual testcases
		 Name and location of all the testcases executed
		 Sucess and failure of different tests for each testcases
		 Error distribution (if any) in the results
		 Computational time as performance measure

	 Example: python3 -m automate -o ./output-folder -p /software/elPaSo/bin/ -c intel -b https://cloud.tu-braunschweig.de/s/J5HypDZZBYz6tcs/download/benchmarks.zip
	 Example with issue reporting: python3 automate.py -o ./output-folder -p /software/elPaSo/bin/ -c intel -b https://cloud.tu-braunschweig.de/s/J5HypDZZBYz6tcs/download/benchmarks.zip -r -g https://git.rz.tu-bs.de/ -i 10 -a $GITLAB_ISSUE_TOKERN
 
## Software dependencies

	 Software Requirements:
      Python3 - preferably ANACONDA distribution
	  elPaSo  - See elPaSo README in https://git.rz.tu-bs.de/akustik/elPaSo-Core/ for installation support
 
## Python library dependencies

	Python library dependencies: See requirements.txt

## Copyright information

Copyright (c) 2023. Authors listed in AUTHORS.md

This file is part of elPaSo-AUTOMATE.

elPaSo-AUTOMATE is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

elPaSo-AUTOMATE is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License along with elPaSo-AUTOMATE (COPYING.txt). If not, see <https://www.gnu.org/licenses/>. 
	
	


