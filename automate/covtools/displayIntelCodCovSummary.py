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

import argparse

def displayIntelCodeCov():
    parser = argparse.ArgumentParser(description='Code to display intel code coverage summary')
    parser.add_argument('-displayIntelCodCovSummary','--displayIntelCodCovSummary', help='Outputs the intel code coverage',required=True)
    parser.add_argument('-f','--file', help='Input file name',required=True)
    args = parser.parse_args()

    ## show values ##
    print ("Input file: %s" % args.file )

    block_total = -100;
    block_cvrd = -100;
    block_uncvrd = -100;
    block_cvrg = -100;

    summarized = False

    lineno = 0
    with open(args.file) as f:
        lines = f.readlines()
        for line in lines:
            lineno = lineno + 1
            words = line.split()
            found = False
            for word in words:
                if word == "Blocks:":
                    found = True
            
            if found:
                toparse = lines[lineno+1]
                values =toparse.split()
                block_total = values[0];
                block_cvrd = values[1];
                block_uncvrd = values[2];
                block_cvrg = values[3];
                summarized = True
                
    if summarized:
        print('elPaSo summary of %s' % args.file)
        print('  Blocks:')
        print('    Total:     %s' % block_total)
        print('    Covered:   %s' % block_cvrd)
        print('    Uncovered: %s' % block_uncvrd)
        print('    Coverage:  %s' % block_cvrg)
    else:
        print('No summary found')
            
            