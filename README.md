Clinvar Crawler
=============

Crawler data from NCBI clinvar by id

# Usage

- `scrapy crawl clinvar_crawler -a id=17662 -o out.json` comma separated ids
- `scrapy crawl clinvar_crawler -a file=input.txt -o out.json` input file, each id per line
