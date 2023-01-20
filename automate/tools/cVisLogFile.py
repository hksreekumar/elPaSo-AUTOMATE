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
from automate import config

# Visualize logging to a file
# Author: Harikrishnan Sreekumar
# Date: 18.12.2020
class cVisLogFile(cVisInterface):
    # Constructor
    # Author: Harikrishnan Sreekumar
    # Date: 18.12.2020
    def __init__(self, output_folder):
        self.filename = str(output_folder)+'/logs/'+str(config.logfileName)
        self.logFileAbstractness = 'long'
        
    # Write information
    # Author: Saurabh Rathore
    # Date: 13.01.2021
    def write(self, information):
        logfile=open(self.filename,"a+")
        for i in range(0,int(len(information))):
            logfile.write(information[i])
            logfile.write('\n')
        logfile.close()
    
    # Write test suite summary
    # Author: Harikrishnan Sreekumar
    # Date: 18.12.2020
    def writeTestSuiteSummary(self, testsuite):
        logTestSuite = cLoggingTestSuite(testsuite)
        self.write(logTestSuite.getSummary(self.logFileAbstractness))        
        
    # Write test suite general information
    # Author: Harikrishnan Sreekumar
    # Date: 18.12.2020
    def writeTestSuiteGeneralInformation(self, testsuite):
        logTestSuite = cLoggingTestSuite(testsuite)
        self.write(logTestSuite.getGeneralInformation(self.logFileAbstractness))       
        
    # Write test suite results
    # Author: Harikrishnan Sreekumar
    # Date: 18.12.2020
    def writeTestSuiteResults(self, testsuite):
        logTestSuite = cLoggingTestSuite(testsuite)
        self.write(logTestSuite.getResults(self.logFileAbstractness))    

    def generateVisualization(self, suite):
        self.writeTestSuiteGeneralInformation(suite)
        self.write(['------------------------------------------------------------------------------------------------'])
        self.writeTestSuiteSummary(suite)
        self.write(['------------------------------------------------------------------------------------------------'])
        self.writeTestSuiteResults(suite)
        self.write('\n')  