"""DrugnameAssembler Class

This module is an implementation of the Assembler class described in the architecture. It handles the creation and execution of all the extractors as specified by the config file from ProjectAERIS. When Assemblers are created for other DataElements, simply copy this class, but remember to change the __init__ function and runExtractors() functions, as per the wiki.

Todo:
    * Go through this class and use the @property decorator and create getter/setter methods that way. 
"""

# from Extractors.Drugname.DrugnameMetamapExtractor import DrugnameMetamapExtractor
from Extractors.Drugname.DrugnameRegExtractor import DrugnameRegExtractor
from Extractors.Drugname.SVMv1DrugNameExtractor import SVMv1DrugNameExtractor
from Assemblers.EntityAssembler import EntityAssembler
import xml.etree.ElementTree as ET


# from test import Compare


class DrugnameAssembler(EntityAssembler):
    def __init__(self, rawTextFileName, intermediateXMLFileName, anExtractorList=[]):
        """
        Initializes the EventDateAssembler and returns it. All Extractors for the Event Date DataElement must be specified in the list below. 

        Args:
            anExtractorList (list): the list passed from the config file for EventDate
        
        Returns:

            EventDateAssembler Object

        """
        super(DrugnameAssembler, self).__init__(rawTextFileName, intermediateXMLFileName, anExtractorList=[])

        self.AllPossibleExtractorList = {
            # "DrugnameMetamapExtractor": DrugnameMetamapExtractor(rawTextFileName, intermediateXMLFileName),
            "DrugnameRegExtractor": DrugnameRegExtractor(rawTextFileName, intermediateXMLFileName),
            "SVMv1DrugNameExtractor": SVMv1DrugNameExtractor(rawTextFileName, intermediateXMLFileName)}
        self.entityName = 'DRUGNAME'
        self.filename = rawTextFileName
        self.testCaseName = self.filename[self.filename.rfind(r'/') + 1:self.filename.rfind(r'.txt')]


    def launchTestSuite(self):
        self.filename
        # # we need the annotation file and the program output file: Test_Suite/Eval_Env/xml/fda001.xml
        # # and Test_Suite/Eval_Env/semifinal/fda001_EVENT_DT_Semifinal.xml
        # comp = Compare('Test_Suite/Eval_Env/xml/'+self.testCaseName+r'.xml', 'Test_Suite/Eval_Env/semifinal/'+self.testCaseName+'_'+self.entityName+'_'+r'Semifinal.xml')
        # #comp = Compare('../Test_Suite/Eval_Env/xml/'+self.testCaseName+r'.xml', '../Test_Suite/Eval_Env/semifinal/'+self.testCaseName+'_'+self.entityName+'_'+r'Semifinal.xml')
        # for elements in self.dataElementList:
        #    # print elements[0].extractedField, elements[0].extractorName, elements[0].entityName
        #     ## if elements is null then might get error
        #     comp.multi_compare(elements[0].entityName, elements[0].extractorName)
        #
