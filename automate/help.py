# Copyright (c) 2023. Authors listed in AUTHORS.md
#
# This file is part of elPaSo-AUTOMATE.
#
# elPaSo-AUTOMATE is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# elPaSo-AUTOMATE is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along
# with elPaSo-AUTOMATE (COPYING.txt). If not, see
# <https://www.gnu.org/licenses/>. 

## AUTOMATE Automated Testing Framework for elPaSo
## The current file is a part of AUTOMATE code package
##
## Authors: Harikrishnan Sreekumar, Christopher Blech
## Property of : Institut für Akustik, TU Braunschweig, Germany
 
# Prints out usage help for the code package
# Author: Dominik Reifer
# Date: 01.04.2019
def printHelp():
    print('Usage:')
    print('')
    print('python verification.py -o <foldername> -p <path> -b <benchmark download url> -c <intel/gnu> [optional arguments] ')
    print('')
    print('Arguments (*mandatory):')
    print('-o <foldername>      -      *Sets the name for the output-folder')

    print('-p <path>            -      *Set the path for the elpasoC-binary location')
    print('-b <download url>    -      *Link to download benchmarks')
    print('-k                   -       Keep the calculated files afterwards')
    print('                             default: false, for saving memory')
    print('-v                   -       Export additionally as .tex-file')
    print('-s                   -       Test one ore more specific testcases (preferred cases will be prompted)')
    print('-c <intel/gnu>       -      *Run in ci-pipeline mode')
    print('-t <testType>        -       Defines the test types to be executed. corr - Correctness, per - Performance, all - for both Correctness and Performance')
    print('                             default: both Correctness and Performance')
    print('-r                   -       If provided issues (if any are communicate to gitlab repos)')
    print('                             Option is activated only in CI env')
    print('                             default: OFF')
    print('-g <git domain url>  -       Git domain for issue reporting. eg: https://git.rz.tu-bs.de/ [use with -r]')
    print('-i <project id>      -       Git project ID. See your project Settings > General > Project ID. eg: 10  [use with -r]')
    print('-d <local git path>  -       Path to your local elPaSo git repository [use with -r]')
    print('-m <path to mpi>     -       Path to your mpi support - required for performance tests eg: /software/openmpi/bin/mpirun')