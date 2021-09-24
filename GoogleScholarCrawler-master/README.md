# Google Scholar Crawler
This is a short python program that search, format, and download paper form google scholar.

## Requirements
1.先將chromedriver.exe所放置的路徑填入config.json中的chromedriver_path ;
2.config.json中的fpath填入google_scholar_crawler-main\\資料夾的路徑(要以雙斜線做區隔)
![log file sample](https://github.com/405520002/google_scholar_crawler/blob/main/gif1.PNG)



## Using this program
1. 
2. open terminal and cd to the target folder;
3. in target folder, change "config.json" file to change search keywords and target journals accordingly;
4. in terminal, use
```shell
python GoogleScholarCrawler.py config.json
```



In each folder, there is an excel log file recorded detailed search results (author, title, journal, year and whether pdf is avaliable).
There will also be all the pdf files that are publicly accessible in Google Scholar.

Here is how the log file will look like:
![log file sample](https://github.com/405520002/google_scholar_crawler/blob/main/gif1.PNG)

The pdf files will be renamed as:
`author-year-title-journal.pdf`


## Get in touch
You can find me at
`nico921113[at]gmail[dot]com`
