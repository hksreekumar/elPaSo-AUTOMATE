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
import matplotlib.pyplot as plt
# Basic imports
import sys
import configparser
import math
import numpy as np

# Project imports
from automate import config
from automate.system.cSystemInterface import cSystemInterface
from automate.system.cSystemElpaso import cSystemElpaso
from automate.system.cSystemAbaqus import cSystemAbaqus
from automate.math.mMathLibrary import *

# Class that defines a test suite
# Author: Harikrishnan Sreekumar
# Date: 09.10.2020
class cTestSuite(object):
    # Constructor
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def __init__(self, name, harnessconfig):
        self.harnessconfig = harnessconfig      # Global configuration
        self.systemUnderTest = None             # System under test - mostly elPaSo
        self.systemUnderTestCheckPassed = None  # System under test - container to allow execution if special dependencies are fulfilled
        
        self.systemTarget = None                # System targeted
        self.errorNorm = None                   # Error norm
        self.nodeMap = None                     # Node map between the SUT and SyT
        
        self.suiteConfig = {
            "author": "<empty>",
            "date": "<empty>",
            "name": "<empty>",
            "description": "<empty>",
            "dir": "<empty>",
            "tolerance": "<empty>"
        }                                       # Suite configuration

        self.suiteConfig["name"] = name         # Suite name
        
        self.testType = None                    # Type of test type. Supported: correctness, performance
        self.testResult = None                  # Variable to contain PASSED/FAILED/SKIPPED
        self.testRemark = ''                    # String to add test remarks
        self.testData = None                    # Container for detailed information of the test which is printed
        
        self.wordingCorrectness = "correctness"
        self.wordingPerformance = "performance"
        
        self.wordingPassed = "PASSED"
        self.wordingFailed = "FAILED"
        self.wordingSkipped = "SKIPPED"
        
        self.plots = []                         # Handle to contain all generated plots

    # Define the system under test
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def defineSystemUnderTestFromConfig(self, path):
        self.systemUnderTest = self.defineSystem(self.suiteConfig["stest"], path, True)
        
    # Define the system targetted
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def defineSystemTargetFromConfig(self):
        self.systemTarget = self.defineSystem(self.suiteConfig["starget"], 'unknown', False)
        
    # Define system according to the systemName
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def defineSystem(self, systemName, path, boolSUT):
        if 'elpaso' in systemName or 'elpasoC' in systemName:
            return cSystemElpaso(systemName, path, self.suiteConfig["name"], self.suiteConfig["dir"], boolSUT)
        elif 'abaqus' in systemName:
            return cSystemAbaqus(systemName, path, self.suiteConfig["name"], self.suiteConfig["dir"], boolSUT)
        else:
            print('Unknown system type')
            sys.exit(2)
            
    # Parse the configuration applicable for the suite
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def parseConfiguration(self,configpath):
        configpath = configpath + config.pathSeparator + 'configuration' + config.pathSeparator
        myConfig = configparser.ConfigParser()
        myConfig.read(configpath + config.pathSeparator + 'config.ini')

        self.suiteConfig["author"] = myConfig.get('info', 'author')
        self.suiteConfig["date"] = myConfig.get('info', 'date')
        self.suiteConfig["name"] = myConfig.get('info', 'name')
        self.suiteConfig["description"] = myConfig.get('info', 'description')

        self.suiteConfig["executeTestcase"]=myConfig.get('switch','execute')

        self.suiteConfig["stest"] = myConfig.get('SystemUnderTest', 'system')
        self.suiteConfig["starget"] = myConfig.get('SystemTarget', 'system')
        
        self.suiteConfig["tolerance"] = float(myConfig.get('verification', 'error_tolerance'))
                
        self.testType = myConfig.get('verification', 'test_type')
        if self.testType in self.wordingPerformance:
            self.suiteConfig["test_parallel"] =  myConfig.get('verification', 'test_parallel')
            self.suiteConfig["test_solver_tag"] =  myConfig.get('verification', 'test_solver_tag')
            self.suiteConfig["ref_performance"] = myConfig.get('SystemTarget', 'ref_performance')
        elif self.testType in self.wordingCorrectness:
            self.suiteConfig["compare_node_elpaso"] = float(myConfig.get('verification', 'compare_node_elpaso'))
            try:
                self.suiteConfig["starget_read_mode"] = myConfig.get('SystemTarget', 'read_mode')
            except:
                self.suiteConfig["starget_read_mode"] = 'dofmap'  # (12.2021) To be removed when benchmarks are updated
                            
        self.suiteConfig["dof"] = 'deprecated and will be removed in future' # int(myConfig.get('calculation', 'dof'))
        self.suiteConfig["loadNode"] = 'deprecated and will be removed in future' # float(myConfig.get('verification', 'loadNode'))

    def getExecutionStatusandTestType(self):
        return [self.suiteConfig["executeTestcase"],self.testType ]
        
    # Perform routines associated to SUT
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def performSystemUnderTest(self):
        # preparation
        self.systemUnderTest.parseConfiguration()
        self.systemUnderTestCheckPassed = self.systemUnderTest.performPreChecks()
        # main execution and interpretation
        if(self.systemUnderTestCheckPassed):
            if self.testType in self.wordingCorrectness:
                self.systemUnderTest.performCorrectnessTest()
            elif self.testType in self.wordingPerformance:
                self.systemUnderTest.performPerformanceTest(self.suiteConfig["test_parallel"], self.suiteConfig["test_solver_tag"], self.harnessconfig )
    
    # Perform routines associated to SyT
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def analyzeSystemTarget(self):
        self.systemTarget.parseConfiguration()
        if self.testType in self.wordingCorrectness:
            self.systemTarget.importFeResults(self.suiteConfig["starget_read_mode"])
        elif self.testType in self.wordingPerformance:
            self.systemTarget.importPerformanceResults(self.suiteConfig["ref_performance"], self.systemUnderTest)
        self.systemTarget.readBenchmarkLog()

    # Filter common solution space between the SUT and SyT
    # Author: Saurabh rathore
    # Date: 09.10.2020
    def filterTest(self):
        if self.testType in self.wordingCorrectness:            
            # create nodemap
            NodeSearch_Radius = 0.01
            self.nodeMap={}
    
            dataSuT = self.systemUnderTest.FeDataStructure
            dataSyT = self.systemTarget.FeDataStructure
            
            compare_node_elpaso=int(self.suiteConfig["compare_node_elpaso"])
            compare_node_elpaso_id = compare_node_elpaso-1
            for j in range(0, int(len(dataSyT.nodes))):
                if math.sqrt((dataSuT.nodes[compare_node_elpaso_id][0] - dataSyT.nodes[j][0]) ** 2 + (dataSuT.nodes[compare_node_elpaso_id][1] - dataSyT.nodes[j][1]) ** 2 + (dataSuT.nodes[compare_node_elpaso_id][2] - dataSyT.nodes[j][2]) ** 2) <= NodeSearch_Radius:
                    self.nodeMap[compare_node_elpaso]=j+1

            # match SUT and SyT
            dofIndexTarget = self.systemTarget.getDofIndexListForNode(self.nodeMap[compare_node_elpaso])
            dofIndexSource = self.systemUnderTest.getDofIndexListForNode(compare_node_elpaso)
            
            if dofIndexSource != dofIndexTarget:
                # more filtering
                if len(dofIndexTarget) == 6 and len(dofIndexSource) == 3: # known case of plate and shell mismatch
                    dofIndexTarget = dofIndexTarget[2::5]
                else:
                    print('ERROR! MISMATCH IN COMPARE FIELD')
                    sys.exit(1)

            self.sourceVector=np.zeros((dataSuT.solutionReal.shape[0], len(dofIndexSource)), dtype=complex)
            self.targetVector=np.zeros((dataSuT.solutionReal.shape[0], len(dofIndexTarget)), dtype=complex)

            for id,dof in enumerate(dofIndexTarget):
                self.targetVector[:,id] = dataSyT.solutionReal[:,dof] + 1j * dataSyT.solutionImag[:,dof]

            for id,dof in enumerate(dofIndexSource):
                self.sourceVector[:,id] = dataSuT.solutionReal[:,dof] + 1j * dataSuT.solutionImag[:,dof]
            
        elif self.testType in self.wordingPerformance:
            self.sourceVector = np.array(self.systemUnderTest.solvertime)
            self.targetVector = np.array(self.systemTarget.solvertime)

    # Verify if the test passed
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def verifyTest(self):
        if self.systemUnderTestCheckPassed:
            # check for type of test
            if self.testType in self.wordingCorrectness:
                self.performCorrectnessCheck()
            elif self.testType in self.wordingPerformance:
                self.performPerformanceCheck()
            else:
                print('    [Error] Unknown verification/test type: ' + self.testType)
                sys.exit(2)
            
            if self.testResult == None or self.testData == None:
                print('    [Error] Test result not set! ')
                sys.exit(2)
        else:
            self.testResult = self.wordingSkipped
            self.testRemark = self.testRemark + ' | Test is internally skipped due to unsatified dependencies from ldd symbols | '
            self.testData = [['Test Type','L2 Error Norm', 'Configured Tolerance', 'Test Result'],
                          [self.testType, '', self.suiteConfig["tolerance"], self.testResult]]
            
    # Function to perform Correctness check
    # Author: Harikrishnan Sreekumar
    # Date: 17.12.2020
    def performCorrectnessCheck(self):        
        # compute error norm
        self.errorNormOverFreq = []        
        for i in range(0, self.sourceVector.shape[0]): # for every frequency
             self.errorNormOverFreq.append(computeVectorNorm(self.sourceVector[i,:] - self.targetVector[i,:]))
        
        self.errorNorm = computeVectorNorm(self.errorNormOverFreq)

        # criteria for pass/fail
        if self.errorNorm >= self.suiteConfig["tolerance"]:
            self.testResult = self.wordingFailed
        else:
            self.testResult = self.wordingPassed
            
        # generate test data
        self.testData = [['Test Type','L2 Error Norm', 'Configured Tolerance', 'Test Result'],
                      [self.testType, self.errorNorm, self.suiteConfig["tolerance"], self.testResult]]
        self.FindLoadNodeData()
                      
    # Trial Function to plot only load case data
    # Author: Saurabh Rathore
    # Date: 12.08.2021
    def FindLoadNodeData(self): 
        if self.targetVector.shape[1] > 2:
            self.TArgetVectLoadPt = self.targetVector[:,2]
            self.SOurceVectLoadPt = self.sourceVector[:,2] 
        else:
            self.TArgetVectLoadPt = self.targetVector[:,0]
            self.SOurceVectLoadPt = self.sourceVector[:,0]  
        
    # Function to perform Performance check
    # Author: Harikrishnan Sreekumar
    # Date: 22.12.2020
    def performPerformanceCheck(self):
        self.errorNorm = computeVectorNorm(self.sourceVector - self.targetVector)/computeVectorNorm(self.sourceVector)
        # criteria for pass/fail
        if self.errorNorm  >= self.suiteConfig["tolerance"]:
            self.testResult = self.wordingFailed
        else:
            self.testResult = self.wordingPassed
            
        # generate test data
        self.testData = [['Test Type','L2 Error Norm', 'Configured Tolerance', 'Test Result'],
                      [self.testType, self.errorNorm , self.suiteConfig["tolerance"], self.testResult]]
        