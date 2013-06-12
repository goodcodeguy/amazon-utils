import boto
import sys, os, shutil
from boto.s3.key import Key
from PIL import Image

import urllib2

def createThumbs(src):

  sys.stdout.write("Creating Thumbs...\n")
  sys.stdout.flush()

  for dirname, dirnames, filenames in os.walk(src):

    for filename in filenames:
      name, ext = filename.split('.')
      if ext == 'jpg':
        size = 800, 800
        im800 = Image.open(os.path.join(dirname, filename))
        im800.thumbnail(size, Image.ANTIALIAS)
        im800.save(dirname + "/" + name + "_800" + ".jpg")
        print "saving:", dirname + "/" + name + "_800" + ".jpg"

        size = 250, 250
        im250 = Image.open(os.path.join(dirname, filename))
        im250.thumbnail(size, Image.ANTIALIAS)
        im250.save(dirname + "/" + name + "_250" + ".jpg")
        print "saving:", dirname + "/" + name + "_250" + ".jpg"

        size = 75, 75
        im75 = Image.open(os.path.join(dirname, filename))
        im75.thumbnail(size, Image.ANTIALIAS)
        im75.save(dirname + "/" + name + "_75" + ".jpg")
        print "saving:", dirname + "/" + name + "_75" + ".jpg"

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


def makeFilesPublic(bucket):
  bucket_list = bucket.list()

  for l in bucket_list:
    l.set_acl('public-read')
    print "Set", str(l.key), "to 'public-read'"