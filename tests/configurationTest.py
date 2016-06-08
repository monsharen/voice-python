#!/usr/bin/python

import unittest

from configuration import *


class ConfigurationTest(unittest.TestCase):

    def test_should_return_data_set_object(self):
        _dataSetName = "dataSetName"
        _dataSet = get_data_set(_dataSetName)

        self.assertEquals(_dataSet.name, _dataSetName)
        self.assertEquals(_dataSet.metaData.folder, root + "\\Datasets\\" + _dataSetName + "\\MetaData\\")
        self.assertEquals(_dataSet.testSet.folder, root + "\\Datasets\\" + _dataSetName + "\\TestSet\\")
        self.assertEquals(_dataSet.testSet.transcriptionInputFile, root + "\\Datasets\\" + _dataSetName + "\\TestSet\\transcription.txt")
