import boto
import sys, os, shutil
from boto.s3.key import Key
from PIL import Image

import urllib2

def createThumbs(src, thumb_config=None):

  if thumb_config == None:
    thumb_config = {
      '75' : { 'w': 75, 'h': 75 },
      '500' : { 'w': 500, 'h': 500 },
      '800' : { 'w': 800, 'h': 800 }
    }

  sys.stdout.write("Creating Thumbs...\n")
  sys.stdout.flush()

  for dirname, dirnames, filenames in os.walk(src):

    for filename in filenames:
      name, ext = filename.split('.')
      if ext == 'jpg':
        for label, thumb_size in thumb_config.iteritems():
          size = thumb_size['w'], thumb_size['h']
          im = Image.open(os.path.join(dirname, filename))
          im.thumbnail(size, Image.ANTIALIAS)
          im.save(dirname + "/" + name + "_" + str(label) + ".jpg")
          sys.stdout.write("Saving: " + dirname + "/" + name + "_" + str(label) + ".jpg...\n")
          sys.stdout.flush()

def uploadThumbs(src, bucket_name, aws_access_id, aws_access_secret):
  updated_keys = 0

  # connect to the bucket
  conn = boto.connect_s3(aws_access_id, aws_access_secret)

  bucket = conn.get_bucket(bucket_name)

  for dirname, dirnames, filenames in os.walk(src):
    for filename in filenames:
      name, ext = filename.split('.')
      if ext == 'jpg':

        if updated_keys >= 100:
          # Close and Reopen connection
          conn.close()

          conn = boto.connect_s3(aws_access_id, aws_access_secret)

        key_dir = dirname.replace(os.path.abspath(src), '')
        sys.stdout.write("saving: " + key_dir + "/" + filename)
        k = Key(bucket)
        k.key = key_dir + "/" + filename
        k.set_contents_from_filename(os.path.join(dirname, filename),cb=done_cb)
        k.set_acl('public-read')
        sys.stdout.write("\n")
        sys.stdout.flush()
        updated_keys = updated_keys + 1

def done_cb(complete, total):
  sys.stdout.write('.')
  sys.stdout.flush()

def getAssets(bucket_name, dest, aws_access_id, aws_access_secret):
  conn = boto.connect_s3(aws_access_id, aws_access_secret)
  bucket = conn.get_bucket(bucket_name)

  # Add trailing slash if it isn't there
  if dest[:-1] != '/':
    dest = dest + '/'

  for l in bucket.list():
    keyString = str(l.key)

    path = os.path.dirname(keyString)
    filename = os.path.basename(keyString)

    if path[0:2] == './':
      path = path[2:]

    if not os.path.exists(dest + path):
      os.makedirs(dest + path)
    
    if not os.path.exists(dest + path + "/" + filename):
      sys.stdout.write('Downloading ' + keyString + ' [' + bucket_name + '] to ' + dest + path + "/" + filename)
      l.get_contents_to_filename(dest + path + "/" + filename, cb=done_cb)
      sys.stdout.write("\n")
      sys.stdout.flush()


def makeFilesPublic(bucket):
  bucket_list = bucket.list()

  for l in bucket_list:
    l.set_acl('public-read')
    print "Set", str(l.key), "to 'public-read'"