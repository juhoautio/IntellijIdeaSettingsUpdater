#!/usr/bin/python
"""
This script modifies IntelliJ IDEA's workspace.xml so that it has the following Maven Import preferences:

  <component name="MavenImportPreferences">
    <option name="importingSettings">
      <MavenImportingSettings>
        <option name="downloadDocsAutomatically" value="true" />
        <option name="downloadSourcesAutomatically" value="true" />
        <option name="importAutomatically" value="true" />
      </MavenImportingSettings>
    </option>
  </component>

If the element exists previously, it is updated. However, if it previously contains any other options than
importAutomatically, it doesn't modify the settings file.

Usage: just run ./updater --help
"""
import logging
import xml.etree.ElementTree as ET
from optparse import OptionParser
from shutil import copyfile
from shutil import move
import glob
from os.path import isfile
import sys

__author__ = 'JuhoAutio'

# XML chunk being added

DOWNLOAD_DOCS_AUTOMATICALLY = \
    '        <option name="downloadDocsAutomatically" value="true" />\n'
DOWNLOAD_SOURCES_AUTOMATICALLY = \
    '        <option name="downloadSourcesAutomatically" value="true" />\n'
IMPORT_AUTOMATICALLY = \
    '        <option name="importAutomatically" value="true" />\n'
IMPORT_SETTINGS = \
    '\n    <option name="importingSettings">\n\
      <MavenImportingSettings>\n\
        ' + DOWNLOAD_DOCS_AUTOMATICALLY + '\
        ' + DOWNLOAD_SOURCES_AUTOMATICALLY + '\
        ' + IMPORT_AUTOMATICALLY + '\
      </MavenImportingSettings>\n\
    </option>\n'


def addDownloadDocs(struct):
    struct.append(ET.fromstring('<option name="downloadDocsAutomatically" value="true" />'))
    logging.info("added downloadDocsAutomatically=true")

def addDownloadSources(struct):
    struct.append(ET.fromstring('<option name="downloadSourcesAutomatically" value="true" />'))
    logging.info("added downloadSourcesAutomatically=true")

def addImportAutomatically(struct):
    struct.append(ET.fromstring('<option name="importAutomatically" value="true" />'))
    logging.info("added importAutomatically=true")

def addMavenImportPreferencestEl(project):
    project.append(ET.fromstring('\n<component name="MavenImportPreferences">\n\
    ' + IMPORT_SETTINGS + '\
  </component>\n'))
    logging.info("added MavenImportPreferences")

def addImportSettings(project):
    project.append(ET.fromstring(IMPORT_SETTINGS))
    logging.info("added importingSettings")

def allOptionsInPlace(options):
    all = ['importAutomatically', 'downloadDocsAutomatically', 'downloadSourcesAutomatically']
    return set(all) == set(map(lambda node: node.attrib['name'], options))

def writeFiles(file, xml):
    # write to a temporary file
    tempfile = file + "-temp"
    xml.write(tempfile)
    # copy the original into a backup
    copyfile(file, file + "-bak")
    # move the newly written file over the actual file
    move(tempfile, file)

def conditionalWrite(file, xml, write, message):
    if write:
        writeFiles(file, xml)
    return message

def update(file, write):

    try:
        xml = ET.parse(file)
    except ET.ParseError as err:
        print("ERROR: Couldn't parse file %s. Parsing failed with message '%s'." % (file, err.message))
        sys.exit(1)

    project = xml.getroot()
    maven = project.find("component[@name='MavenImportPreferences']")

    if not maven:

        # TODO test this case
        # add everything in one chunk
        addMavenImportPreferencestEl(project)
        return conditionalWrite(file, xml, write, "Update succeeded")

    elif len(maven) == 1:

        importingSettings = maven.find("option[@name='importingSettings']")

        if not importingSettings:

            # TODO test this case
            # add almost everything in one chunk
            addImportSettings(project)
            return conditionalWrite(file, xml, write, "Update succeeded")

        if len(importingSettings) != 1:

            # TODO test this case
            return "Skipping file '" + file + "' because it already contains: \n" + ET.tostring(importingSettings)

        else:

            options = importingSettings.find("MavenImportingSettings")

            if not options:

                # TODO test this case
                return "Skipping file '" + file + "' because didn't expect to not find MavenImportingSettings" \
                    "in this case.. This is not implemented, although it would be possible."

            elif len(options) == 1 and options[0].tag == 'option' and options[0].attrib['name'] == 'importAutomatically':

                logging.info("found importAutomatically option")

                addDownloadDocs(options)
                addDownloadSources(options)

                return conditionalWrite(file, xml, write, "added docs and sources")

            elif len(options) == 0:

                logging.info("found empty MavenImportingSettings")

                addDownloadDocs(options)
                addDownloadSources(options)
                addImportAutomatically(options)

                # TODO test this case
                return conditionalWrite(file, xml, write, "added docs, sources & import")

            elif allOptionsInPlace(options):

                return "All options already in place: \n" + ET.tostring(options)

            else:

                return "Skipping file '" + file + "' because it already contains: \n" + ET.tostring(options)

    else:

        # TODO test this case
        return "Skipping file '" + file + "' because it already contains: \n" + ET.tostring(maven)



# class access for unit testing
class Updater:

    def updateFile(self, file, write):
        return update(file, write)


#
# Script scope
#

def updateFiles(files):
    count = 0
    for file in files:
        if not isfile(file):
            print("ERROR: File doesn't exist with path %s" % file)
            sys.exit(1)
        logging.info('updating ' + file)
        result = update(file, True)
        if (not result and not (
            result.startswith("All options already in place")
            or result.startswith("Update succeeded")
            or result.startswith("added docs and sources")
        )):
            print(result)
        else:
            count += 1
            logging.info(result)
    print("updated %s files out of %s" % (count, len(files)))

# The commandline script runs here
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="directory",
                      help="directory of IDEA projects to scan & update. All immediate sub-folders are scanned for \
                           .idea/workspace.xml", metavar="FILE")
    parser.set_usage('%prog [<workspace file(s)>] [options]')
    (options, args) = parser.parse_args()

    # initialize info level logging to console
    logging.basicConfig(level=logging.WARNING)

    if args:
        updateFiles(args)
    elif options and options.directory:
        scanPattern = options.directory + "/*/.idea/workspace.xml";
        logging.info('scanning ' + scanPattern)
        files = glob.glob(scanPattern)
        if not files:
            logging.error('No workspace files found in the provided directory')
        else:
            updateFiles(files)
    else:
        print("\nERROR: No options or args provided.\n")
        parser.print_help()
        sys.exit(1)
