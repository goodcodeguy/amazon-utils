#!/usr/bin/env python

APPNAME = "Amazon S3 File Sync"
VERSION = 1.0
VERSION_STR = APPNAME + " " + str(VERSION)

import os, optparse, yaml

from bklib import *

def main():
  usage = "usage: %prog [options] src dst"
  config = None

  p = optparse.OptionParser(usage=usage, version=VERSION_STR)
  p.add_option('-i', '--images', default=False, action="store_true", dest="createThumbs")
  p.add_option('-c', '--config', default='config/default.yaml', metavar="FILEPATH", dest='configFile')

  options, arguments = p.parse_args()

  # Perform options and Arguments Checks

  if(not(os.path.exists(options.configFile))):
    p.error("Configuration file '{path}' does not exist.".format(path=options.configFile))

  if len(arguments) < 2:
    p.error("You need to specify a source directory and a destination bucket")

  if not(os.path.exists(arguments[0])):
    p.error("The source path '{path}' does not exist.".format(path=arguments[0]))

  # Load Configuration Settings
  try:
    with open(options.configFile) as f:
      config = yaml.load(f)
  except IOError:
    p.error("An error occurred when trying to open '{path}' for configuration".format(path=options.configFile))
  except yaml.scanner.ScannerError:
    p.error("An error occurred when trying to read '{path}' for configuration. Possibly due to a format error.".format(path=options.configFile))

  # Begin Processing Media
  if options.createThumbs == True:
    amazon.createThumbs(arguments[0])

  if 'amazon' not in config or 'access_key_id' not in config['amazon'] or 'access_key_secret' not in config['amazon']:
    p.error("Please specify the amazon access key and access secret in your configuration file.")

  amazon.uploadThumbs(arguments[0], arguments[1], config['amazon']['access_key_id'], config['amazon']['access_key_secret'])


if __name__ == '__main__':
  main()
