Amazon Utilties
============

This is just a series of amazon utilities I wrote to manage resources on Amazon.  Right now it just manages S3 commits.

Installation:
=============

```
$ git clone git://github.com/goodcodeguy/amazon-utils.git
```

then change into the directory of the repo and run `pip install -r deps.txt` to install python dependencies.

Usage:
======

```
$ ./sync.py --config [path] srcdirectory s3bucket
```

You can also use the `-i` flag to create thumbnails on the fly

Configuration:
==============

Configuration syntax is YAML.  Take a look at `config/default.yaml` for an example.
