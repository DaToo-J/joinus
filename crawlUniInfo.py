import requests
from bs4 import BeautifulSoup,element
import re
from multiprocessing import Pool
import pandas as pd



def crawlUni():
    uni = []
    for offset in range(21, 108):
        url = "http://college.gaokao.com/schlist/p%s/" % offset
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.findAll('dl')
        for t in table[1:-1]:
            try:
                uniInfo = {}
                uniInfo['uniName'] = t.strong.text
                uniInfo['feature'] = t.ul.get_text().split()[1].split('：')[-1]
                uniInfo['level'] = t.ul.get_text().split()[4].split('：')[-1]
                uni.append(uniInfo)
            except:
                print(t)

        print(url, '  has been done.')

    with open('university.txt', 'a', encoding='utf-8') as f:
        for u in uni:
            f.write(str(u) + '\n')
        print('university info has been written into the txt')

def processUni():
    uniList = pd.read_csv('uni.csv')
    uni = list(uniList['高校名称'])
    print(uni)

    with open('test_data_uni.txt', 'w', encoding='utf-8') as fw:
        for u in uni[2000:]:
            try:
                fw.writelines(u[0] + ' B-UNI\n')
                for i in u[1:]:
                    fw.writelines(i + ' I-UNI\n')
            except:
                print('except : ', u)

# processUni()

def crawlJob(offset):
    job = []
    # for offset in range(201,401):
    url = "https://jobs.51job.com/jisuanjiruanjian/p%s/" % offset
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.findAll('span', {'class': 'title'})
    for t in table:
        job.append(t.text.strip())

    print(url, '  has been done.')

    with open('job.txt', 'a', encoding='utf-8') as fw:
        for j in job:
            fw.write(j.strip() + '\n')
        print('Those jobs have been written into the txt~ ----- ')
    # return job

# for i in range(251,401):
#     try:
#         crawlJob(i)
#     except Exception as e:
#         print(i, e)

def processJob():
    with open('jobList.txt','r',encoding='utf-8') as fr:
        with open('test_data_job.txt', 'w', encoding='utf-8') as fw:
            for i in fr.readlines()[2000:]:
                # print(i.strip())
                fw.write(i.strip()[0]+ ' B-JOB\n')
                for _ in i.strip()[1:]:
                    fw.write(_ + ' I-JOB\n')
# processJob()

with open('test_data_job.txt', 'r', encoding='utf-8') as fr:
    fr = list(fr)
    print(len(fr))
    for l in fr:
        if len(l.split()) != 2:
            print('l : ',l)
            fr.remove(l)
    print(len(fr))
#
# with open('test_data_job.txt', 'w', encoding='utf-8') as fw:
#     for f in fr:
#         fw.write(f)
