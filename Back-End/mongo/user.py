from datetime import datetime, timedelta

from . import engine
from .publics import PublicCourse

import requests
import html
import json
import jwt
import os

# import urllib
# from urllib import request

# from selenium import webdriver
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

# import time

# from PIL import Image
# import pytesseract

__all__ = ['Boolean', 'Number', 'User', 'jwt_decode']

JWT_EXP = timedelta(days=int(os.environ.get('JWT_EXP', '10')))
JWT_ISS = os.environ.get('JWT_ISS', 'ntnu-course-taking.tw')
JWT_SECRET = os.environ.get('JWT_SECRET', 'SuperSecretStringByAisu')


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

    # GET 方法
    def get(self, url, **kwds):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = self.session.get(url, headers=headers, **kwds)
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

    def login(self):

        now_time = datetime.now()

        user = self.obj
        user.last_login_time = now_time
        user.save()

    def new_coming(self):

        data = self.ntnu_login()

        user_no_number = Number("User No").obj
        user_no = user_no_number.number

        version = Number("User data version").obj.number
        now_time = datetime.now()

        engine.User(user_no=user_no,
                    student_id=self.student_id,
                    password=self.password,
                    name=data['name'],
                    major=data['major'],
                    first_login_time=now_time,
                    last_login_time=now_time,
                    add_version=version,
                    now_version=version).save(force_insert=True)
        user_no_number.number += 1
        user_no_number.save()

    def ntnu_login(self):

        '''
        # 1st try
        # =========== 加入舊版爬蟲程式以獲取驗證碼 =========== #

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--disable-extensions')
        options.add_argument("--no-sandbox")
        # browser = webdriver.Chrome(executable_path = '/usr/lib/chromium-browser/chromedriver', chrome_options = options)
        browser = webdriver.Chrome(chrome_options = options)
        browser.get(Login_check_URL + '?language=TW')

        html = browser.page_source
        target = 'LoginCheckCtrl?action=login&id='
        login_id = html[html.find(target):html.find(target) + 100].split("'")[2]

        while True:
            try:
                verification_code_button = \
                    browser.find_element_by_id('imageBoxTurnIntoTextButton-btnEl')
                verification_code_button.click()
                break
            except:
                time.sleep(0.1)

        while True:
            try:
                verification_code = \
                    browser.find_element_by_xpath("//*[@id = 'messagebox-1001-displayfield-inputEl']/font/b").text
                ok_button = browser.find_element_by_id('button-1005-btnEl')
                ok_button.click()
                break
            except:
                time.sleep(0.1)

        # ================================================== #

        print(f"\n[*] Login ID: '{login_id}' / Validate code: '{verification_code}'.\n", end='')
        print(f"\n[*] Cookies from selenium: {browser.get_cookies()}\n", end='')
        print(f"\n[*] Cookies from request: {self.session.cookies}\n", end='')
        self.session.cookies.set('JSESSIONID', browser.get_cookies()[0]['value'], domain='cos2.ntnu.edu.tw')
        print(f"\n[*] Cookies from request: {self.session.cookies}\n", end='')

        # ================================================== #
        '''

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

        # print(f"\n[*] Login ID: '{login_id}' / Validate code: '{validate_code}'.\n", end='')

        params = { 'action': 'login', 'id': login_id }
        data = { 'userid': self.student_id, 'password': self.password, 'validateCode': validate_code, 'checkTW': '1' }
        r = self.post(Login_check_URL, params=params, data=data)

        # 這判定方法不太好
        # if '驗證碼錯誤' in r.text:
        #     print(f"\n[*] Validate code wrong, try again.\n", end='')
        #     pass
        # elif 'false' in r.text:
        if 'false' in r.text:
            print(f"\n[*] Student '{self.student_id}' login failed.\n", end='')
            raise ValueError
        else:
            print(f"\n[*] Student '{self.student_id}' login success.\n", end='')

        # 存取登入認證頁面
        params = { 'language': 'TW' }
        r = self.get(Index_URL, params=params)

        # 以絕對位置找出「學生姓名」: 尚未開發
        name = r.text[7675:7725].split("'")[1]

        # 發出點擊「下一頁」後會產生的封包
        data = { 'userid': self.student_id, 'stdName': name }
        self.post(Login_URL, data=data)

        # 存取「我的選課」頁面
        params = { 'action': 'go' }
        r = self.get(Enroll_URL, params=params)

        # 以絕對位置找出「學生主修系所」: 完成
        target = '系所:'
        major = r.text[r.text.find(target):r.text.find(target) + 50].split(">")[2]
        major = major[0:major.find('&')]

        return { 'name': name, 'major': major }

    # Not a good method (Only use for development)
    def update_data(self): # , major):

        version = Number("User data version").obj.number
        now_time = datetime.now()

        user = self.obj
        user.now_version = version
        # user.major = major
        user.last_login_time = now_time
        user.save()

    @property
    def watching_list(self):
        watching_list = [
            r.serial_no for r in self.obj.watching_courses
        ]
        return watching_list

    def add_watching_course(self, serial_no):
        user = self.obj
        pc = PublicCourse(serial_no).obj

        wc = engine.WatchingCourse(name=pc.v_chn_name,
                                   serial_no=serial_no,
                                   time_info=pc.time_info,
                                   teacher=pc.teacher,
                                   v_dept_chiabbr=pc.v_dept_chiabbr,
                                   credit=pc.credit,
                                   v_comment=pc.v_comment,
                                   v_limit_course=pc.v_limit_course)

        user.watching_courses.insert(0, wc)
        user.save()
   
    def cancel_watching_course(self, serial_no):
        user = self.obj
        user.watching_courses = [ 
            wc for wc in user.watching_courses if wc.serial_no != serial_no
        ]
        user.save()

    @property
    def taking_list(self):
        taking_list = [
            r.serial_no for r in self.obj.course_taking_records if r.status == 0
        ]
        return taking_list

    def add_taking_course(self, serial_no, domain):
        user = self.obj
        pc = PublicCourse(serial_no).obj
        
        now_time = datetime.now()

        ctr = engine.CourseTakingRecord(name=pc.v_chn_name,
                                        serial_no=serial_no,
                                        domain=domain,
                                        time_info=pc.time_info,
                                        teacher=pc.teacher,
                                        apply_time=now_time)

        user.course_taking_records.insert(0, ctr)
        user.save()

    # REALLY bad method
    def revoke_taking_course(self, serial_no):
        user = self.obj
        ctrs = [ ctr for ctr in user.course_taking_records \
                     if ctr.serial_no == serial_no and ctr.status == 0 ] # This is improper
        
        now_time = datetime.now()
        for record in ctrs:
            record.status = 2
            record.revoke_time = now_time
        user.save()

    @property
    def cookie(self):
        keys = ['studentId', 'name', 'major']
        # maybe 'gender', 'age', 'minor', 'program'
        return self.jwt(*keys)

    @property
    def secret(self):
        keys = ['studentId', 'password']
        return self.jwt(*keys, secret=True)

    def jwt(self, *keys, secret=False, **kwargs):
        if not self:
            return ''
        user = self.obj.reload().to_mongo()
        data = {k: user.get(k) for k in keys}
        data.update(kwargs)
        payload = {
            'iss': JWT_ISS,
            'exp': datetime.utcnow() + JWT_EXP,
            'secret': secret,
            'data': data
        }
        return jwt.encode(payload, JWT_SECRET, algorithm='HS256').decode()


def jwt_decode(token):
    try:
        json = jwt.decode(token,
                          JWT_SECRET,
                          issuer=JWT_ISS,
                          algorithms='HS256')
    except jwt.exceptions.PyJWTError:
        return None
    return json
