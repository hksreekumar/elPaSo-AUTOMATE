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
import sys, os
import getopt
import shutil
from zipfile import ZipFile

# Project imports
from automate import config
from automate.help import printHelp
from automate.testconfigs.cHarnessConfiguration import *
from automate.testsuite.cTestSuite import *
from automate.tools.cVisTex import *
from automate.tools.cVisConsole import *
from automate.tools.cVisLogFile import *
from automate.tools.cIssueGitLab import *

# Test Harness: Is a class for creating the required harness for conduting a number of tests automatically
# Author: Harikrishnan Sreekumar
# Date: 06.10.2020
class cTestHarness():
    # Constructor
    # Author: Harikrishnan Sreekumar
    # Date: 06.10.2020
    def __init__(self):
        self.executedTestsuits=[]
        self.testsuites = None                          # List of test cases to be tested in the harness
        self.configuration = cHarnessConfiguration()    # Object for the harness configuration
        self.setProfileBasicConfigurations()            # By default: load the basic configuration file to the harness
        self.testing = ['correctness','performance']    # defines the test types to be executed
        self.disabledTestsuits=[]
        self.benchmarksDir = None
        self.issueGitRepos = None
        self.issueGitReposProjectID = None
        self.issueGitLocaReposDirectory = None
        
    # Sets the basic configuration from file
    # Author: Harikrishnan Sreekumar
    # Date: 06.10.2020
    def setProfileBasicConfigurations(self):
        #self.configuration.readConfiguration()          #  get config from config.ini
        pass
    
    # setProfileConsoleConfigurations: Parse the console line flags
    # Author: Dominik Reifer
    # Date: 01.04.2019
    def setProfileConsoleConfigurations(self, argv):
        try:
            opts, args = getopt.getopt(argv,'o:c:t:srkp:g:b:d:i:m:',['ofolder=','path','testing='])
        except getopt.GetoptError:
            print('ERROR! Passed arguments contain error or are incomplete')
            printHelp()
            sys.exit(2)

        #print(opts)
        #print(argv)
        #exit()
        for opt, arg in opts:
            #print(opt)
            if opt == '-h':
                printHelp()
                sys.exit()
            elif opt in ("-o", "--ofolder"):
                self.configuration.outputDirectory = arg
            elif opt in ("-p", "--path"):
                self.configuration.binaryPath = arg
            elif opt == '-k':
                self.configuration.boolKeepFiles = True
            elif opt == '-r':
                self.configuration.boolReportIssueGitlab = True
            elif opt == '-v':
                self.configuration.boolExportTexReport = False
            elif opt == '-s':
                self.configuration.boolSpecificTestRun = True
            elif opt == '-c':
                self.configuration.CIEnvironment = arg
                self.setProfileBasicConfigurations()            # Reconfgiure
            elif opt in ("-t", "--self.testing"):
                if arg=='corr':
                    self.testing=['correctness']
                    self.configuration.boolRunCorrectnessTests = True
                    self.configuration.boolRunPerformanceTests = False
                elif arg=='per':
                    self.testing=['performance']
                    self.configuration.boolRunCorrectnessTests = False
                    self.configuration.boolRunPerformanceTests = True
                elif arg=='all':
                    self.testing=['correctness','performance']
                    self.configuration.boolRunCorrectnessTests = True
                    self.configuration.boolRunPerformanceTests = True
                else:
                    printHelp()
                    sys.exit()
            elif opt in ("-b"):
                self.benchmarksDir = arg
            elif opt in ("-g"):
                self.issueGitRepos = arg
            elif opt in ("-i"):
                self.issueGitReposProjectID = arg
            elif opt in ("-d"):
                self.issueGitLocaReposDirectory = arg
            elif opt in ("-m"):
                self.configuration.mpiPath = arg
        try:
            self.configuration.assertConfiguration()
        except:
            print('Configuration incomplete. Please check if all required flags are passed')
            printHelp()
            sys.exit(2)
    
    # Downloads the benchmarks from the cloud
    # Author: Harikrishnan Sreekumar
    # Date: 15.12.2021
    def getBenchmarks(self):
        if self.benchmarksDir is not None:
            print('Fetching benchmarks...')
            # get benchmarks from cloud
            try:
                os.system('rm *.zip*')
                os.system('rm -r ./benchmarks')
            except:
                pass
            if not os.path.exists('./benchmarks.zip'):
                os.system('wget --no-check-certificate ' + self.benchmarksDir) # download from test
            zf = ZipFile('./benchmarks.zip', 'r')
            zf.extractall()
            zf.close()
            #os.system('rm *.zip')
        else:
            print('Fetching benchmarks... failed. Provide download link for downloading benchmarks')
            printHelp()
            sys.exit(1)
            

    # Sets a list of test suites
    # Author: Dominik Reifer
    # Date: 01.04.2019
    def prepareTestsInHarness(self):
        self.testsuites = []
        # open all cases
        if not self.configuration.boolSpecificTestRun:
            for suite_name in sorted(os.listdir(config.baseDir + config.pathSeparator + config.testSuiteFolderName + config.pathSeparator)):
                self.testsuites.append( cTestSuite(suite_name, self.configuration))
        else:
            print('Implemented testsuites:')
            for suite_name in os.listdir(config.baseDir + config.pathSeparator + config.testSuiteFolderName + config.pathSeparator):
                self.testsuites.append( cTestSuite(suite_name, self.configuration))
            for i in range(len(self.testsuites)):
                print('{:d} - {:s}'.format(i, str(self.testsuites[i].suiteConfig["name"])))
            print('')
            print('Type in the numbers of the suites you want to verify seperated with commas (i.e.: 1,3,4,..) and hit Enter afterwards')
            raw_input = input()
            raw_input =(map(int, raw_input.strip('[]').split(',')))

            print('The following cases will be verified:')
            cases_tmp = self.testsuites
            self.testsuites = []
            for num in raw_input:
                self.testsuites.append(cases_tmp[num])
                
    # Sets the folder structure
    # Author: Dominik Reifer
    # Date: 01.04.2019
    def createHarnessBaseDirectoryStructure(self):
        output_folder = self.configuration.outputDirectory + config.pathSeparator + config.outputFolderName
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if not os.path.exists(output_folder + '/plots'):
            os.makedirs(output_folder + '/plots')
        if not os.path.exists(output_folder + '/reports'):
            os.makedirs(output_folder + '/reports')
        if not os.path.exists(output_folder + '/calculation'):
            os.makedirs(output_folder + '/calculation')
        if not os.path.exists(output_folder + '/logs'):
            os.makedirs(output_folder + '/logs')

        for suite in self.testsuites:
            suite.suiteConfig["dir"] = output_folder + '/calculation/' + suite.suiteConfig["name"]
            os.system(
                'cp -r ' + config.baseDir + config.pathSeparator + config.testSuiteFolderName + config.pathSeparator +
                suite.suiteConfig["name"] + ' ' + output_folder + '/calculation')

    def createTestcaseSpecificSubdirectories(self,suite):
        output_folder = self.configuration.outputDirectory + config.pathSeparator + config.outputFolderName
        suite.suiteConfig["dir"] = output_folder + '/calculation/' + suite.suiteConfig["name"]
        os.system('cp -r ' + config.baseDir + config.pathSeparator + config.testSuiteFolderName + config.pathSeparator + suite.suiteConfig["name"] + ' ' + output_folder + '/calculation')

    # Deploy routine for all suites
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def deployTestsInHarness(self):
        print('Starting to deploy...')
        self.logConsoleCommunication = cVisConsole()    # Communication to console
        output_dir = self.configuration.outputDirectory + config.pathSeparator + config.outputFolderName;
        self.logLogFileCommunication = cVisLogFile(output_dir) # Communication to logfile 

        self.createHarnessBaseDirectoryStructure()

        # parse all configurations and print
        # print suite info
        print('> Following testuites will be executed:')
        for suite in self.testsuites:
            testConfigPath = config.baseDir + '/benchmarks/' + suite.suiteConfig["name"]
            suite.parseConfiguration(testConfigPath)         # Recognize the configurations from config file
            [execute,testType] = suite.getExecutionStatusandTestType()
            if execute == 'True' and testType in self.testing:
                print(' > ' + str(testType) + ' | ' + suite.suiteConfig["name"])

        for suite in self.testsuites:            
            [execute,testType] = suite.getExecutionStatusandTestType()
            if execute == 'True' and testType in self.testing:
                self.executedTestsuits.append(suite)
                suite.defineSystemUnderTestFromConfig(
                    self.configuration.binaryPath)  # Based on the configuration, sets the SUT
                suite.defineSystemTargetFromConfig()  # Based on the configuration, sets the targeted system
                self.logConsoleCommunication.generateOpeningVisualization(suite)
                suite.performSystemUnderTest()  # Conducts the execution of SUT
                if suite.systemUnderTestCheckPassed:
                    suite.analyzeSystemTarget()  # Analyze the target (execution is not done)
                    suite.filterTest()  # Filters the results according to available input output

                suite.verifyTest()  # Performs the verification and calculates the error

                self.logConsoleCommunication.generateEndingVisualization(suite)
                self.logLogFileCommunication.generateVisualization(suite)

                if not self.configuration.boolKeepFiles:  # Remove temporary files to save memory
                    os.system('rm -r ' + suite.suiteConfig["dir"])
            elif execute == 'False' and testType in self.testing:
                self.disabledTestsuits.append(suite)
        print('Starting to deploy... Finished.')
        
        print('Starting to export...')
        if self.configuration.boolExportTexReport:
            visExport = cVisTex(self)
            visExport.generateVisualization(self.executedTestsuits,self.disabledTestsuits)
        else:
            print('Unrecognized export routine')

        print('Starting to export... Finished.')
    
    # Report issue if requested
    # Author: Harikrishnan Sreekumar
    # Date: 28.07.2021
    def reportTestIssues(self):
        if self.configuration.boolReportIssueGitlab and self.issueGitRepos is not None and self.issueGitReposProjectID is not None and self.issueGitLocaReposDirectory is not None:
            print('Checking for issues...\n')
            issuemanager = cIssueGitLab(self.issueGitRepos, self.issueGitReposProjectID, self.issueGitLocaReposDirectory)
            suitetype = self.executedTestsuits[0].testType
            for suite in self.executedTestsuits:
                if suite.testResult in suite.wordingFailed:
                    issuemanager.addBenchmarkToIssueList(suite.suiteConfig["name"])
                if suitetype != self.executedTestsuits[0].testType:
                    print('Error! Mixed tests. Disable issue reporting or conduct one type of test!\n')
                    sys.exit()
            
            print('Reporting issues...\n')
            bstringlist = issuemanager.getBenchmarkListAsString()
            #print(bstringlist)
            buildcase = self.configuration.CIEnvironment.capitalize() 
            if len(bstringlist) != 0:
                if suitetype == self.executedTestsuits[0].wordingCorrectness:
                    issuemanager.setAutomateIntegrationIssue(bstringlist,buildcase)
                elif suitetype == self.executedTestsuits[0].wordingPerformance:
                    issuemanager.setAutomatePerformanceIssue(bstringlist,buildcase)
                issuemanager.reportGitlabIssue()
            
            print('Reporting issues... done.\n')
        else:
            print('Issue reporting skipped or incomplete info.\n')

    # Check for overall test result
    # Author: Harikrishnan Sreekumar
    # Date: 17.12.2020
    def getOverallTestResult(self,executedTestsuits):
        tmpResult = executedTestsuits[0].wordingPassed
        for suite in executedTestsuits:
            if suite.testResult in suite.wordingFailed:
                tmpResult = suite.wordingFailed
        
        return tmpResult
        
    # Issue a suitable exit code
    # Author: Harikrishnan Sreekumar
    # Date: 22.12.2020
    def produceExitCode(self):
        wordingFailed = self.testsuites[0].wordingFailed
        if self.getOverallTestResult(self.executedTestsuits) in wordingFailed:
            print('AUTOMATE exiting with error code 1 [Failure]')
            return 1
        else:
            print('AUTOMATE exiting with error code 0 [Success]')
            return 0

        return 0
           
