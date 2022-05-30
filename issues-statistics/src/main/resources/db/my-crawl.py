import requests
import sqlite3
import os
import sys
import json
from bs4 import BeautifulSoup
from subprocess import run
from json import JSONEncoder

print("【info】>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>开始>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
logStr = "【info】>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>开始>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + "\n"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
logStr = logStr + BASE_DIR + "\n"

# 输出日志文件
file = open(BASE_DIR + "/py_run.log", "w")

# 创建数据库连接
conn = sqlite3.connect(BASE_DIR + "/Issues.db")

try:
    gitlab_session = ""
    lableDictStr = ""
    lableDict = {}
    # gitlab_session = "1f98c3a9fdf6b4cd88c4b0d0690c4314"
    # lableDictStr = '{"11211":"0SU-Fifm", "11210":"0SU-Fpln", "11209":"0SU-Fpub", "11196":"1类别-缺陷", "11197":"1类别-需求", "11198":"2等级一般", "11199":"2等级-严重", "11201":"2等级-致命", "11202":"3加急-否", "11203":"3加急-是", "11206":"4状态-Closed", "11207":"4状态-fixed", "11204":"4状态-New", "11205":"4状态-Open", "11208":"4状态-再次出现"}'

    argvLen = len(sys.argv)
    if argvLen > 1 and sys.argv[1] is not None:
        gitlab_session = sys.argv[1]

    if argvLen > 2 and sys.argv[2] is not None:
        lableDictStr = sys.argv[2]
        lableDict = json.loads(lableDictStr)

    print("【info】入参1**********************************gitlab_session【" + gitlab_session + "】**********************************")
    logStr = logStr + "【info】入参1**********************************gitlab_session【" + gitlab_session + "】**********************************" + "\n"

    print("【info】入参2**********************************lableDictStr【" + lableDictStr + "】**********************************")
    logStr = logStr + "【info】入参2**********************************lableDictStr【" + lableDictStr + "】**********************************" + "\n"



    # １指定ajax-post请求的url（通过抓包进行获取）
    url = 'https://git.iec.io/uat_lsvo_issue/dev_lsvo/-/issues?scope=all&state=all'

    # 处理post请求携带的参数(从抓包工具中获取)
    data = {
        'authenticity_token': '6LDTCGPQDHQABCVHSxNYVmBU5BA40a0PZQasy+B2VA23v63n/U8oHNfK42QfFA9fsSBN8wQ3qEILuAGE2mqvCg==',
        'user[login]': '',
        'user[password]': '',
        'user[remember_me]': '0'
    }

    # 自定义请求头信息，相关的头信息必须封装在字典结构中
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }

    # 2.发起基于ajax的post请求
    # sidebar_collapsed=false; auto_devops_settings_dismissed=true; known_sign_in=; ;;
    cookie = {
        "sidebar_collapsed":"false",
        "auto_devops_settings_dismissed":"true",
        # "known_sign_in":known_sign_in,
        "_gitlab_session":gitlab_session,
        # "visitor_id":visitor_id,
        "event_filter":"all"
    }
    response = requests.get(url=url, data=data, headers=headers, cookies=cookie)

    #获取响应内容：响应内容为json串
    data = response.text
    soup = BeautifulSoup(data, "lxml")
    inputUserPassword = soup.find("input", {"id":"user_password"})

    if inputUserPassword is not None:
        raise Exception("登录会话失效，请检查配置！")

    # 获取最后一页页码
    totalPageSize = int(soup.find("li", {"class":"js-last-button"}).find("a").string)
    print("【info】**********************************共" + str(totalPageSize) + "页**********************************")
    logStr = logStr + "【info】**********************************共" + str(totalPageSize) + "页**********************************" + "\n"

    cur = conn.cursor()
    # cur.execute("drop table if exists T_issues")
    cur.execute("Create table if not exists T_issues(id int, issue_reference text, issue_title text, issue_milestone text, issue_assignee text, issue_su text, issue_type text, issue_level text, issue_prioritization text, issue_status text, creator text, createdtime text, version timestamp)")
    cur.execute("delete from T_issues")
    # run("notepad", shell=True)
    totalNum = 0
    idVal = 0
    # 循环爬取每一页issue列表
    for index in range(totalPageSize):
        # print("【info】**********************************第" + str(index + 1) + "页**********************************")
        logStr = logStr + "【info】**********************************第" + str(index + 1) + "页**********************************" + "\n"

        url = "https://git.iec.io/uat_lsvo_issue/dev_lsvo/-/issues?page=" + str(index + 1) + "&scope=all&state=all"
        response = requests.get(url=url, headers=headers, cookies=cookie)
        data = response.text
        soup = BeautifulSoup(data, "lxml")

        liElements = soup.find("ul", {"class":"content-list issues-list issuable-list"}).find_all("li", {"class":"issue"})
        for liElement in liElements:
            totalNum = totalNum + 1

            titleVal = liElement["data-qa-issue-title"]
            labelsVal = liElement["data-labels"].replace(" ", "")
            labelList = labelsVal[1:len(labelsVal)-1].split(",")

            # issue信息dev
            infoDevElement = liElement.find("div", {"class":"issuable-info"})

            # issue编号
            issueReference = infoDevElement.find("span", {"class":"issuable-reference"}).get_text().replace(" ", "").replace("\n", "").replace("\r", "")

            # 校验标签是否完整
            if len(labelList) < 5:
                print("【warn】**********************************数据弃用，【" + issueReference + "】issue标签不完整【" + labelsVal + "】**********************************")
                logStr = logStr + "【warn】**********************************数据弃用，【" + issueReference + "】issue标签不完整【" + labelsVal + "】**********************************" + "\n"
                continue

            issueSuLabelVal = lableDict.get(labelList[0])
            issueTypeLabelVal = lableDict.get(labelList[1])
            issueLevelLabelVal = lableDict.get(labelList[2])
            issuePrioritizationLabelVal = lableDict.get(labelList[3])
            issueStatusLabelVal = lableDict.get(labelList[4])

            if issueSuLabelVal is None or issueTypeLabelVal is None or issueLevelLabelVal is None or issuePrioritizationLabelVal is None or issueStatusLabelVal is None:
                print("【warn】**********************************数据弃用，issue标签为空**********************************")
                logStr = logStr + "【warn】**********************************数据弃用，issue标签为空**********************************" + "\n"
                continue

            # 作者span
            authoredSpanElement = infoDevElement.find("span", {"class":"issuable-authored"})
            # 创建时间
            timeVal = authoredSpanElement.find("time")["datetime"]
            # 创建人
            usernameVal = authoredSpanElement.find("a")["data-username"]

            assigneeLinkObj = liElement.find("div", {"class":"issuable-meta"}).find("a", {"class":"author-link"})
            assigneeLinkVal = "无指派"
            if assigneeLinkObj is not None:
                assigneeLinkVal = assigneeLinkObj["href"][1:]

            # 里程碑span
            milestoneVal = "无"
            milestoneSpanElement = infoDevElement.find("span", {"class":"issuable-milestone"})

            if milestoneSpanElement is not None:
                milestoneVal = milestoneSpanElement.find("a")
                milestoneVal = milestoneVal.get_text().replace(" ", "").replace("\n", "").replace("\r", "")

            idVal = idVal + 1
            insertStr = "insert into T_issues Values(" + str(idVal) + ", '" + issueReference + "', '" + titleVal.replace("'", "''") + "', '" + milestoneVal + "', '" + assigneeLinkVal + "', '" + issueSuLabelVal + "', '" + issueTypeLabelVal + "', '" + issueLevelLabelVal + "', '" + issuePrioritizationLabelVal + "', '" + issueStatusLabelVal + "', '" + usernameVal + "', '" + timeVal + "', datetime('now','localtime'))"
            # print("【debug】" + insertStr)
            logStr = logStr + "【debug】" + insertStr + "\n"
            cur.execute(insertStr)

    # 提交事务，关闭连接
    conn.commit()
    print("【info】**********************************已处理【" + str(idVal) + "/" + str(totalNum) + "】条issue**********************************")
    logStr = logStr + "【info】**********************************已处理【" + str(idVal) + "/" + str(totalNum) + "】条issue**********************************" + "\n"
except Exception as r:
    print("【error】 %s" %(r))
    logStr = logStr + r
finally:
    # 关闭数据库连接
    try:
        conn.close()
    except Exception as r:
        print("【error】关闭数据库连接出现异常 %s" %(r))
        logStr = logStr + r

    print("【info】<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<结束，详情请查看日志文件py_run.log<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    logStr = logStr + "【info】<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<结束<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" + "\n"

    # 写入日志文件
    try:
        file.write(logStr)
    except Exception as r:
        print("【error】写入日志文件出现异常 %s" %(r))
    finally:
        try:
            file.close()
        except Exception as r:
            print("【error】关闭文件流出现异常 %s" %(r))
