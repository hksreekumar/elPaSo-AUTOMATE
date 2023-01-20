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

# Python imports


# Project imports
from automate.tools.cVisInterface import *
from automate.logging.cLoggingTestSuite import *

# Visualize logging to console
# Author: Harikrishnan Sreekumar
# Date: 18.12.2020
class cVisConsole(cVisInterface):
    # Constructor
    # Author: Harikrishnan Sreekumar
    # Date: 18.12.2020
    def __init__(self):
        self.consoleAbstractness = 'short'
    
    # Functions that writes to the console
    # Author: Harikrishnan Sreekumar
    # Date: 18.12.2020
    def print(self, information):
        print(information)
    
    # Print test suite summary
    # Author: Harikrishnan Sreekumar
    # Date: 18.12.2020
    def printTestSuiteSummary(self, testsuite):
        logTestSuite = cLoggingTestSuite(testsuite)
        Summary=logTestSuite.getSummary(self.consoleAbstractness)
        for i in range (0, int(len(Summary))):
            self.print(Summary[i])   
        
    # Print test suite general information
    # Author: Harikrishnan Sreekumar
    # Date: 18.12.2020
    def printTestSuiteGeneralInformation(self, testsuite):
        logTestSuite = cLoggingTestSuite(testsuite) 
        GeneralInformation=logTestSuite.getGeneralInformation(self.consoleAbstractness)
        for i in range (0,int(len(GeneralInformation))):
            self.print(GeneralInformation[i])
        
    # Print test suite results
    # Author: Harikrishnan Sreekumar
    # Date: 18.12.2020
    def printTestSuiteResults(self, testsuite):
        logTestSuite = cLoggingTestSuite(testsuite)
        TestSuiteResults=logTestSuite.getResults(self.consoleAbstractness)
        for i in range(0, int(len(TestSuiteResults))):
            self.print(TestSuiteResults[i])
          
    def generateVisualization(self,suite):
        self.generateOpeningVisualization(suite)
        self.generateEndingVisualization(suite)
    
    def generateOpeningVisualization(self,suite):
        print('------------------------ Begin Console Test Logs --------------------------------------------------------')
        self.printTestSuiteGeneralInformation(suite)

    def generateEndingVisualization(self,suite):  
        self.printTestSuiteSummary(suite)      
        self.printTestSuiteResults(suite)
        print('------------------------ End Console Test Logs ----------------------------------------------------------')