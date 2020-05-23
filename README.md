# JapScanDownloader

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/acf59998d8a743188d5f7ef058010ffa)](https://www.codacy.com/manual/Harkame/JapScanDownloader?utm_source=github.com&utm_medium=referral&utm_content=Harkame/JapScanDownloader&utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/eb654455df609c6fd1a2/maintainability)](https://codeclimate.com/github/Harkame/JapScanDownloader/maintainability)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Installation

This project depends on [Google Chrome][1] and [ChromeDriver][2], install them
first.

```console
pip install japscandownloader
```

## Usage

```console
$ japscandownloader
```

## Configuration

The program uses an configuration file. This file contains list of mangas to
download, destination path, etc.

Copy and edit the default configuration file (config.yml) to match your needs.

### Change image resolutions

Changing the image resolution is not yet a configurable attribute. Yet you can
edit the japscandownloader/jss_selenium.py file and change the `window-size` to
your desired resolution.

## TODO

- Tests with selenium
- Chapters folders name (not only number)
- Don’t download already downloaded manga/chapter/page
- Bug : Maximum connection try
- Bug : doublon/invalid first image

[1]: https://www.google.com/chrome
[2]: https://chromedriver.chromium.org
