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

# Basic imports
import configparser

# Project imports
from automate import config

# Test configuration: Class to contain the configuration for the harness
# Author: Harikrishnan Sreekumar
# Date: 06.10.2020
class cHarnessConfiguration(object):
    # Constructor
    # Author: Harikrishnan Sreekumar
    # Date: 06.10.2020
    def __init__(self):
        self.outputDirectory = None             # Ouput directory for the test harness
        self.boolKeepFiles = False              # [False]: Test harness will not save the computated files (memory saving)
        self.boolExportTexReport = True         # [True] : Generates a TEX (cons. PDF) report summarizing all the tests
        self.boolSpecificTestRun = False        # [False]: Runs only the specified tests
        self.configFileName = 'config.ini'      # Name of the configuration file
        self.configFilePath = config.baseDir    # Path where the configuration file is placed
        self.binaryPath = ''                    # User defined path to the binary
        self.CIEnvironment = None               # Use setting for CI pipeline
        self.boolRunCorrectnessTests= True
        self.boolRunPerformanceTests = True
        self.boolReportIssueGitlab = False      # [False]: By default no issues are communicated
        self.mpiPath = None                     # MPI path

    # Read Configuration from file    
    # Author: Dominiik Reifer
    # Date: 01.04.2020
    def readConfiguration(self):
        myConfigParser = configparser.ConfigParser()
        myConfigParser.read(self.configFilePath + config.pathSeparator + self.configFileName)
        # nothing to read from general configuration
        if self.CIEnvironment in ['intel','gnu']:
            self.configMap = {}
            self.configMap["intel"] = myConfigParser.get('mpi','intel_mpirun')
            self.configMap["gnu"] = myConfigParser.get('mpi','openmpi_mpirun')
        
    # Assert if all configurations are proper for the start
    # Author: Harikrishnan Sreekumar
    # Date: 06.10.2020
    def assertConfiguration(self):
        assert self.outputDirectory
        if self.boolRunPerformanceTests:
            assert self.mpiPath

    # Returns a summary of harness configs
    # Author: Harikrishnan Sreekumar
    # Date: 06.10.2020
    def getConfigurationString(self):
        return ("-- Test Harness ------------------------------------------" + "\n" + 
                "ConfigName:                        " + self.configFileName + "\n" + 
                "ConfigPath:                        " + self.configFilePath + "\n" +
                "ExportTex:                         " + str(self.boolExportTexReport) + "\n" +
                "SpecificTestRun:                   " + str(self.boolSpecificTestRun) + "\n" +
                "KeepFiles:                         " + str(self.boolSpecificTestRun) + "\n" +
                "CI Environment:                    " + str(self.boolUseCIEnvironment)                
               )