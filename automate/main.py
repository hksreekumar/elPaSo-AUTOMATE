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

# General imports
import sys

# Project imports
from automate.help import printHelp
from automate.cTestHarness import *
from automate import config
from automate.covtools import displayIntelCodCovSummary

# Get current version of project
# Author: Harikrishnan Sreekumar
# Date: 05.10.2020
def getVersionString():
    pass

# Get current root directory
# Author: Harikrishnan Sreekumar
# Date: 05.10.2020
def getRoot():
    return os.path.dirname(os.path.realpath(__file__))

# Main script
# Author: Harikrishnan Sreekumar
# Date: 05.10.2020
def main(args):
    if '-displayIntelCodCovSummary' in args:
        displayIntelCodCovSummary.displayIntelCodeCov()
        sys.exit(0)
    else:
        print('Starting AUTOMATE...')
        # intializers
        config.pathSeparator = os.path.sep

        # check requirements for the used py-environment

        # develop test harness
        myHarnessProfile = cTestHarness()
        myHarnessProfile.setProfileConsoleConfigurations(args)
        myHarnessProfile.getBenchmarks()
        myHarnessProfile.prepareTestsInHarness()
        myHarnessProfile.deployTestsInHarness()
        myHarnessProfile.reportTestIssues()
        return_code = myHarnessProfile.produceExitCode()
        print('Exiting AUTOMATE and returning exit code ' + str(return_code))
        sys.exit(return_code)

if __name__ == '__main__':
    main(sys.argv[1:])
