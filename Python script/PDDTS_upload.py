
import time,requests,json
from selenium import webdriver
import configparser  # 引入模块
import pandas as pd
import openpyxl
config = configparser.ConfigParser()  # 类中一个方法 #实例化一个对象
config.read('config.ini')
username=config["userdata"]["username"]
password=config["userdata"]["password"]
user_data = {}
create_user=''

def get_token():
    # 打开浏览器登录并获取数据
    wd = webdriver.Chrome()
    wd.get("https://pddts.lenovo.com/pddts/myIssues")
    wd.find_element_by_id("mat-input-0").send_keys(username)
    time.sleep(2)
    wd.find_element_by_id("mat-input-1").send_keys(password)
    time.sleep(30)
    cookies = wd.execute_script("return window.localStorage")
    userDetails = json.loads(cookies['userDetails'])
    loginId=cookies['loginId']
    # 格式化处理登录返回的数据
    mtoken = userDetails['tokenId']
    global create_user
    create_user= str(
        userDetails['firstName'] + ' ' + userDetails['lastName'] + '<' + userDetails['emailAddress'] + '>')
    print(create_user)
    # 初始化用户请求数据
    user_data['loginId'] = loginId
    user_data['tokenId'] = mtoken
    return  user_data

def get_compoment(releaseId):#获取component数据
    user_data["releaseId"]=releaseId
    url=config['url']['compoment_url']
    compoment=requests.post(url=url,data=user_data)
    compomentarr = (json.loads(compoment.text)['response']['componentDetails'])
    # for i in compomentarr:
    #     print(i['releaseName'], i['componentName'], i['componentId'])
    user_data.pop("releaseId")
    return compomentarr
def get_compomentid(compoment_name,releaseId):
    compoment_name_arr=get_compoment(releaseId)
    compomentId=''
    for i in compoment_name_arr:
        if i["componentName"]==compoment_name:
            componentId= i['componentId']
    if componentId=="":
        return "None"
    else:
        return componentId

def get_release():#获取release数据
    url=config['url']['release_url']
    release=requests.post(url=url,data=user_data)
    releasearr=(json.loads(release.text)['response']['releaseDetails'])
    # for i in releasearr:
    #     print(i['releaseName'],i['releaseId'],i['releaseOwnerId'])

    return releasearr
def get_releaseid(release_name):
    release_name_arr=get_release()
    releaseId=''
    for i in release_name_arr:
        if i["releaseName"]==release_name:
            releaseId= i['releaseId']
    if releaseId=="":
        return "None"
    else:
        return releaseId


def get_priority():#获取priority数据
    url=config['url']['priority_url']
    priority=requests.post(url=url,data=user_data)
    priorityarr = (json.loads(priority.text)['response']['requestedPriorityDetails'])
    # for i in priorityarr:
    #     print(i['issueRequestPriorityName'], i['issueRequestPriorityId'])
    return priorityarr
def get_priorityid(priorityname):#获取priority数据
    priorityname_arr = get_priority()
    priorityid = ''
    for i in priorityname_arr:
        if i["issueRequestPriorityName"] == priorityname:
            priorityid = i['issueRequestPriorityId']
    if priorityid == "":
        return "None"
    else:
        return priorityid



def get_exceldata():
    # excel数据处理
    df = pd.DataFrame(pd.read_excel(r'./test1.xlsx'))
    list_name = list(df)
    req_data = []
    print("开始处理Excel数据")
    for i in range(len(df)):
        data={}
        data['answerCodeId'] = ''
        data['componentId'] = 0
        data['componentOwnerCombinedAG'] = ''
        data['contentTypeId'] = ''
        data['createdBy'] = create_user
        data['crossProduct'] = ''
        data['description'] = ""
        data['dispositionId'] = ''
        data['fixTargetStateId'] = ''
        data['generalCommentsNotes'] = ''
        data['issueNum'] = ''
        data['loginId'] = user_data['loginId']
        data['name'] = ""
        data['operatingSystemId'] = ''
        data['paTestcaseNum'] = ''
        data['phaseFoundId'] = ''
        data['prefixId'] = ''
        data['primaryEcrNum'] = ''
        data['primaryIssueNum'] = ''
        data['reOpenTimes'] = ''
        data['rejectReasonCodeId'] = ''
        data['releaseId'] = 0
        data['requestedPriorityId'] = 0
        data['stateId'] = 1
        data['symptomId'] = ''
        data['tokenId'] = user_data['tokenId']
        data['vendorBugNum'] = ''
        for j in list_name:
            if j not in {"component","Priority","releaseName"}:
                data[j] = df[j][i]
            if (j == "releaseName"):
                print(get_releaseid(df[j][i]))
                if (get_releaseid(df[j][i]) !="None"):
                    data['releaseId'] = int(get_releaseid(df[j][i]))
                    releaseID=get_releaseid(df[j][i])

                else:
                    print ("release %s不存在"%get_releaseid(df[j][i]))
                    break
            if (j=="component"):
                print(get_compomentid(df[j][i],releaseID))
                if (get_compomentid(df[j][i],releaseID)!="None"):
                    data['componentId'] = int(get_compomentid(df[j][i],releaseID))
                else:
                    print ("component不存在")
                    break
            if (j=="Priority"):
                print(get_priorityid(df[j][i]))
                if (get_priorityid(df[j][i])!="None"):
                    data['requestedPriorityId'] = int(get_priorityid(df[j][i]))
                else:
                    print ("Priority不存在")
                    break

        print(data)
        req_data.append(data)
        res=requests.post(url=config['url']['createBug_url'],data=data)
        res=json.loads(res.text)
        print(res)
        df.insert(0, 'issueNum', 0)
        df.loc[i, "issueNum"] = res['response']['issueNum']
    print(req_data)
    print("开始存储数据")
    file_name = str("./issueResult{}.xlsx").format(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
    df.to_excel(file_name)

if __name__=='__main__':
    start_get_token=input("按任意键开始")
    get_token()
    start_get_exceldata = input("按任意键继续,按R回车重新登录")
    if start_get_exceldata!="R":
        get_exceldata()
    else:
        get_token()
