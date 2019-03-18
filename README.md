# JapScanDownloader

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/acf59998d8a743188d5f7ef058010ffa)](https://www.codacy.com/app/Harkame/JapScanDownloader?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Harkame/JapScanDownloader&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/Harkame/JapScanDownloader.svg?branch=master)](https://travis-ci.org/Harkame/JapScanDownloader)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![codecov](https://codecov.io/gh/Harkame/JapScanDownloader/branch/master/graph/badge.svg)](https://codecov.io/gh/Harkame/JapScanDownloader)

## Installation

``` bash
pip install -r requirements.txt
```

## TODO

### Feature, etc
+   Chapters folders name (not only number)
+   Don't download already downloaded chapter
+   Option : Reverse exploration (Download chapters from first to last)

### Bug
+   Sometimes japscan website exploration don't start
    +   cfscrape problem ?

### Dependencies

[cloudflare-scrape](https://github.com/Anorov/cloudflare-scrape)

[Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

[PyYAML](https://github.com/yml/pyyml)

[tqdm](https://github.com/tqdm/tqdm)

[lxml](https://github.com/lxml/lxml.git)

[Pillow](https://github.com/python-pillow/Pillow.git)

## Usage

### Run

``` bash
python japscandownloader/main.py
```

### Options

``` bash
usage: main.py [-h] [-c CONFIG_FILE] [-d DESTINATION_PATH] [-f FORMAT] [-v]
               [-r REMOVE]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        Set config file Example : python
                        japscandownloader/main.py -c /home/myconfigfile.yml
  -d DESTINATION_PATH, --destination_path DESTINATION_PATH
                        Set destination path of downloaded config.mangas
                        Example : python japscandownloader/main.py -d
                        /home/mymangas/
  -f FORMAT, --format FORMAT
                        Set format of downloaded config.mangas Example :
                        python japscandownloader/main.py -f cbz
  -v, --verbose         Active verbose mode, support different level Example :
                        python japscandownloader/main.py -vv
  -r REMOVE, --remove REMOVE
                        remove downloaded images (when format is pdf/cbz)
                        (default : true) Example : python
                        japscandownloader/main.py -r false|f|no|n|0
```

### How it work

This program use an config file (default : ./config.yml)

This file contains list of mangas to download, destination path, etc.

#### Example  of config file

``` yaml

mangas:
  - url:
      https://www.japscan.to/manga/shingeki-no-kyojin/
  - url:
      https://www.japscan.to/manga/hunter-x-hunter/

destinationPath:
  ./mangas/

mangaFormat:
  pdf

```

### Download an manga

Add an entry to attribute mangas

``` yml
mangas :
    - url:
        https://www.japscan.cc/mangas/shingeki-no-kyojin/
    ...
    - url:
        my_manga_url
```

#### URL : Url of the manga
:boom: Be careful to URL format :boom:

### Change downloads destination
Replace destinationPath's value by desired path

#### Linux

 ``` yml
destinationPath:
    /home/harkame/mangas
```

#### Windows

 ``` yml
destinationPath:
    F:\data\mangas
```

#### Change Manga format

Replace mangaFormat value by desired format

Supported format
+   jpg/png (default) : Just download image file
+   pdf : Create PDF file
+   cbz : Create CBZ archive

``` yml
mangaFormat:
   jpg
```

## Test

### Dependencies

[tox](https://github.com/tox-dev/tox)

(Others are specified in tox.ini)

``` bash
  pip install tox

  tox
```
