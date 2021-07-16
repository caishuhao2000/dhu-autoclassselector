from selector import *
from authorization import authorize
import time





username = ""
password = ""

username = input("请输入用户名:")
password = input("请输入密码：")

JSessionID,username,password = authorize(username,password)


set_username_password(username,password)

# while not flag:
#     print("请重新登录")
#     flag,JSessionID = authorize(username,password)



set_jsessionid(JSessionID)

courseID = input("请输入您想选择的课程编号:")

errormsg = ""
flag,errormsg = course_judge(courseID)

if not flag:
    print(errormsg)
    if errormsg.find("选课系统没有开放") != -1:
        exit()

flag,courses = get_course_details(courseID)
# courses = get_course_details("130271")

while not flag:
    courseID = input("请输入您想选择的课程编号:")
    flag,courses = get_course_details(courseID)

if len(courses[0]) - 1 > 1:
    print("(1-"+str(len(courses[0]) - 1)+")")
else:
    print("(1)")
c = int(input("请输入您想选择的课程序号:"))
    
while c not in range(1,len(courses[0])):
    print("请输入有效的课程序号.")
    print("(1-"+len(courses)+")")
    c = int(input("请输入您想选择的课程序号:"))

courseNum = courses[0][c]

while (True):
        
    if course_availablecheck(courseID,courseNum):
        flag1,errormsg = course_judge(courseNum)
        
        if not flag1:
            conflic_classNum = get_select_course_classNum(courseID)
            flag = course_delete(courseID,conflic_classNum)
            # while not flag:
            #     flag = course_delete(courseID,conflic_classNum)
        
        flag2,conflic_courseID = course_confliccheck(courseNum)

        # if not flag2:
        #     conflic_classNum = get_select_course_classNum(conflic_courseID)
        #     flag = course_delete(conflic_courseID,conflic_classNum)
        #     # while not flag:
        #     #     flag = course_delete(conflic_courseID,conflic_classNum)
        
        flag1 = course_judge(courseNum)
        flag2,conflic_courseID = course_confliccheck(courseNum)

        if flag1:
            course_select(courseNum)
            break
        else:
            continue
            
    time.sleep(1)
