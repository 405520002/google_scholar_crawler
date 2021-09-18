# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 22:15:47 2021

@author: wadep
"""
import pandas as pd
import os
import json
from selenium import webdriver
from tkinter import *
from PIL import ImageTk, Image



def look_at_pdf(file,thesis,chromedriver_path,fpath):
    try:
        path=fpath+'//'+file+'//'
        file_list=os.listdir(path)
        print(file_list)
        log_file=[x for x in file_list if '.csv' in x]
        print(log_file)
        pdf_file=pd.read_csv(path+log_file[0])
        print(pdf_file.columns)
        try:
            url=pdf_file[pdf_file['Unnamed: 0']==int(thesis)]['pdf'].iloc[0]
        except:
            print('no number')
        chrome_driver= webdriver.Chrome(chromedriver_path)
        chrome_driver.get(url)
    except Exception as e:
        print(e)
        print('no log file')
        
def open_chrome_reader(path,chromedriver_path,fpath):
       f2=open(path[:-12]+'config_look.json')
       config_look = json.load(f2)
       file=config_look['folder']
       thesis=config_look['number']
       look_at_pdf(file,thesis,chromedriver_path,fpath)
        
 
        
def make_gui(path,chromedriver_path,fpath):
    global literature,number,result_label
    def search():
        global literature,number,result_label
        s = str(literature.get())
        n = float(number.get())
        result={'number':n,'folder':s}
        print(result)
        with open(fpath +'GoogleScholarCrawler-master\\config_look.json', 'w') as fp:
            json.dump(result, fp)
        result = 'success'
        #將計算結果更新到 result_label 文字內容
        result_label.set(result)
        open_chrome_reader(path,chromedriver_path,fpath)
   
        
         
    tk=Tk()
    literature=StringVar()
    number=IntVar()
    result_label=StringVar()
    
    tk.title('look at literature pdf')
    
    Label(tk,text="choose subject").grid(row=0,sticky=E)#靠右
    Label(tk,text="choose number").grid(row=1,sticky=W)#第二行，靠左
    
    Entry(tk,textvariable=literature).grid(row=0,column=1,padx=10,pady=10)
    Entry(tk,textvariable=number).grid(row=1,column=1)
    
    
    
    
    
    photo = ImageTk.PhotoImage(Image.open(fpath+"GoogleScholarCrawler-master\\photo.jpg").resize((30, 30)))  
    label=Label(image=photo)
    label.grid(row=0,column=2,rowspan=2,columnspan=2,
    sticky=W+E+N+S, padx=5, pady=5)#合并两行，两列，居中，四周外延5个长度
    
    
    button1=Button(tk,text="look_pdf",command=search)
    button1.grid(row=2,column=2)
    Label(tk,textvariable=result_label).grid(row=2,sticky=E)
        
    
    
    #主事件循环
    mainloop()

    

        
    

if __name__ == '__main__':
    global literature,number,result_label
    path=os.getcwd()
    print(path)
    f=open(path[:-12]+'config.json')
    config = json.load(f)
    chromedriver_path=config['chromedriver_path']
    fpath = config['fpath']
    make_gui(path,chromedriver_path,fpath)
    
    
    

