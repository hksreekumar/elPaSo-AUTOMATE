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

# Class that defines the logging for a test-suite in general
# Author: Harikrishnan Sreekumar
# Date: 18.12.2020
class cLoggingTestSuite:
    # Constructor
    # Author: Harikrishnan Sreekumar
    # Date: 18.12.2020
    def __init__(self, suite):
        self.suite = suite
    
    # Define what to log as a general information about the testcase (nothing about results)
    # Author: Saurabh Rathore
    # Date: 13.01.2021
    def getGeneralInformation(self, abstractness='short'):
        GeneralInformation = []
        if abstractness in 'short':
            # Some short information to be returned
            GeneralInformation.append('Testcase Name:'+self.suite.suiteConfig["name"])
            GeneralInformation.append('Folder Name:'+self.suite.suiteConfig["name"]+
                                      '     Source:'+self.suite.systemUnderTest.system+
                                      '     Target:'+self.suite.systemTarget.system)
        elif abstractness in 'long':
            # Some long information to be returned
            GeneralInformation.append('================================================================================================')
            GeneralInformation.append('Testcase Name:' + self.suite.suiteConfig["name"] +'      Created On:'+str(self.suite.suiteConfig["date"]))
            GeneralInformation.append('================================================================================================')
            GeneralInformation.append('Description:'+self.suite.suiteConfig["description"])
            GeneralInformation.append('Folder Name:' + self.suite.suiteConfig["name"] +
                                      '     Source:' + self.suite.systemUnderTest.system +
                                      '     Target:' + self.suite.systemTarget.system)
            GeneralInformation.append('eLPaSo Path:'+str(self.suite.systemUnderTest.binaryPath) )
        return GeneralInformation
        
    # Define what to log about the test-suite results
    # Author: Saurabh Rathore
    # Date: 13.01.2021
    def getResults(self, abstractness='short'):
        Results=[]
        if abstractness in 'short':
            # Some short information to be returned
            Results.append('Test Type: '+self.suite.testType+'       Configured Tolerance: '+ str(self.suite.suiteConfig["tolerance"])+'       Test Result: '+self.suite.testResult)
        elif abstractness in 'long':
            # Some long information to be returned
            Results.append('Test Type: ' + self.suite.testType + '       Configured Tolerance: '+ str(self.suite.suiteConfig["tolerance"])+ '       Test Result: ' + self.suite.testResult)
        return Results
    
    # Define what to log as a full-summary (includes both general and result information)
    # Author: Saurabh Rathore
    # Date: 13.01.2021
    def getSummary(self, abstractness='short'):
        Summary=[]
        if abstractness in 'short':
            # Some short information to be returned
            Summary.append('Executable:'+ self.suite.systemUnderTest.system)
            Summary.append('Input/Output:'+self.suite.systemUnderTest.systemConfig["input_type"]+ '/' + self.suite.systemUnderTest.systemConfig["output_type"])
            Summary.append('Domain:'+ self.suite.systemUnderTest.systemConfig["analysis"])
        elif abstractness in 'long':
          # Some long information to be returned
            Summary.append('Executable:' + self.suite.systemUnderTest.system)
            Summary.append('Input/Output:' + self.suite.systemUnderTest.systemConfig["input_type"] + '/' +
                           self.suite.systemUnderTest.systemConfig["output_type"])
            Summary.append('Domain:' + self.suite.systemUnderTest.systemConfig["analysis"])
            Summary.append('--------------------------Source---------------------------')
            Summary=Summary+self.suite.systemUnderTest.binaryInfo
            Summary.append('--------------------------Target---------------------------')
            Summary = Summary +self.suite.systemTarget.binaryInfo
        return Summary
    