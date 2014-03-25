#!/usr/bin/python

"""
Small and simple example of parsing large xml files using SAX parsing in
Python.

"""

import os
import sys
import logging
import resource

from lxml import etree
from docopt import docopt
from faker import Factory

FAKE = Factory.create()
LOG = logging.getLogger(__name__)

class XMLObject(object):
    """Represent an object serialised to XML"""

    def from_xml(self, element):
        """docstring for from_xml"""
        for child in element:
            setattr(self, child.tag, child.text.decode('utf-8'))
        return self

    def to_xml(self):
        """ Returns etree element based on class dict """

        class_element = etree.Element(self.__class__.__name__)
        for key, value in self.__dict__.iteritems():
            attribute_element = etree.Element(key)
            attribute_element.text = value
            class_element.append(attribute_element)
        return class_element

    def __str__(self):
        """
        object string representation
        returns a string list of object attributes
        
        """
        return (" , ".join(["{key} = {value}".format(key=key, value=value)\
                for key, value in self.__dict__.iteritems()])).\
                replace('\n',' ')



def incremental_xml_dump(xml_filename, object_dict):
    """
    Incrementally dumps objects from object dict to XML

    Params:
        xml_filename : output XML filename
        object_dict : dictionary of parent tag and list of child objects
    """

    with etree.xmlfile(xml_filename, encoding="utf-8") as xml_fp:
        for key, values in object_dict.iteritems():
            with xml_fp.element(key):
                for value in values:
                    xml_fp.write(value.to_xml())


def sax_parse_xml_file(filename, tag):
    """
    SAX parse large xml file
    
    """

    with open(filename) as xml_fp:

        # only listen to 'end' events because in this case the entire element
        # has been read.
        LOG.debug("Parsing XML file %s looking for tag : %s" , filename, tag)
        sax_parser = etree.iterparse(xml_fp,
                                     events=('end',),
                                     tag=tag,
                                     encoding="utf-8")

        # Loop through file but only get elements of type 'tag' and action
        # 'end'
        for action, element in sax_parser:

            assert action == "end"
            assert element.tag == tag

            # get object
            klass = globals()[element.tag]
            # initate object from XML
            xml_object = klass().from_xml(element)
            LOG.info("imported %s", xml_object)

            # Memory clean up section
            # clear children elements from memory
            element.clear()
            # clear parrent reference to previous elements
            while element.getprevious() is not None:
                del element.getparent()[0]

        # clean up parser
        del sax_parser


class Person(object):
    def __init__(self, name=None, address=None, country=None):
        super(Person, self).__init__()
        self.name = name
        self.address = address
        self.country = country
        

class MyPerson(Person, XMLObject):
    """
    Simple Mixin class. Provides xmldump functionality to the Person object.

    """
    pass
        

def fake_data_generator(N=10000):
    """
    
    """
    for i in range(N):
        yield MyPerson(name=FAKE.name(), 
                       address=FAKE.address(),
                       country=FAKE.country())



if __name__ == '__main__':
    LOG = logging.getLogger('lxml-example')
    logging.basicConfig(level=logging.DEBUG)

    __doc__ = """
    File: lxml_example.py
    Usage:
        lxml_example.py dump <filename> <number>
        lxml_example.py import <filename> <tag>
        lxml_example.py (-h | --help)
        lxml_example.py --version 
    Options:
        -h --help     Show this screen.
        --version     Show version.
    """
    arguments = docopt(__doc__, version='0.1')

    rusage = resource.getrusage(resource.RUSAGE_SELF)
    LOG.debug("Start: Maximum resident mem usage %s", rusage.ru_maxrss)

    if arguments['import']:
        sax_parse_xml_file(arguments['<filename>'], tag=arguments['<tag>'])
    elif arguments['dump']:
        incremental_xml_dump(arguments['<filename>'], 
                {'persons' : fake_data_generator(N=int(arguments['<number>']))})
    else:
        # docopt takes care of the input parsing
        pass
    
    rusage = resource.getrusage(resource.RUSAGE_SELF)
    LOG.debug("End: Maximum resident mem usage %s", rusage.ru_maxrss)
    LOG.debug("User mode time %s", rusage.ru_utime)
    LOG.debug("System mode time %s", rusage.ru_stime)
    
