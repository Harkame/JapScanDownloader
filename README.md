# JapScanDownloader

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/acf59998d8a743188d5f7ef058010ffa)](https://www.codacy.com/app/Harkame/JapScanDownloader?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Harkame/JapScanDownloader&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/Harkame/JapScanDownloader/badge.svg?branch=master)](https://coveralls.io/github/Harkame/JapScanDownloader?branch=master)
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
+   Code coverage, test
+   Don't download already downloaded chapter
+   Download scans from other website
+   Option : Reverse exploration (Download chapters from first to last)
+   Option : Don't remove downloaded png (pdf, cbz)

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
optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        Set config file
  -d DESTINATION_PATH, --destination_path DESTINATION_PATH
                        Set destination path of downloaded mangas
  -f FORMAT, --format FORMAT
                        Set format of downloaded mangas
  -v, --verbose         Active verbose mode, support different level
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
