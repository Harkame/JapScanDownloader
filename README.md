# JapScanDownloader

## Installation - Please keep dependencies updated

pip install -r requirements.txt -U

### Dependencies

  - [Beautiful Soup 4]()
  - [PyYAML]()
  - [lxml]()
  - [tqdm]()
  - [Pillow]()
  - [cloudscraper]()

## Usage

### Run

``` bash
python japscandownloader/main.py
```

### Options

``` bash
usage: main.py [-h] [-c CONFIG_FILE] [-d DESTINATION_PATH] [-f FORMAT] [-v]
               [-r] [-k] [-u]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        Set config file Example : python
                        japscandownloader/main.py -c /home/myconfigfile.yml
  -d DESTINATION_PATH, --destination_path DESTINATION_PATH
                        Set destination path of downloaded mangas Example :
                        python japscandownloader/main.py -d /home/mymangas/
  -f FORMAT, --format FORMAT
                        Set format of downloaded mangas Example : python
                        japscandownloader/main.py -f cbz|pdf|jpg|png
  -v, --verbose         Active verbose mode, support different level Example :
                        python japscandownloader/main.py -vv
  -r, --reverse         Reverse chapters download order (Default : Last to
                        first) Example : python japscandownloader/main.py -r
  -k, --keep            Keep downloaded images (when format is pdf/cbz)
                        (default : false) Example : python
                        japscandownloader/main.py -k
  -u, --unscramble      Force unscrambling Example : python
                        japscandownloader/main.py -u
```

### How it work

This program use an config file (default : ./config.yml)

This file contains list of mangas to download, destination path, etc.

#### Example of config file

``` yaml
mangas:
  - chapter:
      https://www.japscan.to/lecture-en-ligne/shingeki-no-kyojin/60/

  - url:
      https://www.japscan.to/manga/uq-holder/

  - chapters:
      url:
         https://www.japscan.to/lecture-en-ligne/black-clover/
      chapter_min:
         158
      chapter_max:
         197

destination_path:
  ./mangas/

manga_format:
  jpg
```

### Download an manga

Add an entry to attribute mangas

``` yml
mangas:
  - url:
      https://www.japscan.to/manga/uq-holder/

  - chapter:
      https://www.japscan.to/lecture-en-ligne/shingeki-no-kyojin/60/

  - chapters:
      url:
        https://www.japscan.to/lecture-en-ligne/black-clover/
      chapter_min:
        158
      chapter_max:
        197
```

3 supported format of download

Be careful to URL format :boom:

#### Manga

  - url : Url of the manga to download
