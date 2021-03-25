import random
import datetime
from baidu_utils import BaiduUtils
from dfss_utils import DFSSUtils

class Driver:
    def __init__(self, studentId, password, baiduAppId, baiduAppSecret):
        self.baidu = BaiduUtils(baiduAppId, baiduAppSecret)
        self.dfss = DFSSUtils(studentId, password)

    def initSetting(self):
        self.dfss.getCookies()
        # get valid code
        self.code = self.baidu.getValidCode(self.dfss.getValidPNG(), self.baidu.getAccessToken())
        # login
        self.dfss.login(self.code)

    def scan(self, lessonId, scope, start, end):
        
        today = datetime.date.today()
        for i in range(0, scope):
            date = today + datetime.timedelta(days=i)
            carList = self.dfss.getCarList(lessonId, date, start, end, self.code)

            humanList = []
            for car in carList:
                # Robot Car
                if car['fchrCarInfoID'][0] == '6' or not car['fchrCoachName']:
                    continue
                humanList.append(car)
                print("%s: %s-%s-%s"%(date, car['fchrCarInfoID'], car['fchrCarTypeName'], car['fchrCoachName']))
            
            if len(humanList) == 0:
                print("[*] %s没有符合条件的车辆!\n"%(date))

    def query(self, lessonId, date, start, end, flag):
        
        carList = self.dfss.getCarList(lessonId, date, start, end, self.code)

        humanList = []
        for car in carList:
            # Robot Car
            if car['fchrCarInfoID'][0] == '6' or not car['fchrCoachName']:
                continue
            print("%s: %s-%s-%s"%(date, car['fchrCarInfoID'], car['fchrCarTypeName'], car['fchrCoachName']))
            humanList.append(car)

        if len(humanList) == 0:
            print("[*] 没有符合条件的车辆!\n")
            exit(1)
        
        if flag == 1:
            randomCar = random.choice(humanList)
            self.dfss.bookCar(lessonId, date, 8, 12, randomCar['fchrCarInfoID'], randomCar['fchrReleaseCarID'], self.code)
            print("[*] 已约日期：%s， 车号：%s-%s-%s"%(date, randomCar['fchrCarInfoID'], randomCar['fchrCarTypeName'], randomCar['fchrCoachName']))

    def delayQuery(self, lessonId, date, start, end, flag):
        self.initSetting()
        self.query(lessonId, date, start, end, flag)