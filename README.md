# 3gpp-archive-download

A python spider to download 3gpp's [archive documents](https://www.3gpp.org/ftp/Specs/archive).

## How to use it

`python 3gpp_archive.py -h`

```commandline
usage: 3gpp_archive.py [-h] [-m] [-s SERIES]                                                 
                                                                                             
Download 3gpp documents                                                                      
                                                                                             
optional arguments:                                                                          
  -h, --help            show this help message and exit                                      
  -m, --multithread     enable multithreaded                                                 
  -s SERIES, --series SERIES                                                                 
                        set the series indices that you need to download, 
                        separated by commas
```
## Example

`python 3gpp_archive.py -s 23,38` means that download 23,38 series documents without multithread.

`python 3gpp_archive.py -s 01 -m` means that download 01 series documents with multithread.

`python 3gpp_archive.py -s 00,36 -m` means that download 00,36 series documents with multithread.


## Features

- [x] Automatically match the structure with 3gpp's [archive documents](https://www.3gpp.org/ftp/Specs/archive), detect the files that have not been downloaded.
- [x] Automatically extract zip files.
- [x] Error log
- [x] Support to download any series.
- [x] Multi-Thread
- [ ] Asynchronous
