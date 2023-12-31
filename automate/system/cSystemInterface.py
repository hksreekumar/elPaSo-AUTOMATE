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
import abc

# System interface class
# Author: Harikrishnan Sreekumar
# Date: 09.10.2020
class cSystemInterface(metaclass=abc.ABCMeta):
    # Constructor
    # Author: Harikrishnan Sreekumar
    # Date: 06.10.2020
    def __init__(self, systemName, systemPath, modelName, modelPath, boolSUT):
        self.system = systemName            # system name
        self.binaryPath = systemPath        # system path
        self.modelName = modelName          # model name
        self.modelPath = modelPath          # model path
        self.boolSUT = boolSUT              # boolean - if System under test
        
        self.systemCommand = '' 
        
        self.binary = systemName            # same as systemtype

        self.FeDataStructure = None         # datastructure handle

        # Binary related
        self.binaryInfo = []                # binary info - includes version and performance related data
        
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'parseConfiguration') and 
                callable(subclass.parseConfiguration) and 
                hasattr(subclass, 'compute') and 
                callable(subclass.compute) and 
                hasattr(subclass, 'importFeResults') and 
                callable(subclass.importFeResults) and 
                hasattr(subclass, 'deleteTemporaryFiles') and 
                callable(subclass.deleteTemporaryFiles) and 
                hasattr(subclass, 'readTestLog') and 
                callable(subclass.readTestLog) and 
                hasattr(subclass, 'readBenchmarkLog') and 
                callable(subclass.readBenchmarkLog) and
                hasattr(subclass, 'importPerformanceResults') and 
                callable(subclass.importPerformanceResults) or 
                NotImplemented)

    # Abstract method: Parse system configuration
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    @abc.abstractmethod
    def parseConfiguration(self):
        raise NotImplementedError
    
    # Abstract method: Call the system binary for computation
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    @abc.abstractmethod
    def computeResults(self):
        raise NotImplementedError
    
    # Abstract method: Imports the FE results of the current system into the datastructure
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    @abc.abstractmethod
    def importFeResults(self):
        raise NotImplementedError
    
    # Abstract method: Delete temporary files generated by the system
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    @abc.abstractmethod
    def deleteTemporaryFiles(self):
        raise NotImplementedError
    
    # Abstract method: Reads the system's test log
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    @abc.abstractmethod
    def readTestLog(self):
        raise NotImplementedError
    
    # Abstract method: Reads the system's target log
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    @abc.abstractmethod
    def readBenchmarkLog(self):
        raise NotImplementedError
        
    # Abstract method: Import performance test results for system target    
    # Author: Harikrishnan Sreekumar
    # Date: 22.12.2020
    @abc.abstractmethod
    def importPerformanceResults(self, import_type, reference_system):
        pass
