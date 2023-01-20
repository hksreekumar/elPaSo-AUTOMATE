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
import os
import subprocess
import configparser
import re
import glob
import numpy as np
import h5py

# Project import
from automate import config
from automate.system.cSystemInterface import *
from automate.datastructure.cFeDataStructure import *
from automate.mod_hdf5.cElpasoFileRomHdf5 import cElpasoFileRomHdf5

# System class for elPaSo functionalities
# Author: Harikrishnan Sreekumar
# Date: 09.10.2020
class cSystemElpaso(cSystemInterface):   
    # Parse the configuration applicable for the system
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020 
    def parseConfiguration(self):
        configpath = self.modelPath + config.pathSeparator + 'configuration' + config.pathSeparator
        myConfig = configparser.ConfigParser()
        myConfig.read(configpath + config.pathSeparator + 'config.ini')

        self.systemConfig = {}
        self.systemConfig["input_type"] = myConfig.get('SystemUnderTest', 'input_type')
        self.systemConfig["output_type"] = myConfig.get('SystemUnderTest', 'output_type')
        self.systemConfig["analysis"] = myConfig.get('SystemUnderTest', 'analysis')
        self.systemConfig["start_freq"] = myConfig.get('SystemUnderTest', 'start_freq')
        self.systemConfig["stop_freq"] = myConfig.get('SystemUnderTest', 'stop_freq')
        self.systemConfig["increment"] = myConfig.get('SystemUnderTest', 'increment')

        if self.boolSUT:
            self.systemConfig["flag"] = myConfig.get('SystemUnderTest', 'system_flags')
            self.systemConfig["start_freq"] = myConfig.get('SystemUnderTest', 'start_freq')
            self.systemConfig["stop_freq"] = myConfig.get('SystemUnderTest', 'stop_freq')
            self.systemConfig["increment"] = myConfig.get('SystemUnderTest', 'increment')
            self.systemConfig["dependency-ldd"] = myConfig.get('SystemUnderTest', 'dependency-ldd').split(',')
    
        self.systemConfig["class"] = 'deprecated and will be removed in future' # myConfig.get('SystemUnderTest', 'class')
        self.systemConfig["stp_line"] = 'deprecated and will be removed in future' # int(myConfig.get('calculation', 'stp_line'))

    # Perform pre-checks to check for needed dependencies
    # Author: Harikrishnan Sreekumar
    # Data: 21.12.2020
    def performPreChecks(self):
        print('Conducting prechecks...')
        checksPassed = True
        # Generate ldd and spot if intel
        for iDependency in self.systemConfig["dependency-ldd"]:
            if(iDependency != ''):
                os.system('rm env.txt')
                os.system('ldd ' + self.binaryPath + self.binary  + ' | grep ' + iDependency + ' >> env.txt')
                with open("env.txt", "r") as envread:
                    if len(str(envread.read())) == 0:
                        checksPassed = False

        if checksPassed:
            print('Conducting prechecks... checks passed')
        else:
            print('Conducting prechecks... checks failed')
        return checksPassed
            
    # Call the system binary for computation
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def computeResults(self, computepath, execprestatement, execflags, environment):        
        print('Computing...')
        os.system('cp -r ' + self.modelPath + config.pathSeparator + 'model ' + computepath)
        os.chdir(computepath)
        self.systemCommand = environment + execprestatement + self.binaryPath + self.binary + ' -c -inp ' + self.modelName + '.' + self.systemConfig["input_type"] + ' ' + execflags;
        print('CMD: ',self.systemCommand)
        os.system(self.systemCommand)
        os.chdir(config.baseDir)
        print('Computing... Finished')
    
    # Perform correctness test on system under test
    # Author: Harikrishnan Sreekumar
    # Date: 22.12.2020
    def performCorrectnessTest(self):
        self.computeResults(self.modelPath + config.pathSeparator + 'calculation', '', self.systemConfig["flag"], '')
        self.importFeResults()
        self.readTestLog(self.modelPath + config.pathSeparator + 'calculation')
    
    # Perform performance test on system under test
    # Author: Harikrishnan Sreekumar
    # Date: 22.12.2020
    def performPerformanceTest(self, parallel_type, solver_tag, harnessconfig):
        mpirunexec = 'mpirun'
        environment = ''
        if harnessconfig.CIEnvironment != None:
            mpirunexec= harnessconfig.mpiPath
            if harnessconfig.CIEnvironment in 'gnu':
                mpirunexec = mpirunexec + ' --allow-run-as-root '
            #environment = 'export OMPI_ALLOW_RUN_AS_ROOT=1 && export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 && '
        
        self.mpi_processes = []
        self.omp_processes = []
        
        self.solvertime = []
        
        if parallel_type in 'mpi': # conduct mpi parallelization
            max_threads = os.cpu_count()/2
            iThread = 1
            while iThread <= max_threads:
                self.mpi_processes.append(iThread)
                self.omp_processes.append(1)
                iThread = iThread*2
            #if self.mpi_processes[-1] < max_threads:
            #    self.mpi_processes.append(int(max_threads))
            #    self.omp_processes.append(1)
            self.thread_vector =   self.mpi_processes       
        elif parallel_type in 'omp': # conduct omp parallelization
            max_threads = os.cpu_count()/2
            iThread = 1
            while iThread <= max_threads:
                self.mpi_processes.append(0)
                self.omp_processes.append(iThread)
                iThread = iThread*2
            #if self.omp_processes[-1] < max_threads:
            #    self.mpi_processes.append(0)
            #    self.omp_processes.append(int(max_threads))   
            self.thread_vector =   self.omp_processes       
        
        solverFlags = self.getSolverFlags(solver_tag)    
        os.mkdir(self.modelPath + config.pathSeparator + 'calculation')
        for (iMPI, iOMP) in zip(self.mpi_processes,self.omp_processes):
            case_path = self.modelPath + config.pathSeparator + 'calculation' + config.pathSeparator + 'm' + str(iMPI) + '_o' + str(iOMP)
            environment = environment + 'export OMP_NUM_THREADS='+str(iOMP)+' && '
            if parallel_type in 'omp':
                case_execprestatement = ''
                case_execflag = self.systemConfig["flag"] + ' ' + solverFlags["solverMsgLvl"] + ' ' + solverFlags["solverOmpThreads"] + ' ' + str(iOMP)
            else:
                case_execprestatement = mpirunexec + ' -np ' + str(iMPI)+' '
                case_execflag = self.systemConfig["flag"] + ' ' + solverFlags["solverMsgLvl"]
            self.computeResults(case_path, case_execprestatement, case_execflag, environment)
            self.readTestLog(case_path)
            self.solvertime.append(self.parseSolverTimeFromBinaryInfo()) 
    
    # Import performance test results for system target    
    # Author: Harikrishnan Sreekumar
    # Date: 22.12.2020
    def importPerformanceResults(self,import_type, reference_system):
        self.solvertime = []
        if import_type in 'log':
            for (iMPI, iOMP) in zip(reference_system.mpi_processes,reference_system.omp_processes):
                case_path = self.modelPath + config.pathSeparator + 'Benchmarked' + config.pathSeparator + 'm' + str(iMPI) + '_o' + str(iOMP)
                self.readTestLog(case_path)
                self.solvertime.append(self.parseSolverTimeFromBinaryInfo())
        elif import_type in 'list':
            # not implemented
            raise            
    
    # Return the solver flags
    # Author: Harikrishnan Sreekumar
    # Date: 22.12.2020
    def getSolverFlags(self, solver_tag):
        if solver_tag == 'mumps':
            solverFlag = {
                "solvertype": "-solver",
                "solverMsgLvl": "-mat_mumps_icntl_4 2",
                "solverOmpThreads": ""
            }
        elif solver_tag == 'cpardiso':
            solverFlag = {
                "solvertype": "-solver",
                "solverMsgLvl": "-mat_mkl_cpardiso68 1",
                "solverOmpThreads": ""
            }
        elif solver_tag == 'pardiso':
            solverFlag = {
                "solvertype": "-solver",
                "solverMsgLvl": "-mat_mkl_pardiso68 1",
                "solverOmpThreads": "-mat_mkl_pardiso65"
            }
        else:
            raise
        return solverFlag
    
    # Parse Solver Time Representation in Binary Info and return time in seconds
    # Author: Harikrishnan Sreekumar
    # Date: 22.12.2020
    def parseSolverTimeFromBinaryInfo(self):
        for entry in self.binaryInfo:
            if entry.find("solve system") != -1:
                time=entry.split()[3].split(':')
                return float(time[0])*86400 + float(time[1])*3600 + float(time[2])*60 + float(time[3])
                   
        raise    
        
    # Delete temporary files generated by the system
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def deleteTemporaryFiles(self):
        pass
    
    # Imports the FE results of the current system into the datastructure from HDF5 file formats
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def importFeResults(self, dummy=0):
        print('Analyzing elPaSo generated files...')

        self.FeDataStructure = cFeDataStructure()

        if self.systemConfig["analysis"] == 'frequency':
            freqSteps = self.readFrequencyFromAK3(self.modelPath + config.pathSeparator + 'calculation' + config.pathSeparator + self.modelName + '.' + self.systemConfig["input_type"])
            self.freqSteps = freqSteps
            self.FeDataStructure.freqSteps = freqSteps
        
            filename_hdf5 = self.modelPath + config.pathSeparator + 'calculation' + config.pathSeparator + self.modelName + '.' + self.systemConfig["input_type"]
            resultFilename_hdf5 = self.modelPath + config.pathSeparator + 'calculation' + config.pathSeparator + 'eGenOutput_' + self.modelName + '.' + self.systemConfig["input_type"]
            self.FeDataStructure.nodes = self.readNodesFromHdf5(filename_hdf5)            # Getting Nodal data from Source (eLPaSo)
        
            filehdf5 = h5py.File(resultFilename_hdf5, 'r') # read mode
            dset = filehdf5['/Solution/Maps/mtxDofMap']
            self.FeDataStructure.solutionReal = np.zeros((len(freqSteps), dset.shape[0]))
            self.FeDataStructure.solutionImag = np.zeros((len(freqSteps), dset.shape[0]))
        
            for iStep in range(0,len(freqSteps)):
                [solutionReal, solutionImag] = self.readResultsFromHdf5(resultFilename_hdf5, iStep+1) 
                self.FeDataStructure.solutionReal[iStep,:] = solutionReal
                self.FeDataStructure.solutionImag[iStep,:] = solutionImag
        elif self.systemConfig["analysis"] == 'eigen':
            resultFilename_hdf5 = self.modelPath + config.pathSeparator + 'calculation' + config.pathSeparator + 'eGenOutput_' + self.modelName + '.' + self.systemConfig["input_type"]
            filename_hdf5 = self.modelPath + config.pathSeparator + 'calculation' + config.pathSeparator + self.modelName + '.' + self.systemConfig["input_type"]

            eigvalues = self.readEigenValueInfoFromHdf5(resultFilename_hdf5)
            self.freqSteps = eigvalues
            self.FeDataStructure.freqSteps = eigvalues
            self.FeDataStructure.nodes = self.readNodesFromHdf5(filename_hdf5)            # Getting Nodal data from Source (eLPaSo)
        
            filehdf5 = h5py.File(resultFilename_hdf5, 'r') # read mode
            dset = filehdf5['/Solution/Maps/mtxDofMap']
            self.FeDataStructure.solutionReal = np.zeros((len(eigvalues), dset.shape[0]))
            self.FeDataStructure.solutionImag = np.zeros((len(eigvalues), dset.shape[0]))

            for iStep in range(0,len(eigvalues)):
                [solutionReal, solutionImag] = self.readResultsFromHdf5(resultFilename_hdf5, iStep+1) 
                self.FeDataStructure.solutionReal[iStep,:] = solutionReal
                self.FeDataStructure.solutionImag[iStep,:] = solutionImag
        elif self.systemConfig["analysis"] == 'static':
            resultFilename_hdf5 = self.modelPath + config.pathSeparator + 'calculation' + config.pathSeparator + 'eGenOutput_' + self.modelName + '.' + self.systemConfig["input_type"]
            filename_hdf5 = self.modelPath + config.pathSeparator + 'calculation' + config.pathSeparator + self.modelName + '.' + self.systemConfig["input_type"]

            staticStepValues = self.readStaticStepInfoFromHdf5(resultFilename_hdf5)
            self.freqSteps = staticStepValues
            self.FeDataStructure.freqSteps = staticStepValues
            self.FeDataStructure.nodes = self.readNodesFromHdf5(filename_hdf5)            # Getting Nodal data from Source (eLPaSo)
        
            filehdf5 = h5py.File(resultFilename_hdf5, 'r') # read mode
            dset = filehdf5['/Solution/Maps/mtxDofMap']
            self.FeDataStructure.solutionReal = np.zeros((len(staticStepValues), dset.shape[0]))
            self.FeDataStructure.solutionImag = np.zeros((len(staticStepValues), dset.shape[0]))

            for iStep in range(0,len(staticStepValues)):
                [solutionReal, solutionImag] = self.readResultsFromHdf5(resultFilename_hdf5, iStep+1) 
                self.FeDataStructure.solutionReal[iStep,:] = solutionReal
                self.FeDataStructure.solutionImag[iStep,:] = solutionImag
        elif self.systemConfig["analysis"] == 'mor-offline':
            # check if the ROM results matched with ROM results?
            resultFilename_hdf5 = self.modelPath + config.pathSeparator + 'calculation' + config.pathSeparator + 'eGenModRed_ROM.hdf5'
            filename_hdf5 = self.modelPath + config.pathSeparator + 'calculation' + config.pathSeparator + self.modelName + '.' + self.systemConfig["input_type"]
            
            rom_reader = cElpasoFileRomHdf5(resultFilename_hdf5)
            all_H, freqSteps = rom_reader.getAllTransferFunctions()
            self.freqSteps = freqSteps
            self.FeDataStructure.freqSteps = freqSteps
            self.FeDataStructure.nodes = self.readNodesFromHdf5(filename_hdf5)            # Getting Nodal data from Source (eLPaSo)
        
            nshape = all_H.shape[0]*all_H.shape[1]
            self.FeDataStructure.solutionReal = np.zeros((len(freqSteps), nshape))
            self.FeDataStructure.solutionImag = np.zeros((len(freqSteps), nshape))
                        
            for iStep in range(len(freqSteps)):
                self.FeDataStructure.solutionReal[iStep,:] = np.real(all_H[:,:,iStep].flatten())
                self.FeDataStructure.solutionImag[iStep,:] = np.imag(all_H[:,:,iStep].flatten())
            # check if VMAT size is the same?
        else:
            print('Unknown analysis. Exiting...')
            exit(-1)

        print('Analyzing elPaSo generated files... Finished')
        
    # Return the dof indices for an elpaso node
    # Author: Harikrishnan Sreekumar
    # Date: 14.12.2021
    def getDofIndexListForNode(self, node):
        if self.systemConfig["analysis"] == 'mor-offline':
            # in this case we expect the dof id in one-indexed to be inputed as node
            return np.array([node-1]) # to zero indexed
        else:
            resultFilename_hdf5 = self.modelPath + config.pathSeparator + 'calculation' + config.pathSeparator + 'eGenOutput_' + self.modelName + '.' + self.systemConfig["input_type"]

            filehdf5 = h5py.File(resultFilename_hdf5, 'r') # read mode
            dofmap = filehdf5['/Solution/Maps/mtxDofMap']        
        
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

    # Imports the FE results of the current system into the datastructure from HDF5 file formats
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def importFeResultsFromHDF5(self):
        pass
    
    # Imports the FE results of the current system into the datastructure from STP file formats
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def importFeResultsFromSTP(self):
        pass
   
    # Reads the system's test log
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    def readTestLog(self, path):
        logFile = path + config.pathSeparator + self.modelName + '.log.0'
        self.binaryInfo = self.readElpasoDetails(logFile)

    # Reads the system's target log
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020    
    def readBenchmarkLog(self):
        logFile = self.modelPath + config.pathSeparator + 'Benchmarked' + config.pathSeparator + self.modelName + '.log.0'
        self.binaryInfo = self.readElpasoDetails(logFile)

    # Reads the system's details
    # Author: Saurabh Rathore
    # Date: 09.10.2020
    def readElpasoDetails(self, logFile):
        SourceInfo = []
        with open(logFile) as file:
            lines = file.readlines()
            # freq
            SourceInfo = [" ".join(lines[1].split()), " ".join(lines[3].split()), " ".join(lines[4].split()), " ".join(lines[5].split()), " ".join(lines[6].split()), " ".join(lines[8].split()),
            " ".join(lines[9].split()), " ".join(lines[10].split()), " ".join(lines[11].split()), " ".join(lines[12].split()), " ".join(lines[13].split())]
            for l in range (0,20):
                SourceInfo.append(" ".join(lines[int(len(lines))-21+l].split()))
        file.close()
        return SourceInfo

    # need to change
    def readFrequencyFromAK3(self, pathAK3):
        startFreq=int(self.systemConfig["start_freq"])
       
        deltaFreq=int(self.systemConfig["increment"])
        stepsFreq=int((int(self.systemConfig["stop_freq"])-int(self.systemConfig["start_freq"]))/deltaFreq)+1
        #startFreq=100
        #stepsFreq=2
        #deltaFreq=500
        freq = []            
        freq.append(startFreq)
        for iStep in range(1, stepsFreq):
            freq.append(freq[iStep - 1] + deltaFreq)

        return freq

    # need to change
    def readDataFromVTK(self, pathVTK, pointer):
        count = 0
        with open(pathVTK, 'r') as f:
            for line in f:
                if pointer in line:
                    count = count + 1
        f.close()
        List = [''] * count
        count = 0
        with open(pathVTK, 'r') as f:
            for line in f:
                if pointer in line:
                    key_val = re.split(' ', line)
                    List[count] = key_val[1]
                    count = count + 1
        f.close()
        return (List)
    
    # Reads node information from model hdf5
    # Author: Harikrishnan Sreekumar
    # Date: 13.12.2021
    def readNodesFromHdf5(self, modelhdf5):
        filehdf5 = h5py.File(modelhdf5, 'r') # read mode
        dset = filehdf5['/Nodes/mtxFemNodes']
        xCoords = np.array(dset.fields("xCoords")[:])
        yCoords = np.array(dset.fields("yCoords")[:])
        zCoords = np.array(dset.fields("zCoords")[:])
        ids = np.array(dset.fields("Ids")[:])

        ids_indx_sorted = np.argsort(ids)

        Nds = len(ids) # get number of nodes
        nodeInfo = np.zeros((Nds, 3))
        nodeInfo[:,0] = xCoords[ids_indx_sorted]
        nodeInfo[:,1] = yCoords[ids_indx_sorted]
        nodeInfo[:,2] = zCoords[ids_indx_sorted]

        return nodeInfo

    # deprecated. replaced with hdf5
    #def readNodesFromVTK(self, pathVTK, pointer):
    #    Nds = self.readDataFromVTK(pathVTK, 'POINTS')
    #    Nds = int(float(Nds[0]))
    #    arg1 = np.zeros((Nds, 3))
    #    with open(pathVTK, 'r') as f:
    #        for line in f:
    #            line = line.strip()
    #            if line.startswith(pointer):
    #                line = next(f)
    #                for x in range(0, Nds):
    #                    keyVal = re.split(' ', line)
    #                    arg1[x][0] = float(keyVal[0])
    #                    arg1[x][1] = float(keyVal[1])
    #                    arg1[x][2] = float(keyVal[2])
    #                    line = next(f)
    #                break
    #    return (arg1)
    
    # Reads results from hdf5
    # Author: Harikrishnan Sreekumar
    # Date: 13.12.2021
    def readResultsFromHdf5(self, resultshdf5, step):
        filehdf5 = h5py.File(resultshdf5, 'r') # read mode
        dset = filehdf5['/Solution/State/vecFemStep' + str(step)]
        realdata = np.array(dset.fields("real")[:])
        imagdata = np.array(dset.fields("imag")[:])
        return [realdata, imagdata]

    # Reads eigenvalues from hdf5
    # Author: Harikrishnan Sreekumar
    # Date: 04.05.2022
    def readEigenValueInfoFromHdf5(self, resultshdf5):
        filehdf5 = h5py.File(resultshdf5, 'r') # read mode
        att_list = filehdf5['/Solution/State']

        eigvals = []
        for att in att_list:
            if 'EigStep' in att:
                eigval = float(filehdf5['/Solution/State'].attrs[att])
                eigvals.append(eigval)

        eigvals = np.array(eigvals)
        return eigvals
    
    # Reads static steps from hdf5
    # Author: Harikrishnan Sreekumar
    # Date: 05.05.2022
    def readStaticStepInfoFromHdf5(self, resultshdf5):
        filehdf5 = h5py.File(resultshdf5, 'r') # read mode
        att_list = filehdf5['/Solution/State']

        staticvals = []
        for att in att_list:
            if 'StaticStep' in att:
                val = float(filehdf5['/Solution/State'].attrs[att])
                staticvals.append(val)

        staticvals = np.array(staticvals)
        return staticvals
    
    # deprecated. Replaced with hdf5
    #def readResultsFromSTP(self, pathSTP):
    #    realvector = []
    #    imgvector = []
    #    with open(pathSTP) as f:
    #        lines = f.readlines()
    #        freq = float(lines[0])
    #        for i in range(1, self.systemConfig["stp_line"]):
    #            realvector.append(float(lines[i].split('  ')[1]))
    #            imgvector.append(float(lines[i].split('  ')[2]))
    #    return [realvector, imgvector]
