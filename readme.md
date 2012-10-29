Image Namer
==========

Version 0.6 - Mon 29 Oct 2012

by Reimund Trost <reimund@code7.se> 
Website <http://lumens.se/imagenamer/>


Description
-----------
Renames images in a directory, sorted by date.


    usage: imagenamer.py [-h] [-i input dir] [-s string] [-d digits] [-v]
                         [--skip-xmp] [--keep-case]  

    optional arguments:
      -h, --help     show this help message and exit
      -i input dir   rename images in this directory.
      -s string      the resulting files will have this prefix.
      -d digits      the number of digits to use.
      -v, --verbose  verbose output.
      --skip-xmp     don't rename xmp files.
      --keep-case    don't alter the case of the extension.


Requirements
------------
Requires EXIF.py.


Changelog
=========

0.6
---
* Rename xmp files (default, disable with --skip-xmp)
* Now writes extensions in lowercase (default, disable with --keep-case)

0.5
---
* Basic renaming features.
