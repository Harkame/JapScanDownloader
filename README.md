# JapScanDownloader

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/acf59998d8a743188d5f7ef058010ffa)](https://www.codacy.com/app/Harkame/JapScanDownloader?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Harkame/JapScanDownloader&amp;utm_campaign=Badge_Grade)

[![Coverage Status](https://coveralls.io/repos/github/Harkame/JapScanDownloader/badge.svg?branch=master)](https://coveralls.io/github/Harkame/JapScanDownloader?branch=master)

[![Build Status](https://travis-ci.org/Harkame/JapScanDownloader.svg?branch=master)](https://travis-ci.org/Harkame/JapScanDownloader)

## Installation

[Python](https://www.python.org/downloads/)

``` bash
pip install -r requirements.txt
```

### Dependencies

[cloudflare-scrape](https://github.com/Anorov/cloudflare-scrape)

[Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

[PyYAML](https://github.com/yaml/pyyaml)

[tqdm](https://github.com/tqdm/tqdm)

[lxml](https://github.com/lxml/lxml.git)

## Usage

### Run

``` bash
python main.py
```

### Options

``` bash
-c, --config_file <configFile> : Set config file
  Example : ... -c /home/harkame/config.yaml
  Default : ./config_file.yaml

-d, --destination_path <destinationPath> : Set destination path where download mangas
  Example : ... -d /home/harkame/mangas
  Default : ./mangas

-h, --help : Print this help
  Example : ... -h

-v, --verbose : Activate verbose mod (debug, info, error)
  Example : ... -v
```

### How it work

This program use an config file (default : ./config.yaml)

This file contains list of mangas to download, destination path, etc.

### Download an manga

Add an entry to attribute mangas

``` yaml
mangas:
    url:
        https://www.japscan.cc/mangas/shingeki-no-kyojin/
    ...
    url:
        my_manga_url
```

#### URL : Url of the manga
:boom: Be careful to URL format :boom:

### Change downloads destination
Replace destinationPath's value by desired path

#### Linux

 ``` yaml
destinationPath:
    /home/harkame/mangas
```

#### Windows

 ``` yaml
destinationPath:
    F:\data\mangas
```
