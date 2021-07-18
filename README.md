DHU自动选课系统

在选课时由于学校网络不稳定导致没有选到心仪的课，为了能实时监控选课情况并及时选课而开发了这个系统
（这里吐槽一下DHU的选课系统，在学校内使用内网选课十分稳定，使用vpn访问返回系统错误页面，等系统正常的时候课都选完了）

我会尽可能根据教务处选课系统调整代码
系统目前仍有许多地方需要修改和改进，如遇问题请多多见谅


使用方法：


pip install -r requirements.txt
python main.py

使用时根据提示输入用户名和密码
接着输入课程代码
根据返回的课程信息选择课程

系统会先检查课程是否可选
若人数已满，则会不断检测直至课程可选
选择课程时会先检测课程是否有冲突，若有冲突会先删除冲突课程再选择该课程（一定要确认选择的课程是否优先于其他课程！）

程序执行选择或删除课程后请及时确认选择结果
若系统在执行过程中出现问题，请提交issue并说明具体情况，谢谢！

希望这个系统能帮助到大家

目前发现问题：
1.课程信息只支持显示两个时间段
2.若有两个或两个以上的课程时间冲突会导致程序错误

