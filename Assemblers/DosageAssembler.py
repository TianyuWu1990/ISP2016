"""DosageAssembler Class

This module is an implementation of the Assembler class described in the architecture. It handles the creation and execution of all the extractors as specified by the config file from ProjectAERIS. When Assemblers are created for other DataElements, simply copy this class, but remember to change the __init__ function and runExtractors() functions, as per the wiki.

Todo:
    * Go through this class and use the @property decorator and create getter/setter methods that way. 
"""

from Extractors.Dosage.DosageRegExtractor import DosageRegExtractor
from Preprocessing.Preprocessor import Preprocessor
from Assemblers.EntityAssembler import EntityAssembler
import xml.etree.ElementTree as ET
import xml.etree.ElementTree as ET
# from test import Compare
from pprint import pprint


class DosageAssembler(EntityAssembler):
    def __init__(self, rawTextFileName, intermediateXMLFileName, anExtractorList=[]):
        """
        Initializes the EventDateAssembler and returns it. All Extractors for the Event Date DataElement must be specified in the list below. 

        Args:
            anExtractorList (list): the list passed from the config file for EventDate
        
        Returns:
            EventDateAssembler Object
        """
        super(DosageAssembler, self).__init__(rawTextFileName, intermediateXMLFileName, anExtractorList=[])

        self.AllPossibleExtractorList = {
            "DosageRegExtractor": DosageRegExtractor(rawTextFileName, intermediateXMLFileName)}
        # TODO: We need to figure out the best way to get this to work.
        self.entityName = 'DOSAGE'
        self.filename = rawTextFileName
        self.testCaseName = self.filename[self.filename.rfind(r'/') + 1:self.filename.rfind(r'.txt')]


    def launchTestSuite(self):
        self.filename
        # # we need the annotation file and the program output file: Test_Suite/Eval_Env/xml/fda001.xml
        # # and Test_Suite/Eval_Env/semifinal/fda001_EVENT_DT_Semifinal.xml
        # comp = Compare('Test_Suite/Eval_Env/xml/'+self.testCaseName+r'.xml', 'Test_Suite/Eval_Env/semifinal/'+self.testCaseName+'_'+self.entityName+'_'+r'Semifinal.xml')
        # #comp = Compare('../Test_Suite/Eval_Env/xml/'+self.testCaseName+r'.xml', '../Test_Suite/Eval_Env/semifinal/'+self.testCaseName+'_'+self.entityName+'_'+r'Semifinal.xml')
        #
        #
        # # for de in self.dataElementList[0][0]:
        # #    # print de.entityName ,  de.extractorName, de.extractedField
        # #     comp.multi_compare(de.entityName, de.extractorName)
