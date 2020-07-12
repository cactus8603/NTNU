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