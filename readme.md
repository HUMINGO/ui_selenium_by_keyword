**ui_framework**

`简介`

该框架是通过关键字驱动的ui自动化测试，只需要在test_cases目录下创建Excel文件，然后在Excel文件中创建测试用例，即可完成UI自动化测试用例的编写。此框架使用更加灵活，扩展性高。

`技术特点`

本框架使用Python+pytest+yaml+Excel+logging+allure等组件来搭建，实现了：

1、yaml文件自动读取；

2、yaml文件动态写入；

3、pytest_xlsx_run_step钩子函数自动读取Excel中的用例；

4、热加载函数；

5、日志管理；

6、html报告

7、其他

`使用`

1、通过Excel编写测试用例，Excel文件的名必须是test开头，后缀是.xlsx;

2、安装Python3.10环境，安装项目依赖，pip install -r requirements.txt，执行命令：python run.py