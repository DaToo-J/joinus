# from cocoNLP.extractor import extractor
import os
import jieba
import re
import pdfplumber
from main import *
import logging
# 文件路径设置
stopwordsPath = os.path.join(os.getcwd(), 'stopwords.txt')
termsPath = os.path.join(os.getcwd(), 'terms.txt')

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
        logging(e)
        print('There is an error during process input file : ', e )
        print('The input file name is ', filename)
        return None

    return txt

def ExtractInfo(text):
    '''
    输入简历文本内容，返回个人信息，存入字典 personalDict
    '''
    personalDict = {}
    # ex = extractor()

    # 抽取姓名
    personalDict["name"] = extractName(text)

    # 抽取学校
    personalDict["uni"] = extractUni(text)

    # 抽取手机号
    # cellphones = ex.extract_cellphone(text, nation='CHN')
    # if cellphones:
    #     personalDict["cellphone"] = [i.strip() for i in cellphones][0]
    # else:
    #     cellPattern = re.compile('1[0-9]{10}')
    #     cellphone = cellPattern.findall(text)
    #     personalDict['cellphone'] = cellphone[0]
    # personalDict['id'] = personalDict['cellphone']

    # 抽取邮箱
    mailPattern = re.compile(r"(\w+@\w+\.\w+)")
    mail = mailPattern.findall(text)
    personalDict['mail'] = mail[0]

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
        eduPattern = re.compile('学[\s\S]*?历[;：]([\S\s]{0,6})')
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

        # 抽取技能
        skillKw = ['个人技能','专业技能','知识技能','职业技能','I T 技能']
        for s in skillKw:
            if s in line:
                skillList = [t.strip() for t in txtList[i+1:i+10] if t != ' ']
                skillStr = ' '.join(skillList)
                skillCut = extractSkills(skillStr)
                personalDict['skill'] = skillCut
                break

    return personalDict

def stopwordslist():
    stopWordsFile = stopwordsPath
    stopwords = [line.strip() for line in open(stopWordsFile, 'r', encoding='utf-8').readlines()]
    return stopwords

def extractSkills(skillLines):
    '''
    单独处理‘个人技能’中的关键词
    '''
    stopwords = stopwordslist()
    jieba.load_userdict(termsPath)
    skillStr = ''
    cut = jieba.cut(skillLines)
    outstr = ''
    for word in cut:
        if word not in stopwords and word != ' ':
            outstr += word
            outstr += "/ "
    skillStr += outstr

    return skillStr

def extractName(txt):
    # 提取人名
    extractName = ' '.join(txt.split()[:10])
    nameEntity = extractEntity(extractName)['per']
    # print('name:  ',nameEntity)
    if nameEntity:
        return nameEntity[0]

def extractUni(txt):
    UniEntity = extractEntity(txt)['org']
    for i in UniEntity:
        i = i.replace('\n', '')
        if ('大学' == i[-2:] )or ('学院'  == i[-2:]):
            # print('----- ',i)
            return i
    return 'null'

# def logging(e):
#     # 第一步，创建一个logger
#     logger = logging.getLogger("__abc__")
#     logger.setLevel(level=logging.DEBUG)  # Log等级开关
#
#     # 第二步，创建一个handler，用于写入日志文件
#     log_path = os.path.dirname(os.getcwd()) + '/tmp/'
#     log_name = log_path + 'log.txt'
#     logfile = log_name
#     file_handler = logging.FileHandler(logfile, mode='a+')
#     file_handler.setLevel(logging.ERROR)  # 输出到file的log等级的开关
#
#     # 第三步，定义handler的输出格式
#     formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
#     file_handler.setFormatter(formatter)
#
#     # 第四步，将handler添加到logger里面
#     logger.addHandler(file_handler)
#     logger.exception(msg=e)


if __name__ == "__main__":
    # pass
    namelist = ['1559561708000_ykbktjvoijlooyyl','1559560749000_fwpgjoysyhiqcmzh','1559561896000_xitzjhrxcxtwriwk','1559562681000_hmeyaluwemjloegu']
    personlist = []
    for n in namelist:
        filename = "C:/Users/Datoo/Desktop/简历/%s.pdf" % n
        txt = ProcessInput(filename)
        personDict = ExtractInfo(txt)
        personlist.append(personDict)
    # print(txt)
    # print('--------------------')
    # print(txt.split()[:10])

    print(personlist)