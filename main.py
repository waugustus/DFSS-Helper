#!/usr/bin/env python
# -*- coding: utf-8 -*-


from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import json
import getopt
import sys
from driver import Driver

lesson_scope = {
    "001": 7,
    "002": 36,
    "041": 36,
    "007": 36,
    "008": 36
}

time_scope = {
    "1": [8, 12],
    "2": [12, 16],
    "3": [16, 20]
}

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.loads(f.read())
    studentId = config['dfss']['studentId']
    password = config['dfss']['password']
    baiduAppId = config['baidu']['appId']
    baiduAppSecret = config['baidu']['appSecret']
    
    if len(sys.argv) == 1 or sys.argv[1] not in ['scan', 'query']:
        print('''
            [*] Usage: python main.py actions [params]
            [*] Actions:
                help 获取帮助列表
                scan 扫描模式，从本日扫描指定天数的数据（数据由课程类型决定：散段7天，桩训及科三36天）
                query 查询模式，查询指定日期的可用非AI车辆列表
            [*] Params:
                -w 查询结束后直接随机从结果中选择教练进行预约
                -l 指定课程类型ID，ID对应关系如下：
                    001: 散段
                    002: 桩训
                    041: 科三场内
                    007: 综合训练
                    008: 考前路训
                -t 课程时间ID，ID对应关系如下：
                    1: 8:00-12:00
                    2: 12:00-16:00
                    3: 16:00-20:00
                -d 查询日期，满足YYYY-MM-DD格式
                -s 定时执行命令，日期满足YYYY-MM-DD格式
        ''')
        exit(1)
    flag = 0
    schedule_date = ""
    lessonId = "000"
    timeId = ""
    schedule_date = ""
    date = ""

    opts, args = getopt.getopt(sys.argv[2:], "wl:t:s:d:")
    for opt_name,opt_value in opts:
        if opt_name == '-w':
            flag = 1
        elif opt_name == '-l':
            lessonId = opt_value
        elif opt_name == '-t':
            timeId = opt_value
        elif opt_name == '-s':
            schedule_date = opt_value
        elif opt_name == '-d':
            date = opt_value

    if lessonId not in lesson_scope:
        print('''
            [*] 课程ID不合法!
            [*] -l 指定课程类型ID，ID对应关系如下：
                    001: 散段
                    002: 桩训
                    041: 科三场内
                    007: 综合训练
                    008: 考前路训
        ''')
        exit(1)
    if timeId not in time_scope:
        print('''
            [*] 时间ID不合法!
            [*] -t 指定课程时间ID，ID对应关系如下：
                1: 8:00-12:00
                2: 12:00-16:00
                3: 16:00-20:00
        ''')
        exit(1)
    if schedule_date:
        try:
            datetime.datetime.strptime(schedule_date, "%Y-%m-%d")
        except ValueError:
            print("[x] 定时日期时间格式错误，时间格式应满足yyyy-MM-dd.\n")
            exit(1)
    if date:
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("[x] 目标日期时间格式错误，时间格式应满足yyyy-MM-dd.\n")
            exit(1)

    start = time_scope[timeId][0]
    end = time_scope[timeId][1]

    driver = Driver(studentId, password, baiduAppId, baiduAppSecret)

    if sys.argv[1] == 'scan':
        driver.initSetting()
        driver.scan(lessonId, lesson_scope[lessonId], start, end)
    elif sys.argv[1] == 'query':
        if schedule_date:
    
            print("[*] 进入定时模式，将在%s 06:00:00执行脚本.\n"%(schedule_date))
            year = int(schedule_date.split("-")[0])
            month = int(schedule_date.split("-")[1])
            day = int(schedule_date.split("-")[2])
            hour = 6
            minute = 0
            second = 0
            
            exec_datetime = datetime.datetime(year, month, day, hour, minute, second)

            sched = BlockingScheduler()
            sched.add_job(driver.delayQuery, 'date', run_date=exec_datetime, args=[lessonId, date, start, end, flag])
            sched.start()
        else:
            driver.initSetting()
            driver.query(lessonId, date, start, end, flag)

    
    
