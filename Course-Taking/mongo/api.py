# 導入函式庫
import requests
# import json

# ================================================== 分隔線 ================================================== #

# 登入首頁頁面網址
Login_check_URL = "http://cos2.ntnu.edu.tw/AasEnrollStudent/LoginCheckCtrl"
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


__all__ = ['Course', 'Account']


DEBUG = False


class Course:
    def __init__(self, name, serial_no, domain=None):

        # 課程名稱
        self.name = name
        # 課程代碼
        self.serial_no = serial_no

        # domain 為領域 (通識課程才有)，domain_code 為領域代號
        if domain == None:
            self.domain = None
            self.domain_code = None
        elif "語言" in domain:
            self.domain = "語言與文學"
            self.domain_code = "00UG"
        elif "藝術" in domain:
            self.domain = "藝術與美感"
            self.domain_code = "01UG"
        elif "哲學" in domain:
            self.domain = "哲學思維與道德推理"
            self.domain_code = "02UG"
        elif "公民" in domain:
            self.domain = "公民素養與社會探究"
            self.domain_code = "03UG"
        elif "歷史" in domain:
            self.domain = "歷史與文化"
            self.domain_code = "04UG"
        elif "數學" in domain:
            self.domain = "數學與邏輯思維"
            self.domain_code = "05UG"
        elif "科學" in domain:
            self.domain = "科學與生命"
            self.domain_code = "06UG"


class Account:
    def __init__(self, student_id, password, name=None):
        self.student_id = student_id
        self.password = password
        self.session = requests.Session()

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

    # 存取登入首頁，獲取「發送『登入請求封包』的目標網址後綴 ID」
    @property
    def login_id(self):
        self.session.cookies.clear()
        params = {"language": "TW"}
        r = self.get(Login_check_URL, params=params)

        # Find 'Login id' by absolute position: Done
        target = 'LoginCheckCtrl?action=login&id='
        output = r.text[r.text.find(target):r.text.find(target) + 100].split("'")[2]
        if DEBUG:
            print(f"\n[*] Login id: {output}\n\n", end='')

        return output
        
    # 登入
    def login(self):
    
        # 發送登入請求
        login_id = self.login_id
        params = {"action": "login", "id": login_id} 
        data = {"userid": self.student_id, "password": self.password}
        r = self.post(Login_check_URL, params=params, data=data)

        # 這判定方法不太好
        if "false" in r.text:
            print(f"\nStudent '{self.student_id}' login failed.\n\n", end='')
            raise ValueError
        print(f"\nStudent '{self.student_id}' login success.\n\n", end='')

        # 存取登入認證頁面
        params = {"language": "TW"}
        r = self.get(Index_URL, params=params)

        # 以絕對位置找出「學生姓名」: 尚未開發
        name = r.text[7675:7725].split("'")[1]
        if DEBUG:
            print(f"\n[*] Student's name: {name}\n\n", end='')
        self.name = name

        # 發出點擊「下一頁」後會產生的封包
        data = {"userid": self.student_id, "stdName": self.name}
        self.post(Login_URL, data=data)

        # 存取「我的選課」頁面
        params = {"action": "go"}
        r = self.get(Enroll_URL, params=params)

        # 以絕對位置找出「學生主修系所」: 完成
        target = '系所:'
        major = r.text[r.text.find(target):r.text.find(target) + 50].split(">")[2]
        major = major[0:major.find('&')]
        self.major = major

    # 獲取「我的選課」表格內的所有課程
    def get_my_courses(self):
        params = {"action": "showGrid"}
        r = self.get(Stfseld_list_URL, params=params)
        # beauty_r = json.dumps(r, indent = 4)
        # print(beauty_r)
        
    # 切換到「加選」頁面
    def switch_to_add_course_page(self):
        params = {"action": "add"}
        self.get(Course_query_URL, params=params)

    # 準備 (登入 + 切換到「加選」頁面)
    def ready(self):
        try:
            self.login()
            self.switch_to_add_course_page()
        except:
            raise

    # 加選課程 (跑一次清單便結束)
    def add_course(self, course_list):

        for course in course_list:

            # 加選課程前置步驟 1/2
            data = {
                "action": "checkCourseTime",
                "serial_no": course.serial_no,
                "direct": "1"
            }
            r = self.post(Enroll_URL, data=data)

            # 加選課程前置步驟 2/2
            data = {
                "action": "checkDomain",
                "serial_no": course.serial_no,
                "direct": "1"
            }
            r = self.post(Enroll_URL, data=data)

            # 如果課程非通識
            if course.domain == None:
                params = {
                    "action": "add",
                    "serial_no": course.serial_no,
                    "direct": "1"
                }
                r = self.post(Enroll_URL, params=params)
            # 如果課程是通識
            else:
                data = {
                    "action": "add",
                    "serial_no": course.serial_no,
                    "direct": "1",
                    "guDomain": course.domain_code
                }
                r = self.post(Enroll_URL, data=data)

            # 輸出網頁回傳結果內容
            print(r.text)

    # 加選課程 (完整功能)
    # def add_course_until_done(self, course_list):
