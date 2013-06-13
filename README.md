Amazon Utilties
============

This is a series of amazon utilities I wrote to manage resources on Amazon.  Right now it just manages S3 commits.

##Installation:

Install Dependencies (only run the line that pertains to your package manager):

```
(homebrew) $ brew install libjpeg
(macports) $ port install jpeg
(ubuntu)   $ sudo apt-get install libjpeg8
```

Clone the Repository and install the python dependencies:

```
$ git clone git://github.com/goodcodeguy/amazon-utils.git amazon-utils && cd amazon-utils
$ pip install -r deps.txt
```

##Usage:

__s3put__

```
$ ./s3put --config [configfile] srcdirectory s3bucket
```
You can also use the `-i` flag to create thumbnails on the fly __(requires libjpeg to be installed as described above)__

__s3get__

```
$ ./s3get --config [configfile] s3bucket destinationfolder
```


##Configuration:

Configuration syntax is YAML.  Take a look at `config/default.yaml` for an example.
