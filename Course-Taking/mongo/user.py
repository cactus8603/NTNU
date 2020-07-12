from datetime import datetime, timedelta

import requests

from . import engine

import json

# import time

# from PIL import Image
# import pytesseract

__all__ = ['Boolean', 'Number', 'User']


# ================================================== 分隔線 ================================================== #

# 登入首頁頁面網址
Login_check_URL = "http://cos2.ntnu.edu.tw/AasEnrollStudent/LoginCheckCtrl"
# 獲取驗證碼圖片網址
Rand_image_URL = "http://cos2.ntnu.edu.tw/AasEnrollStudent/RandImage"
# 獲取驗證碼網址
Image_box_URL = "http://cos2.ntnu.edu.tw/AasEnrollStudent/ImageBoxFromIndexCtrl"
# 「下一頁」頁面網址
Index_URL = "http://cos2.ntnu.edu.tw/AasEnrollStudent/IndexCtrl"
# 按下「下一頁」按鈕後，發送封包的目標網址
Login_URL = "http://cos2.ntnu.edu.tw/AasEnrollStudent/LoginCtrl"
# 存取「我的選課」頁面 & 所有後續行動發送封包的目標網址
Enroll_URL = "http://cos2.ntnu.edu.tw/AasEnrollStudent/EnrollCtrl"
# 存取「加選」頁面網址
Course_query_URL = "http://cos2.ntnu.edu.tw/AasEnrollStudent/CourseQueryCtrl"
# 獲取「我的選課」表格內的所有課程網址
Stfseld_list_URL = "http://cos2.ntnu.edu.tw/AasEnrollStudent/StfseldListCtrl"

# ================================================== 分隔線 ================================================== #


class Boolean:
    def __init__(self, name):
        self.name = name

    @property
    def obj(self):
        try:
            obj = engine.Boolean.objects.get(name=self.name)
        except:
            return None
        return obj


class Number:
    def __init__(self, name):
        self.name = name

    @property
    def obj(self):
        try:
            obj = engine.Number.objects.get(name=self.name)
        except:
            return None
        return obj


class User:
    def __init__(self, student_id, password):
        self.student_id = student_id
        self.password = password
        self.session = requests.Session()

    @property
    def obj(self):
        try:
            obj = engine.User.objects.get(student_id=self.student_id)
            if self.password != obj.password:
                raise ValueError
        except:
            return None
        return obj

    @property
    def taking_list(self):
        taking_list = [
            r.serial_no for r in self.obj.course_taking_records if r.status == 0
        ]
        return taking_list

    # REALLY bad method
    def stop_taking_course(self, serial_no, reason):
        user = self.obj
        ctrs = [ ctr for ctr in user.course_taking_records \
                     if ctr.serial_no == serial_no and ctr.status == 0 ] # This is improper

        # if len(ctrs) == 0:
        #     raise IndexError
        
        now_time = datetime.now()
        for record in ctrs:
            record.status = 1 if reason == 'success' else 2
            record.revoke_time = now_time
            name = record.name
        
        if reason == 'success':
            content = '成功搶到課程：'
        elif reason == 'repeated':
            content = '中止重複加選課程：'
        elif reason == 'conflict':
            content = '中止衝堂課程：'
        notification = engine.Notification(time=now_time, content=content + name)
        user.notifications.insert(0, notification)

        user.save()

    # GET 方法
    def get(self, url, **kwds):
        r = self.session.get(url, **kwds)
        return r

    # POST 方法
    def post(self, url, **kwds):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = self.session.post(url, headers=headers, **kwds)
        return r

    # 于傑的方法 (用來代替 '.json()')
    @staticmethod
    def parse_json(s):
        j = ','.join(map(lambda t: (lambda u: f'"{t[:u]}"{t[u:]}')(
            t.find(':')), s[1:-1].split(',')))
        return json.loads(f'{{{j}}}')

    # 登入
    def ntnu_login(self):

        self.session.cookies.clear()
        params = { 'language': 'TW' }
        r = self.get(Login_check_URL, params=params)

        # 以絕對位置找出「Login id」: 完成
        target = 'LoginCheckCtrl?action=login&id='
        login_id = r.text[r.text.find(target):r.text.find(target) + 100].split("'")[2]

        r = self.get(Rand_image_URL)
        # f = open('validateCode.jpg', 'wb')
        # for chunk in r:
        #     f.write(chunk)
        # f.close()
        # try:
        #     image = Image.open('validateCode.jpg')
        #     # image = image.covert('L')
        # except:
        #     continue
        # validate_code = pytesseract.image_to_string(image)
        r = self.get(Image_box_URL)
        validate_code = self.parse_json(r.text)['msg']

        r = self.post(Login_check_URL, params = {
            'action': 'login',
            'id': login_id
        }, data = {
            'userid': self.student_id,
            'password': self.password,
            'validateCode': validate_code,
            'checkTW': '1'
        })

        # if '驗證碼錯誤' in r.text:
        #     pass
        # else:
        #     break
        # print('登入: ' + str(r) + ' - ' + r.text)

        # 存取登入認證頁面
        r = self.get(Index_URL, params = {'language': 'TW'})
        # print('存取登入認證頁面: ' + str(r) + ' - ' + r.text)

        # 發出點擊「下一頁」後會產生的封包
        r = self.post(Login_URL, data = {
            'userid': self.student_id,
            'stdName': self.obj.name
        })
        # print('發出點擊「下一頁」後會產生的封包: ' + str(r) + ' - ' + r.text)

        # 存取「我的選課」頁面
        r = self.get(Enroll_URL, params = {'action': 'go'})
        # print('存取「我的選課」頁面: ' + str(r) + ' - ' + r.text)

    # 切換到「加選」頁面
    def switch_to_add_course_page(self):
        r = self.get(Course_query_URL, params = {"action": "add"})
        # print('切換到「加選」頁面: ' + str(r) + ' - ' + r.text)

    # 加選課程
    def take_course(self, serial_no, domain):

        # 加選課程前置步驟 1/2
        r = self.post(Enroll_URL, data = {
            "action": "checkCourseTime",
            "serial_no": serial_no,
            "direct": "1"
        })
        # print('加選課程前置步驟 1/2: ' + str(r) + ' - ' + r.text)

        # 加選課程前置步驟 2/2
        r = self.post(Enroll_URL, data = {
            "action": "checkDomain",
            "serial_no": serial_no,
            "direct": "1"
        })
        # print('加選課程前置步驟 2/2: ' + str(r) + ' - ' + r.text)

        # 如果課程非通識
        if domain == '':
            r = self.post(Enroll_URL, params = {
                "action": "add",
                "serial_no": serial_no,
                "direct": "1"
            })
            # print('如果課程非通識: ' + str(r) + ' - ' + r.text)
        # 如果課程是通識
        else:
            r = self.post(Enroll_URL, data = {
                "action": "add",
                "serial_no": serial_no,
                "direct": "1",
                "guDomain": domain
            })
            # print('如果課程非通識: ' + str(r) + ' - ' + r.text)

        # 輸出網頁回傳結果內容
        return r.json()