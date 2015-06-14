# FeedFinder

## Description
* Gets a list of HTTP(s) URLs from an input file
* Fetches each page via GET
* Extracts the URLs of linked RSS and ATOM feeds and prints them to stdout

## Dependencies
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/), `$ pip install beautifulsoup4`

## Usage
```
$ python feedfinder.py <input.txt>
```

Command line arguments:

* `--user-agent`: perform HTTP requests with defined user agent
* `--no-check-certificate`: ignore SSL certificate validation errors
