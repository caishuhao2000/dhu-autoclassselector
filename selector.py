import requests
from authorization import authorize

headers = {
    'Host': 'jwgl.dhu.edu.cn',
    'Content-Length' : '12',
    'Accept' : 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With' : 'XMLHttpRequest',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64',
    'Content-Type' : 'application/x-www-form-urlencoded;charset=UTF-8',
    'Origin' : 'http://jwgl.dhu.edu.cn',
    'Referer' : 'http://jwgl.dhu.edu.cn/dhu/selectcourse/toSH',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language' : 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cookie': '',
    'Connection' : 'close'
}

username = ""
password = ""

def get_content_length(p : dict) -> int:  #读取data段长度

    character_length = 0

    for i in range(len(p)):
        character_length += len(list(p.keys())[i]) + len(list(p.values())[i])
    
    punctuation_mark_length = len(p) * 2 - 1
    total_length = character_length + punctuation_mark_length
    return total_length
        
def set_jsessionid(JSessionID : str):
    headers['Cookie'] ='array=jwgl_03; array=jwgl_03; JSESSIONID=' + JSessionID + '; array=jwgl_03'
    return True

def set_username_password(username : str,password :str):
    username = username
    password = password



def get_course_list(studentNo : str, semester : str) -> list:  #读取课程列表

    data = {
        'studNo' : studentNo,
        'scSemester' : semester
    }

    headers['Content-Length'] = str(get_content_length(data))

    r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/initTSCourses", headers=headers,data = data)

    print(r.text)


def get_course_details(courseID : str):  #读取课程详细信息
    data = {
        'sEcho' : '1',
        'iColumns' : '10',
        'sColumns' : '',
        'iDisplayStart' : '0',
        'iDisplayLength' : '-1',
        'mDataProp_0' : 'cttId',
        'mDataProp_1' : 'classNo',
        'mDataProp_2' : 'maxCnt',
        'mDataProp_3' : 'applyCnt',
        'mDataProp_4' : 'enrollCnt',
        'mDataProp_5' : 'priorMajors',
        'mDataProp_6' : 'techName',
        'mDataProp_7' : 'cttId',
        'mDataProp_8' : 'cttId',
        'mDataProp_9' : 'cttId',
        'iSortCol_0' : '0',
        'sSortDir_0' : 'asc',
        'iSortingCols' : '1',
        'bSortable_0' : 'false',
        'bSortable_1' : 'false',
        'bSortable_2' : 'false',
        'bSortable_3' : 'false',
        'bSortable_4' : 'false',
        'bSortable_5' : 'false',
        'bSortable_6' : 'false',
        'bSortable_7' : 'false',
        'bSortable_8' : 'false',
        'bSortable_9' : 'false',
        'courseCode' : courseID
    }

    headers['Content-Length'] = str(get_content_length(data))

    # proxies = {
    # 'http' : 'http://127.0.0.1:8080',
    # 'https' : 'http://127.0.0.1:8080'
    # }

    r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/initACC", headers=headers,data = data)
    # r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/initACC", headers=headers,data = data,proxies=proxies,verify=False)
    
#    print(r.text)

    try:
        response_json = r.json()
    except:
        JsessionID,_,_ = authorize(username,password)
        set_jsessionid(JsessionID)
        r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/initACC", headers=headers,data = data)
        response_json = r.json()
    

    if response_json['success'] != True:
        print(response_json['msg'])
        return False,""
    
    courses = ["courseNum"],["TeacherName"],["roomNum"],["courseWeek"],["classTime"],["maxcount"],["enrollcount"],["applycount"],[True]
    
    for i in range(len(response_json['aaData'])):
        courses[0].append(response_json['aaData'][i]['cttId'])
        courses[1].append(response_json['aaData'][i]['techName'])
        courses[2].append(response_json['aaData'][i]['roomcode1'])
        courses[3].append(response_json['aaData'][i]['useWeek1'])
        courses[4].append(response_json['aaData'][i]['classTime1'])
        if response_json['aaData'][i]['roomcode1'] != "":
            courses[2][i + 1] += " " + response_json['aaData'][i]['roomcode2']
        if response_json['aaData'][i]['useWeek2'] != "":
            courses[3][i + 1] += " " + response_json['aaData'][i]['useWeek2']
        if response_json['aaData'][i]['classTime2'] != None:
            courses[4][i + 1] += " " + response_json['aaData'][i]['classTime2']
        courses[5].append(response_json['aaData'][i]['maxCnt'])
        courses[6].append(response_json['aaData'][i]['enrollCnt'])
        courses[7].append(response_json['aaData'][i]['applyCnt'])

        if courses[6][i + 1] < courses[5][i + 1]:
            courses[8].append(True)
        else:
            courses[8].append(False)

    print(courses)

    return True,courses

def get_select_course_details():  #读取已选课程信息

    headers['Content-length'] = '0'

    r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/initSelCourses", headers=headers)

    # print(r.text)

    try:
        response_json = r.json()
    except:
        JsessionID,_,_ = authorize(username,password)
        set_jsessionid(JsessionID)
        r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/initSelCourses", headers=headers)
        response_json = r.json()

    if response_json['success'] != True:
        print(response_json['msg'])
        return False,""

    courses = ["courseID"],["classNumber"],["TeacherName"],["roomNum"],["courseWeek"],["classTime"]
    
    for i in range(len(response_json['enrollCourses'])):
        courses[0].append(response_json['enrollCourses'][i]['courseCode'])
        courses[1].append(response_json['enrollCourses'][i]['classNo'])
        courses[2].append(response_json['enrollCourses'][i]['teachName'])
        courses[3].append(response_json['enrollCourses'][i]['classRoom1'])
        courses[4].append(response_json['enrollCourses'][i]['useWeek1'])
        courses[5].append(response_json['enrollCourses'][i]['classTime1'])
        if response_json['enrollCourses'][i]['classRoom2'] != "":
            courses[3][i + 1] += " " + response_json['enrollCourses'][i]['classRoom2']
        if response_json['enrollCourses'][i]['useWeek2'] != "":
            courses[4][i + 1] += " " + response_json['enrollCourses'][i]['useWeek2']
        if response_json['enrollCourses'][i]['classTime2'] != None:
            courses[5][i + 1] += " " + response_json['enrollCourses'][i]['classTime2']

    print(courses)
        
    return True,courses

def get_select_course_classNum(courseID: str):
    
    _,select_courses = get_select_course_details()
    
    classNum = ""

    for i in range(len(select_courses[0])):
        if select_courses[0][i] == courseID:
            classNum = str(select_courses[1][i])
            return True,classNum
    
    return False,classNum



def course_availablecheck(courseID : str, courseNum :str) -> bool :  #检测课程人数是否已满


    data = {
        'sEcho' : '1',
        'iColumns' : '10',
        'sColumns' : '',
        'iDisplayStart' : '0',
        'iDisplayLength' : '-1',
        'mDataProp_0' : 'cttId',
        'mDataProp_1' : 'classNo',
        'mDataProp_2' : 'maxCnt',
        'mDataProp_3' : 'applyCnt',
        'mDataProp_4' : 'enrollCnt',
        'mDataProp_5' : 'priorMajors',
        'mDataProp_6' : 'techName',
        'mDataProp_7' : 'cttId',
        'mDataProp_8' : 'cttId',
        'mDataProp_9' : 'cttId',
        'iSortCol_0' : '0',
        'sSortDir_0' : 'asc',
        'iSortingCols' : '1',
        'bSortable_0' : 'false',
        'bSortable_1' : 'false',
        'bSortable_2' : 'false',
        'bSortable_3' : 'false',
        'bSortable_4' : 'false',
        'bSortable_5' : 'false',
        'bSortable_6' : 'false',
        'bSortable_7' : 'false',
        'bSortable_8' : 'false',
        'bSortable_9' : 'false',
        'courseCode' : courseID
    }

    headers['Content-Length'] = str(get_content_length(data))

    r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/initACC", headers=headers,data = data)

#    print(r.text)

    try:
        response_json = r.json()
    except:
        JsessionID,_,_ = authorize(username,password)
        set_jsessionid(JsessionID)
        r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/initACC", headers=headers,data = data)
        response_json = r.json()

    if response_json['success'] != True:
        print(response_json['msg'])
        return False
    
    for i in range(len(response_json['aaData'])):
        if courseNum == response_json['aaData'][i]['cttId']:
            break

    max_count = response_json['aaData'][0]['maxCnt']
    enroll_count = response_json['aaData'][0]['enrollCnt']
    apply_count = response_json['aaData'][0]['applyCnt']

    if enroll_count < max_count:
        print("课程可选")
        return True
    else:
        print("课程人数已满")
        return False


    


def course_judge(courseNum: str):  #检测课程是否已选
    
    data = {
        'courseCode' : courseNum
    }

    headers['Content-Length'] = str(get_content_length(data))

    r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/accessJudge", headers=headers,data = data)

    # print(r.text)

    try:
        response_json = r.json()
    except:
        JsessionID,_,_ = authorize(username,password)
        set_jsessionid(JsessionID)
        r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/accessJudge", headers=headers,data = data)
        response_json = r.json()

    if response_json['success']:
        return True,""
    elif response_json['msg'].find("不允许再次选择了") != -1:
        print("检测到与已选课程冲突")
        # print(response_json['msg'])
        return False,""
    else:
        # print(response_json['msg'])
        return False,response_json['msg']
    

def course_confliccheck(courseNum : str):  #检测课程与已有课程时间是冲突

    data = {
        'cttId' : courseNum
    }

    # content_length = len('cttId') + 1 + len(courseNum)

    headers['Content-Length'] = str(get_content_length(data))

    r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/scConflictCheck", headers=headers,data = data)

#    print(r.text)

    if r.status_code != 200:
        print("Error code:",r.status_code)
        return False

    try:
        response_json = r.json()
    except:
        JsessionID,_,_ = authorize(username,password)
        set_jsessionid(JsessionID)
        r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/scConflictCheck", headers=headers,data = data)
        response_json = r.json()

    if response_json['success']:
        return True, ""
    elif(response_json['msg'].find("冲突") != -1):
        print(response_json['msg'])
        print("检测到与已选课程冲突")
        conflic_course = response_json['msg'][response_json['msg'].find("(") + 1:response_json['msg'].find(")")] 
        return False, conflic_course
    else:
        print(response_json['msg'])
        return False ,""

def course_select(courseNum : str , ifNeedMeterial = True) -> bool:  #选择给定课程
    
    data = {
        'cttId' : courseNum,
        'needMaterial' : str(ifNeedMeterial)
    }

    # content_length = len('cttId') + 1 + len(courseNum) + 1 + len('needMaterial') + 1 + len(str(ifNeedMeterial))

    headers['Content-Length'] = str(get_content_length(data))

    r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/scSubmit", headers=headers,data = data)

#    print(r.text)

    if r.status_code != 200:
        print("Error code:", r.status_code)
        return False
    
    try:
        response_json = r.json()
    except:
        JsessionID,_,_ = authorize(username,password)
        set_jsessionid(JsessionID)
        r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/scSubmit", headers=headers,data = data)
        response_json = r.json()

    if response_json['success']:
        print("选课成功")
        return True
    else:
        print("选课失败")
        print(response_json['msg'][0])
        return False

def course_delete(courseID : str, classNum : str) -> bool:  #删除给定课程

    data = {
        'courseCode' : courseID,
        'classNo' : classNum,
        'cancelType' : '1'
    }

    headers['Content-Length'] = str(get_content_length(data))

    r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/cancelSC", headers=headers,data = data)

    # print(r.text)

    try:
        response_json = r.json()
    except:
        JsessionID,_,_ = authorize(username,password)
        set_jsessionid(JsessionID)
        r = requests.post("http://jwgl.dhu.edu.cn/dhu/selectcourse/cancelSC", headers=headers,data = data)
        response_json = r.json()

    if response_json['success']:
        print("课程删除成功")
        return True
    else:
        print("课程删除失败")
        return False



# if __name__ == '__main__':

    # courseID = input("Please input the courseID of the course you want:")
    # courses = get_course_details(courseID)
    # # courses = get_course_details("130271")
    # c = int(input("Please choose the course you want:"))
    
    # while c not in range(len(courses)):
    #     print("Please input valid number of the course.")
    #     c = int(input("Please choose the course you want:"))

    # courseNum = courses[0][c]

    # while (True):
        
    #     if course_availablecheck(courseID,courseNum):
    #         if course_confliccheck(courseNum):
    #             course_select(courseNum)
    #             break
    #     time.sleep(1)

    
    
    # get_course_list("191310624","20212022a")

    # course_judge("131361")
    
    # course_select("246360")

    # get_course_details("130132")
    
    # _,conflic_course = course_confliccheck("246381")

    # course_select("246381")

    # flag1,classNum = get_select_course_classNum("130461")

    # if flag1:
    #     course_delete("130461",classNum)
    

