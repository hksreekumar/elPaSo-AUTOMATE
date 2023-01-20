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

# Basic import
import os, sys
import glob
import pandas as pd
import numpy as np

# Project import
from automate import config
from automate.system.cSystemInterface import *
from automate.datastructure.cFeDataStructure import *

# System class for Abaqus functionalities
# Author: Harikrishnan Sreekumar
# Date: 09.10.2020
class cSystemAbaqus(cSystemInterface):
    # Parse the configuration applicable for the system
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def parseConfiguration(self):
        self.systemConfig = {}
    
    # Call the system binary for computation
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def computeResults(self):
        print('Computing cannot be performed from the current python environment')

    # Imports the FE results of the current system into the datastructure
    # Author: Harikrishnan Sreekumar, Saurabh Rathore
    # Date: 09.10.2020
    def importFeResultsDeprecated(self, numDofsPerNode):
        self.FeDataStructure = cFeDataStructure()
        print('Analyzing abaqus generated files...')

        freqFiles = (glob.glob(self.modelPath + config.pathSeparator + 'Benchmarked'  + config.pathSeparator + '*.csv'))  # gets list of all abaqus CSV results files
        os.chdir(self.modelPath + config.pathSeparator + 'Benchmarked')
        freqFilesTemp = glob.glob('*.csv') 
        os.chdir(config.baseDir)
        freqFilesTemp = map(lambda each: each.strip(".csv"), freqFilesTemp)
        freqSteps = list(map(float, freqFilesTemp))
        freqSteps.sort()
        freqSteps.pop(0)

        targetData = pd.read_csv(freqFiles[0])
        numDofs = targetData.shape[0]*numDofsPerNode

        self.FeDataStructure.freqSteps = freqSteps
        self.FeDataStructure.solutionReal = np.zeros((len(freqSteps), numDofs))
        self.FeDataStructure.solutionImag = np.zeros((len(freqSteps), numDofs))
        self.FeDataStructure.nodes = np.zeros((targetData.shape[0], 3))

        nodesMaped=False

        for iStep in range(0,len(freqSteps)):
            #print('reading freqFiles[iStep]###############'+str(freqSteps[iStep])+ '*.csv')
            targetData = pd.read_csv(self.modelPath + config.pathSeparator + 'Benchmarked/'+str(freqSteps[iStep])+ '.csv')
            if not nodesMaped:
                self.FeDataStructure.nodes[:,0] = targetData.x2
                self.FeDataStructure.nodes[:,1] = targetData.y2
                self.FeDataStructure.nodes[:,2] = targetData.z2
                nodesMaped = True

            targetReal=[]
            targetImaginary=[]
            for j in range(0, targetData.shape[0]):
                for col in targetData.columns[3::2]:  # skipping first three entries as it contains x y yz coordinated
                    targetReal.append(float(targetData[col][j]))
                for col in targetData.columns[4::2]:  # skipping first
                    targetImaginary.append(float(targetData[col][j]))

            self.FeDataStructure.solutionReal[iStep,:] = targetReal
            self.FeDataStructure.solutionImag[iStep,:] = targetImaginary

        print('Analyzing abaqus generated files... Finished.')
    
    # Imports the FE results of the current system into the datastructure using dofmaps
    # Author: Harikrishnan Sreekumar
    # Date: 14.10.2020
    def importFeResultsUsingDofMaps(self):
        self.FeDataStructure = cFeDataStructure()
        print('Analyzing abaqus generated files from dof maps...')

        dofmap = np.loadtxt(self.modelPath + config.pathSeparator + 'Benchmarked'  + config.pathSeparator + 'abaqus_dofmap.dat', delimiter=',')

        freqFiles_U = (glob.glob(self.modelPath + config.pathSeparator + 'Benchmarked'  + config.pathSeparator + 'U_*.csv'))  # gets list of all abaqus CSV results files
        freqFiles_POR = (glob.glob(self.modelPath + config.pathSeparator + 'Benchmarked'  + config.pathSeparator + 'POR_*.csv'))
        # bools
        BOOL_U_RESULTS = False
        BOOL_POR_RESULTS = False
        # node counters
        all_nodes = {}
        if len(freqFiles_U):
            BOOL_U_RESULTS = True
        if len(freqFiles_POR):
            BOOL_POR_RESULTS = True

        # read all results to data
        ###### U DATA                
        data_u_freq = []
        if BOOL_U_RESULTS:
            os.chdir(self.modelPath + config.pathSeparator + 'Benchmarked')
            freqFilesTemp = glob.glob('U_*.csv') 
            os.chdir(config.baseDir)
            freqFilesTemp = map(lambda each: each.strip(".csv"), freqFilesTemp)
            freqFilesTemp = map(lambda each: each.strip("U_"), freqFilesTemp)
            freqSteps = list(map(float, freqFilesTemp))
            freqSteps.sort()
            freqSteps.pop(0)
            #print('> Reading U dofs...')
            self.FeDataStructure.freqSteps = freqSteps
            for iStep in range(0,len(freqSteps)):
                targetData = pd.read_csv(self.modelPath + config.pathSeparator + 'Benchmarked/U_'+ str(freqSteps[iStep])+ '.csv')
                mappeddata_u_freq = {}
                for iLabel in range(targetData.shape[0]):
                    array = []
                    currNode = int(targetData['label'][iLabel])
                    for col in targetData.columns[1:]:
                        array.append(targetData[col][iLabel])

                    mappeddata_u_freq[currNode] = array
                    all_nodes[currNode] = 'U'
                
                data_u_freq.append(mappeddata_u_freq)
        
        ##### POR DATA 
        data_por_freq = []
        if BOOL_POR_RESULTS:
            os.chdir(self.modelPath + config.pathSeparator + 'Benchmarked')
            freqFilesTemp = glob.glob('POR_*.csv') 
            os.chdir(config.baseDir)
            freqFilesTemp = map(lambda each: each.strip(".csv"), freqFilesTemp)
            freqFilesTemp = map(lambda each: each.strip("POR_"), freqFilesTemp)
            freqSteps = list(map(float, freqFilesTemp))
            freqSteps.sort()
            freqSteps.pop(0)  
            print('> Reading POR dofs...')
            self.FeDataStructure.freqSteps = freqSteps
            numStructNodes = len(all_nodes)
            for iStep in range(0,len(freqSteps)):
                targetData = pd.read_csv(self.modelPath + config.pathSeparator + 'Benchmarked/POR_'+ str(freqSteps[iStep])+ '.csv')
                mappeddata_por_freq = {}
                for iLabel in range(targetData.shape[0]):
                    array = []
                    currNode = int(targetData['label'][iLabel])+numStructNodes
                    for col in targetData.columns[1:]:
                        array.append(targetData[col][iLabel])
                    mappeddata_por_freq[currNode] = array
                    all_nodes[currNode] = 'POR'

                data_por_freq.append(mappeddata_por_freq)
                
        # put the different dofs together
        numDofs = dofmap.shape[0]
        self.FeDataStructure.solutionReal = np.zeros((len(freqSteps), numDofs))
        self.FeDataStructure.solutionImag = np.zeros((len(freqSteps), numDofs))
        self.FeDataStructure.nodes = np.zeros((len(all_nodes), 3))

        ## get all nodes
        #print('> Parsing nodal coords...')
        for iNode in all_nodes:
            found = False
            try:
                nodeinfo = data_u_freq[0][iNode]
                found = True
            except:
                nodeinfo = data_por_freq[0][iNode]
                found = True

            if found:
                self.FeDataStructure.nodes[iNode-1,0] = nodeinfo[0]
                self.FeDataStructure.nodes[iNode-1,1] = nodeinfo[1]
                self.FeDataStructure.nodes[iNode-1,2] = nodeinfo[2]
            else:
                print('Node reading issue')
                sys.exit(-1)

        # get all solution
        #print('> Parsing nodal solutions...')        
        for iStep in range(0,len(freqSteps)):
            solReal = []
            solImag = []
            for iNode in all_nodes:
                if all_nodes[iNode] == 'U':
                    nodal_sol = data_u_freq[iStep][iNode]
                    solReal.extend(nodal_sol[3::2])
                    solImag.extend(nodal_sol[4::2])
                elif all_nodes[iNode] == 'POR':
                    nodal_sol = data_por_freq[iStep][iNode]
                    solReal.append(nodal_sol[3])
                    solImag.append(nodal_sol[4])
            
            if len(solReal) != dofmap.shape[0] or len(solImag) != dofmap.shape[0]:
                print('Dof sizes do not match')
                sys.exit(-1)

            self.FeDataStructure.solutionReal[iStep,:] = solReal
            self.FeDataStructure.solutionImag[iStep,:] = solImag
        
        print('Analyzing abaqus generated files from dof maps... Finished.')

    # Imports the FE results of the current system into the datastructure using dofmaps
    # Author: Harikrishnan Sreekumar
    # Date: 14.10.2020
    def importFeResults(self, mode):
        if mode == 'manualdof':
            print('Deprecated...')
            self.importFeResultsDeprecated(6)
        elif mode == 'dofmap':
            self.importFeResultsUsingDofMaps()
        else:
            print('Unknown reading mode for abaqus')
            sys.exit()
            
    # Return the dof indices for a abaqus node
    # Author: Harikrishnan Sreekumar
    # Date: 14.10.2020
    def getDofIndexListForNode(self, node):
        dofmap = np.loadtxt(self.modelPath + config.pathSeparator + 'Benchmarked'  + config.pathSeparator + 'abaqus_dofmap.dat', delimiter=',')
        
        indexDict = {}
        for iNode in range(dofmap.shape[0]):
            nodeId = dofmap[iNode][0]
            if nodeId in indexDict:
                arr = indexDict[nodeId] 
                arr.append(iNode)
            else:
                arr = [iNode]
            indexDict[nodeId] = arr            

        return indexDict[node]

    # Import performance test results for system target    
    # Author: Harikrishnan Sreekumar
    # Date: 22.12.2020
    def importPerformanceResults(self, import_type, reference_system):
        pass
        
    # Delete temporary files generated by the system
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def deleteTemporaryFiles(self):
        pass

    # Reads the system's test log
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def readTestLog(self):
        print('Error: Abaqus cannot be the system under test')
        sys.exit(2)
    
    # Reads the system's target log
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def readBenchmarkLog(self):
        logfile= self.modelPath + config.pathSeparator + 'Benchmarked' + config.pathSeparator + self.modelName + '.msg'
        self.binaryInfo = self.readAbaqusDetails(logfile)
        
    # Reads the system's details
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def readAbaqusDetails(self, logfile):
        TargetInfo =[]
        with open(logfile) as file:
            lines = file.readlines()
            TargetInfo = [" ".join(lines[1].split()), " ".join(lines[2].split()), " ".join( lines[124].split()),  " ".join(lines[125].split()), " ".join(lines[126].split())," ".join(lines[127].split())," ".join(lines[128].split()) ]
            #print(TargetInfo)
        file.close()
        return TargetInfo
