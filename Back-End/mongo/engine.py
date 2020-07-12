from mongoengine import *

import mongoengine
import os
from datetime import datetime

__all__ = [*mongoengine.__all__]

MONGO_HOST = os.environ.get('MONGO_HOST', 'mongomock://localhost')
connect('ntnu-course-taking', host=MONGO_HOST)


class Boolean(Document):
    name = StringField(required=True)
    boolean = BooleanField(default=True)


class Number(Document):
    name = StringField(required=True)
    number = IntField(default=1)


class PublicCourse(Document):
    chn_name = StringField(db_field='chnName')
    course_code = StringField(db_field='courseCode')
    credit = StringField()
    dept_code = StringField(db_field='deptCode')
    option_code = StringField(db_field='optionCode')
    serial_no = StringField(db_field='serialNo')
    teacher = StringField()
    time_info = StringField(db_field='timeInfo')
    v_chn_name = StringField(db_field='vChnName')
    v_comment = StringField(db_field='vComment')
    v_dept_chiabbr = StringField(db_field='vDeptChiabbr')
    v_limit_course = StringField(db_field='vLimitCourse')


class Request(EmbeddedDocument):
    user = ReferenceField('User')
    domain = StringField(default='')


class TakingCourse(Document):
    is_performing = BooleanField(db_field='isPerforming', default=True)
    serial_no = StringField(db_field='serialNo', required=True)
    is_general = BooleanField(db_field='isGeneral', default=False)
    request_list = ListField(EmbeddedDocumentField(Request), db_field='requestList', default=list)


class WatchingCourse(EmbeddedDocument):
    name = StringField(required=True)
    serial_no = StringField(db_field='serialNo', required=True)
    time_info = StringField(db_field='timeInfo')
    teacher = StringField()
    v_dept_chiabbr = StringField(db_field='vDeptChiabbr')
    credit = StringField()
    v_comment = StringField(db_field='vComment')
    v_limit_course = StringField(db_field='vLimitCourse')


class CourseTakingRecord(EmbeddedDocument):
    status = IntField(default=0)
    name = StringField(required=True)
    serial_no = StringField(db_field='serialNo', required=True)
    domain = StringField(default='')
    time_info = StringField(db_field='timeInfo')
    teacher = StringField()
    apply_time = DateTimeField(db_field='applyTime', required=True)
    revoke_time = DateTimeField(db_field='revokeTime', null=True)


class Notification(EmbeddedDocument):
    read = BooleanField(default=False)
    time = DateTimeField(required=True)
    content = StringField(required=True)


class User(Document):
    user_no = IntField(db_field='userNo', required=True)
    student_id = StringField(db_field='studentId', max_length=10, required=True)
    password = StringField(max_length=50, required=True)
    name = StringField(max_length=10, required=True)
    major = StringField(max_length=50, required=True)
    vip_level = IntField(db_field='vipLevel', default=1)
    watching_courses = ListField(EmbeddedDocumentField(WatchingCourse),
                                 db_field='watchingCourses',
                                 default=list)
    course_taking_records = ListField(EmbeddedDocumentField(CourseTakingRecord),
                                      db_field='courseTakingRecords',
                                      default=list)
    notifications = ListField(EmbeddedDocumentField(Notification), default=list)
    first_login_time = DateTimeField(db_field='firstLoginTime', required=True)
    last_login_time = DateTimeField(db_field='lastLoginTime', required=True)
    add_version = IntField(db_field='addVersion', required=True)
    now_version = IntField(db_field='nowVersion', required=True)
    minor = StringField(max_length=50, null=True)
    program = StringField(max_length=50, null=True)
    #user_id2 = StringField(db_field='userId2', max_length=24, default='')
    #email = EmailField(required=True, unique=True)
    #md5 = StringField(required=True)
    #active = BooleanField(default=False)
    #role = IntField(default=2, choices=[0, 1, 2])
    #profile = EmbeddedDocumentField(Profile, default=Profile)
    #editor_config = EmbeddedDocumentField(EditorConfig,
    #                                      db_field='editorConfig',
    #                                      default=EditorConfig,
    #                                      null=True)
    #contest = ReferenceField('Contest', db_field='contestId')
    #courses = ListField(ReferenceField('Course'))
    #submissions = ListField(ReferenceField('Submission'))
    #last_submit = DateTimeField(default=datetime.min)
    #AC_problem_ids = ListField(IntField(), default=list)
    #AC_submission = IntField(default=0)
    #submission = IntField(default=0)


'''
class Homework(Document):
    homework_name = StringField(max_length=64,
                                required=True,
                                db_field='homeworkName')
    markdown = StringField(max_length=10000, default='')
    scoreboard_status = IntField(default=0,
                                 choices=[0, 1],
                                 db_field='scoreboardStatus')
    course_id = StringField(required=True, db_field='courseId')
    duration = EmbeddedDocumentField(Duration, default=Duration)
    problem_ids = ListField(IntField(), db_field='problemIds')
    student_status = DictField(db_field='studentStatus')


class Contest(Document):
    name = StringField(max_length=64, required=True, db_field='contestName')
    scoreboard_status = IntField(default=0,
                                 choice=[0, 1],
                                 db_field='scoreboardStatus')
    course_id = StringField(db_field='courseId')
    duration = EmbeddedDocumentField(Duration, default=Duration)
    contest_mode = IntField(default=0, choice=[0, 1], db_field='contestMode')
    problem_ids = ListField(IntField(), db_field='problemIds')
    participants = DictField(db_field='participants')


class Course(Document):
    student_nicknames = DictField(db_field='studentNicknames')
    course_status = IntField(default=0, choices=[0, 1])
    course_name = StringField(max_length=64,
                              required=True,
                              unique=True,
                              db_field='courseName')
    teacher = ReferenceField('User', db_field='teacher')
    tas = ListField(ReferenceField('User'), db_field='tas')
    contests = ListField(ReferenceField('Contest', reverse_delete_rule=PULL),
                         db_field='contests')
    homeworks = ListField(ReferenceField('Homework', reverse_delete_rule=PULL),
                          db_field='homeworks')
    announcements = ListField(ReferenceField('Announcement'),
                              db_field='announcements')
    posts = ListField(ReferenceField('Post'), db_field='posts', default=list)


class ProblemCase(EmbeddedDocument):
    case_score = IntField(required=True, db_field='caseScore')
    memory_limit = IntField(required=True, db_field='memoryLimit')
    time_limit = IntField(required=True, db_field='timeLimit')
    input = StringField(required=True)
    output = StringField(required=True)


class ProblemTestCase(EmbeddedDocument):
    language = IntField(choices=[0, 1, 2])
    fill_in_template = StringField(db_field='fillInTemplate', max_length=16000)
    cases = ListField(EmbeddedDocumentField(ProblemCase, default=ProblemCase),
                      default=list)


class Problem(Document):
    problem_id = IntField(db_field='problemId', required=True, unique=True)
    courses = ListField(ReferenceField('Course'), default=list)
    problem_status = IntField(default=1, choices=[0, 1])
    problem_type = IntField(default=0, choices=[0, 1])
    problem_name = StringField(db_field='problemName',
                               max_length=64,
                               required=True)
    description = StringField(max_length=100000, required=True)
    owner = StringField(max_length=16, required=True)
    # pdf =
    tags = ListField(StringField(max_length=16))
    test_case = EmbeddedDocumentField(ProblemTestCase,
                                      db_field='testCase',
                                      required=True,
                                      default=ProblemTestCase,
                                      null=True)
    ac_user = IntField(db_field='ACUser', default=0)
    submitter = IntField(default=0)
    homeworks = ListField(ReferenceField('Homework'), default=list)
    contests = ListField(ReferenceField('Contest'), default=list)
    # user can view stdout/stderr
    can_view_stdout = BooleanField(db_field='canViewStdout', default=True)


class TestCaseResult(EmbeddedDocument):
    status = IntField(required=True)
    exec_time = IntField(required=True, db_field='execTime')
    memory_usage = IntField(required=True, db_field='memoryUsage')
    stdout = StringField(required=True)
    stderr = StringField(required=True)


class Submission(Document):
    problem = ReferenceField(Problem, required=True)
    user = ReferenceField(User, required=True)
    language = IntField(required=True, db_field='languageType')
    timestamp = DateTimeField(required=True)
    status = IntField(default=-2)
    score = IntField(default=0)
    cases = ListField(EmbeddedDocumentField(TestCaseResult), default=list)
    exec_time = IntField(default=-1, db_field='runTime')
    memory_usage = IntField(default=-1, db_field='memoryUsage')
    code = BooleanField(
        default=False)  # wheather the user has uploaded source code


class Message(Document):
    timestamp = DateTimeField(default=datetime.utcnow)
    sender = StringField(max_length=16, required=True)
    receivers = ListField(StringField(max_length=16), required=True)
    status = IntField(default=0, choices=[0, 1])  # not delete / delete
    title = StringField(max_length=32, required=True)
    markdown = StringField(max_length=100000, required=True)


class Inbox(Document):
    receiver = StringField(max_length=16, required=True)
    status = IntField(default=0, choices=[0, 1, 2])  # unread / read / delete
    message = ReferenceField('Message')


class Announcement(Document):
    status = IntField(default=0, choices=[0, 1])  # not delete / delete
    title = StringField(max_length=64, required=True)
    course = ReferenceField('Course', required=True)
    create_time = DateTimeField(db_field='createTime', default=datetime.utcnow)
    update_time = DateTimeField(db_field='updateTime', default=datetime.utcnow)
    creater = ReferenceField('User', required=True)
    updater = ReferenceField('User', required=True)
    markdown = StringField(max_length=100000, required=True)


class PostThread(Document):
    markdown = StringField(default='', required=True, max_length=100000)
    author = ReferenceField('User', db_field='author')
    course_id = ReferenceField('Course', db_field='courseId')
    depth = IntField(default=0)  # 0 is top post, 1 is reply to post
    created = DateTimeField(required=True)
    updated = DateTimeField(required=True)
    status = IntField(default=0, choices=[0, 1])  # not delete / delete
    reply = ListField(ReferenceField('PostThread', db_field='postThread'),
                      dafault=list)


class Post(Document):
    post_name = StringField(default='', required=True, max_length=64)
    thread = ReferenceField('PostThread', db_field='postThread')
'''