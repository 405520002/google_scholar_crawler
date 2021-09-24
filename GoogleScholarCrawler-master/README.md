# Google Scholar Crawler
This is a short python program that search, format, and download paper form google scholar.

## Requirements
1.先將chromedriver.exe所放置的路徑填入config.json中的chromedriver_path.  
2.config.json中的fpath填入google_scholar_crawler-main資料夾的路徑(要以雙斜線做區隔，最後也要加雙斜線).  
![log file sample](https://github.com/405520002/google_scholar_crawler/blob/main/gif1.PNG)



## Using this program
1. 在keyword:中打入想搜尋的論文主題(ex:live streaming);
2. 在require_page中輸入要爬的頁數(ex :1);
![log file sample](https://github.com/405520002/google_scholar_crawler/blob/main/gif2.PNG)
4. 執行.\\GoogleScholarCrawler-master\\dist中的GoogleScholarCrawler.exe;
5. 開始執行爬蟲程式 會在google_scholar_crawler的資料夾內顯示論文主題的資料夾，裡面會有論文pdf檔案，以及一個論文資訊整理的csv檔 (author, title, journal, year and whether pdf is avaliable).  
![log file sample](https://github.com/405520002/google_scholar_crawler/blob/main/GoogleScholarCrawler-master/log_file_sample.png). 

## 有些ＰＤＦ檔會下載失敗，若欲看下載失敗的論文請使用look_at_pdf.exe. 
1.點開./look_at//dist//look_at_pdf.exe. 

2.在choose subject 中輸入欲查看的論文主題，(論文主題必須要有對應的論文資訊csv檔案). 
3.在choose number 中輸入欲查看pdf的編號 （log file title左邊的欄位數字). 
![log file sample](https://github.com/405520002/google_scholar_crawler/blob/main/%E6%88%AA%E5%9C%96%202021-09-24%20%E4%B8%8B%E5%8D%8810.28.38.png). 
4.點選右下角look_pdf查看論文. 
![log file sample](https://github.com/405520002/google_scholar_crawler/blob/main/%E6%88%AA%E5%9C%96%202021-09-24%20%E4%B8%8B%E5%8D%8810.24.30.png). 




The pdf files will be renamed as:
`author-year-title-journal.pdf`



