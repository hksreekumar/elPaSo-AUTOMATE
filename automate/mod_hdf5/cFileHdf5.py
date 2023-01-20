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

### Details: cFileHdf5
### Date: 12.11.2021
### Author: Harikrishnan Sreekumar

# python imports
import h5py
import numpy as np

class cFileHdf5:
    # @note unit-tested
    # mode: 'a': append mode, 'r': read mode, 'w' create new file
    def __init__(self, filename, mode):
        self.filenamehdf5 = filename
        self.filehdf5 = h5py.File(self.filenamehdf5, mode)
        self.cmptype = np.dtype([('real','float64'), ('imag','float64')])

    # @brief Function to close the hdf5 file
    # @note unit-tested
    def closeFile(self):
        self.filehdf5.close()

    # @brief Function to delete a group
    # @note unit-tested
    def deleteGroup(self, groupname):
        del self.filehdf5[groupname]

    # @brief Function to rename a group
    # @note unit-tested
    def renameGroup(self, old_groupname, new_groupname):
        self.filehdf5[new_groupname] = self.filehdf5[old_groupname]
        self.deleteGroup(old_groupname)

    # @brief Function to clear the file
    # @note unit-tested
    def clearFile(self):
        paths = self.filehdf5['/']
        for everypath in paths:
            del self.filehdf5[everypath]

    # @brief Function to create a group
    # @note unit-tested
    def createGroup(self, groupname):
        self.filehdf5.create_group(groupname)

    # @brief Function to add an attribute
    # @note unit-tested
    def addAttribute(self, path, attributename, value):
        self.filehdf5[path].attrs[attributename] = value

    # @brief Function to read an attribute
    # @note unit-tested
    def readAttribute(self, path, attributename):
        return self.filehdf5[path].attrs[attributename]

    # @brief Function to get an attribute list
    # @note unit-tested
    def getAttributeList(self, path):
        set_list = []
        att_list = self.filehdf5[path].attrs
        for att in att_list:
            set_list.append(att)
        return set_list

    # @brief Function to get the list of datasets
    # @note unit-tested
    def getDataSetList(self, path):
        grp = self.filehdf5[path]
        set_list = []
        for dset in grp:
            set_list.append(dset)

        return set_list

    # @brief Function to add a dataset
    # @note unit-tested
    def addDataSet(self, path, datasetname, value):
        self.filehdf5.create_dataset(path + '/' + datasetname, data=value)

    # @brief Function to read a complex compound datatype
    # @note unit-tested
    def readdataset_complexcompound(self, path, dsetname):
        dset = self.filehdf5[path + '/' + dsetname]
        realdata = np.array(dset.fields("real")[:])
        imagdata = np.array(dset.fields("imag")[:])
        return realdata+imagdata*1j

    # @brief Function to write an empty complex compound datatype
    # @note unit-tested
    def writedataset_emptycomplexcompound(self, path, dsetname):
        dt_type = np.dtype([('real','float64'), ('imag','float64')])
        self.filehdf5.create_dataset(path + '/' + dsetname, (0,), dtype=dt_type)

    # @brief Function to write a complex compound datatype
    # @note unit-tested
    def writedataset_complexcompound(self, path, dsetname, value):
        if value.dtype != self.cmptype:
            value_tmp = value
            value = np.zeros(value_tmp.shape, dtype=self.cmptype)
            value['real'] = np.real(value_tmp)
            value['imag'] = np.imag(value_tmp)

        if self.datasetExists(path + '/' + dsetname):
            del self.filehdf5[path + '/' + dsetname]

        dt_type = np.dtype([('real','float64'), ('imag','float64')])
        self.filehdf5.create_dataset(path + '/' + dsetname, value.shape, dtype=dt_type, data = value)

    # @brief function to read a dataset
    # @note unit-tested
    def readdataset(self, path, dsetname):
        dset = self.filehdf5[path + '/' + dsetname]
        return dset[:]

    # @brief Checks if a group exists
    # @note unit-tested
    def groupExists(self, path):
        try:
            grp = self.filehdf5[path]
            return True
        except:
            return False

    # @brief Checks if the data set exists
    # @note unit-tested
    def datasetExists(self, path):
        try:
            dset = self.filehdf5[path]
            return True
        except:
            return False

    # @brief Returns a list of group names in path
    # @note unit-tested
    def getGroupList(self, path):
        grp = self.filehdf5[path]
        set_list = []
        for gset in grp:
            set_list.append(gset)

        return set_list
