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

# Visualizer interface class
# Author: Harikrishnan Sreekumar
# Date: 09.10.2020
class cVisInterface(metaclass=abc.ABCMeta):        
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'generateVisualization') and 
                callable(subclass.generateVisualization)  or 
                NotImplemented)
    
    # Abstract method: Generates visualization
    # Author: Harikrishnan Sreekumar
    # Date: 09.10.2020
    @abc.abstractmethod
    def generateVisualization(self):
        raise NotImplementedError