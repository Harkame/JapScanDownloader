# JapScanDownloader

## Installation

``` bash
pip install cfscrape BeautifulSoup4 pyyaml lxml tqdm
```

### Dependencies

[cloudflare-scrape](https://github.com/Anorov/cloudflare-scrape)

[Beautiful Soup 4](https://beautiful-soup-4.readthedocs.io/en/latest/)

[PyYAML](https://github.com/yaml/pyyaml)

[tqdm](https://github.com/tqdm/tqdm)

## Usage

This program use an config file (config.yml)

 TODO
### Options

+ -c | --config_file : Path of config file
    + Default path is ./config_file.yml

### Download an manga
Add an entry to attribute mangas

Copy past to avoid synthax error

If an scan is already on the drive, it is not re-downloaded

``` yaml
mangas:
    url:
        https://www.japscan.cc/mangas/shingeki-no-kyojin/
    ...
    url:
        my_manga_url
```

#### URL : Url of the manga
Be careful to URL format

#### minimalChapter : Download all chapters from the last to minimalChapter (TODO)

Usefull to avoid full check of all chapters (Can take several time)

To download all chapters, set minimalChapter to 0

### Change downloads destination
Replace destinationPath's value by desired path

 ``` yaml
destinationPath:
    F:\data\mangas
    #OR
    /home/harkame/mangas
```
