from cocoNLP.extractor import extractor
import os
import jieba
import re
import pdfplumber
from main import extractEntity

# 文件路径设置
stopwordsPath = os.path.join(os.getcwd(), 'stopwords.txt')
termsPath = os.path.join(os.getcwd(), 'terms.txt')
skillPath = os.path.join(os.getcwd(), 'skills.txt')

def ProcessInput(filename):
    '''
    输入简历路径，返回简历文本内容，存入 txt
    '''
    if '.doc' in filename:
        # word转pdf
        return None
    try:
        with pdfplumber.open(filename) as pdf:
            txt = ''
            for page in pdf.pages:
                txt += page.extract_text().strip()
    except Exception as e:
        print('There is an error during process input file : ', e )
        print('The input file name is ', filename)
        return None

    return txt

def ExtractInfo(text):

    '''
    输入简历文本内容，返回个人信息，存入字典 personalDict
    '''
    personalDict = {}
    ex = extractor()

    extract_name_uni = extractEntity(text)

    # 抽取姓名
    personalDict["name"] = extract_name_uni['per']

    # # 抽取学校
    personalDict["uni"] = extract_name_uni['org']

    # 抽取手机号
    cellphones = ex.extract_cellphone(text, nation='CHN')
    if cellphones:
        personalDict["cellphone"] = [i.strip() for i in cellphones][0]
    else:
        cellPattern = re.compile('1[0-9]{10}')
        cellphone = cellPattern.findall(text)
        personalDict['cellphone'] = cellphone[0]
    personalDict['id'] = personalDict['cellphone']

    # 抽取邮箱
    mailPattern = re.compile(r"(\w+@\w+\.\w+)")
    mail = mailPattern.findall(text)
    personalDict['mail'] = mail[0]

    # 抽取技能
    skillCut = extractSkills(text)
    personalDict['skill'] = skillCut

    txtList = text.split('\n')
    for i in range(len(txtList)):
        # 抽取岗位
        position = ['应聘岗位','应聘职位','求职意向','求职目标']
        for pos in position:
            if pos in txtList[i] :
                posPattern = '%s[:：]?([\s\S]*?)\Z' % pos
                posPattern = re.compile(posPattern)
                posResult = posPattern.findall(txtList[i])
                if posResult and posResult[0].strip() != '':
                    personalDict['position'] = posResult[0].strip()
                    break
                else:
                    personalDict["position"] = txtList[i+1].strip()
                    break

        # 抽取学历
        eduPattern = re.compile('学[\s\S]*?历[;：]([\S]{0,6})\s')
        edu = eduPattern.findall(txtList[i])
        if edu:
            personalDict['edu'] = edu[0].strip()

        # 抽取年龄
        ageKw = ['出生年月','年龄']
        line = ''.join(txtList[i].split())
        for a in ageKw:
            if a in line:
                agePattern = '%s[:：]?([\s0-9.]{0,7})' % a
                agePattern = re.compile(agePattern)
                age = agePattern.findall(line)
                if age:
                    personalDict['age'] = age[0]

    return personalDict

def stopwordslist():
    stopWordsFile = stopwordsPath
    stopwords = [line.strip() for line in open(stopWordsFile, 'r', encoding='utf-8').readlines()]
    return stopwords

def skillslist():
    skillwords = [line.strip() for line in open(skillPath, 'r', encoding='utf-8').readlines()]
    return skillwords

def extractSkills(text):
    '''
    单独处理‘个人技能’中的关键词
    '''
    skillwords = skillslist()
    cut = jieba.cut(text)
    outstr = []
    for word in cut:
        if word in skillwords:
            outstr.append(word)
    outstr = set(outstr)
    return '/ '.join(outstr)

if __name__ == "__main__":
    pass