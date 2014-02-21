__author__ = 'JuhoAutio'

import unittest
import logging
from updater import Updater

class UpdaterTestCase(unittest.TestCase):

    # asserts that the return message from Updater is correct
    # TODO this doesn't really test the actual output / modifications, but that should definitely be done
    def assertUpdate(self, file, result):
        # initialize debug level logging to console
        logging.basicConfig(level=logging.DEBUG)
        self.assertEqual(result, Updater.updateFile(Updater(), file, False))

    def test_download_import_automatically(self):
        self.assertUpdate('resources/download_import_automatically/.idea/workspace.xml', 'All options already in place: \n\
<MavenImportingSettings>\n\
        <option name="downloadDocsAutomatically" value="true" />\n\
        <option name="downloadSourcesAutomatically" value="true" />\n\
        <option name="importAutomatically" value="true" />\n\
      </MavenImportingSettings>\n\
    ')

    def test_import_automatically(self):
        self.assertUpdate('resources/importAutomatically/.idea/workspace.xml', 'added docs and sources')

    def test_unknown_options(self):
        self.assertUpdate('resources/unknownOptions/.idea/workspace.xml',
                          'Skipping file \'resources/unknownOptions/.idea/workspace.xml\' because it already contains: \n\
<MavenImportingSettings>\n\
        <option name="importAutomatically" value="true" />\n\
        <option name="unknownOption" value="true" />\n\
      </MavenImportingSettings>\n\
    ')

    def test_no_maven_settings(self):
        self.assertUpdate('resources/no_maven_settings/.idea/workspace.xml', 'Update succeeded')

if __name__ == '__main__':

    # run tests
    unittest.main()
