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

### Details: cElpasoFileRomHdf5
### Date: 15.11.2021
### Author: Harikrishnan Sreekumar

# python imports
import numpy as np

# project modules
from automate.mod_hdf5 import cFileHdf5

class cElpasoFileRomHdf5:
    # @brief initialization method
    # @note unit-tested
    def __init__(self, filename):
        self.filename = filename
        # cGeneralLogging.addStatementToLog('>> elPaSo rom file initialized | file: ' + self.filename)

    # @brief function to get the latest error data
    # @note unit-tested
    def getLatestErrorData(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        dslist = myfile.getDataSetList('/SystemModRed/Error')
        ydata = myfile.readdataset_complexcompound('/SystemModRed/Error', dslist[len(dslist)-1])
        return ydata

    # @brief function to get the history expansion points
    def getExpansionPointsHistory(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        id = self.getAttribute('/SystemModRed/Training','training_id')
        listofEP = myfile.getDataSetList('/SystemModRed/Training')
        id_array = []
        ep_array = []
        for every_ds in listofEP:
            if 'vecCurrentEPs_' in every_ds:
                curr_id = int(every_ds.split('vecCurrentEPs_')[1])
                xdata = myfile.readdataset_complexcompound('/SystemModRed/Training', 'vecCurrentEPs_'+str(curr_id))
                add_ids = curr_id*np.ones(len(xdata))
                id_array.append(add_ids)
                ep_array.append(xdata)
        id_array = np.concatenate(id_array)
        ep_array = np.concatenate(ep_array)
        return ep_array, id_array

    # @brief function to get the expansion points
    # @note unit-tested
    def getExpansionPoints(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        id = self.getAttribute('/SystemModRed/Training','training_id')
        xdata = myfile.readdataset_complexcompound('/SystemModRed/Training', 'vecCurrentEPs_'+id)
        return xdata

    # @brief function to get the training point data
    # @note unit-tested
    def getTrainingPoints(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        id = self.getAttribute('/SystemModRed/Training','training_id')
        xdata = myfile.readdataset_complexcompound('/SystemModRed/Training', 'vecTrainingPoints_I'+id)
        return xdata

    # @brief function to get the history training points
    def getTrainingPointsHistory(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        id = self.getAttribute('/SystemModRed/Training','training_id')
        listofEP = myfile.getDataSetList('/SystemModRed/Training')
        id_array = []
        ep_array = []
        for every_ds in listofEP:
            if 'vecCurrentEPs_' in every_ds:
                curr_id = int(every_ds.split('vecCurrentEPs_')[1])
                xdata = myfile.readdataset_complexcompound('/SystemModRed/Training', 'vecTrainingPoints_I'+str(curr_id))
                add_ids = curr_id*np.ones(len(xdata))
                id_array.append(add_ids)
                ep_array.append(xdata)
        id_array = np.concatenate(id_array)
        ep_array = np.concatenate(ep_array)
        return ep_array, id_array

    # @brief function to read the frequency interval
    def getDefinedFrequencyInterval(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        start = myfile.readAttribute('/SystemModRed','freq_min')
        end = myfile.readAttribute('/SystemModRed','freq_max')
        return float(start), float(end)

    # @brief function to get all transfer functions
    # @note unit-tested
    def getAllTransferFunctions(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        dslist = myfile.getDataSetList('/SystemModRed/TransferFunction')
        freq = np.zeros(len(dslist))

        testread = myfile.readdataset_complexcompound('/SystemModRed/TransferFunction', dslist[0])
        numoutput = testread.shape[0]
        numinput = testread.shape[1]

        hdata = np.zeros((numoutput, numinput, len(dslist)), dtype=complex)

        # read frequency available
        freq_data, sorting = self.getEvaluatedTransferFunctionFrequency()

        # read dataset according to sorting
        indx = 0
        for everyds in dslist:
            hdata[:,:,indx] = myfile.readdataset_complexcompound('/SystemModRed/TransferFunction', everyds)
            indx+=1
        hdata = hdata[:,:,sorting]

        return hdata, freq_data

    # @brief function to get a specific transfer function
    # @note unit-tested
    def getTransferFunctions(self, i_inp, i_out):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        dslist = myfile.getDataSetList('/SystemModRed/TransferFunction')
        hdata = np.zeros(len(dslist), dtype=complex)

        # read frequency available
        freq_data, sorting = self.getEvaluatedTransferFunctionFrequency()

        indx = 0
        for everyds in dslist:
            hdata[indx] = myfile.readdataset_complexcompound('/SystemModRed/TransferFunction', everyds)[i_out][i_inp]
            indx+=1

        hdata = hdata[sorting]

        return hdata, freq_data

    # function to get eigen value information from file
    def getEigenValueInWindow(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        return myfile.readdataset_complexcompound( '/SystemModRed/Eigen', 'vecEigValInFreqWindow')

    # @brief function to get an attribute value
    # @note unit-tested
    def getAttribute(self, path, attribute):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        return myfile.readAttribute( path, attribute)

    # @brief function to get evaluated frequency from attribute data
    # @note unit-tested
    def getEvaluatedTransferFunctionFrequency(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        listofatt = myfile.getAttributeList('/SystemModRed/TransferFunction')
        freq = np.zeros(len(listofatt))
        iIndx = 0
        for everyatt in listofatt:
            id = int(everyatt.split('FreqStep')[1])-1
            freq[iIndx] = float(myfile.readAttribute('/SystemModRed/TransferFunction', 'FreqStep' + str(id+1)))
            iIndx += 1
        id_sort = np.argsort(freq)
        freq = freq[id_sort]
        return freq, id_sort

    # @brief function to get the rom dimension
    # @note unit-tested
    def getRomDimension(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        rom_stiffness_mat = myfile.readdataset_complexcompound('/SystemModRed/Stiffness', 'mtxStiffnessRom')
        return rom_stiffness_mat.shape[0]

    # @brief function to get the projection basis V dimension
    # @note unit-tested
    def getBasisVDimension(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        basis = myfile.readdataset_complexcompound('/SystemModRed/Bases', 'mtxBasisV')
        return basis.shape

    # @brief function to get the projection basis W dimension
    # @note unit-tested
    def getBasisWDimension(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        basis = myfile.readdataset_complexcompound('/SystemModRed/Bases', 'mtxBasisW')
        return basis.shape

    # @brief function to get the number of inputs
    # @note unit-tested
    def getNumInputs(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        rom_input_mat = myfile.readdataset_complexcompound('/SystemModRed/SignalB', 'mtxBmatRom')
        return rom_input_mat.shape[1]

    # @brief function to get the number of outputs
    # @note unit-tested
    def getNumOutputs(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        rom_input_mat = myfile.readdataset_complexcompound('/SystemModRed/SignalC', 'mtxCmatRom')
        return rom_input_mat.shape[0]

    # @brief function to read a dataset
    # @note unit-tested
    def readDataSet(self, path, dsetname):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        return myfile.readdataset(path, dsetname)

    # @brief function to read ROM matrices
    # @note unit-tested
    def readRomSystemMatrices(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        system_rom = {}
        system_rom['KROM'] = myfile.readdataset_complexcompound('/SystemModRed/Stiffness','mtxStiffnessRom')
        system_rom['DROM'] = myfile.readdataset_complexcompound('/SystemModRed/Damping','mtxDampingRom')
        system_rom['MROM'] = myfile.readdataset_complexcompound('/SystemModRed/Mass','mtxMassRom')
        system_rom['VMAT'] = myfile.readdataset_complexcompound('/SystemModRed/Bases','mtxBasisV') # to be depricated
        #system_rom['WMAT'] = myfile.readdataset_complexcompound('/SystemModRed/Bases','mtxBasisW')
        return system_rom

    # @brief function to write the ROM matrices
    # @note unit-tested
    def writeRomSystemMatrices(self, KROM, DROM, MROM, BROM, CROM, VMAT, WMAT):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'a')
        myfile.writedataset_complexcompound('/SystemModRed/Stiffness','mtxStiffnessRom', KROM)
        myfile.writedataset_complexcompound('/SystemModRed/Damping','mtxDampingRom', DROM)
        myfile.writedataset_complexcompound('/SystemModRed/Mass','mtxMassRom', MROM)
        myfile.writedataset_complexcompound('/SystemModRed/SignalB','mtxBmatRom', BROM)
        myfile.writedataset_complexcompound('/SystemModRed/SignalC','mtxCmatRom', CROM)
        myfile.writedataset_complexcompound('/SystemModRed/Bases','mtxBasisV', VMAT)
        myfile.writedataset_complexcompound('/SystemModRed/Bases','mtxBasisW', WMAT)
        myfile.closeFile()

    # @brief function to read ROM signal matrices
    # @note unit-tested
    def readRomSystemSignals(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        system_rom = {}
        system_rom['BROM'] = myfile.readdataset_complexcompound('/SystemModRed/SignalB','mtxBmatRom')
        system_rom['CROM'] = myfile.readdataset_complexcompound('/SystemModRed/SignalC','mtxCmatRom')
        return system_rom

    # function to read tangent basis
    # @note unit-tested
    def readTangentBasis(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        system_rom = {}
        system_rom['TMAT'] = myfile.readdataset_complexcompound('/SystemModRed/Bases','mtxBasisT')
        return system_rom

    # function to read projection bases
    # @note unit-tested
    def readProjectionBases(self):
        myfile = cFileHdf5.cFileHdf5(self.filename, 'r')
        system_rom = {}
        system_rom['VMAT'] = myfile.readdataset_complexcompound('/SystemModRed/Bases','mtxBasisV')
        system_rom['WMAT'] = myfile.readdataset_complexcompound('/SystemModRed/Bases','mtxBasisW')
        return system_rom