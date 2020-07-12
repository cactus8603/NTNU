# Related third party imports
from flask import Blueprint, request

# Local application
from mongo import *
from .utils import *

__all__ = ['search_api']

search_api = Blueprint('search_api', __name__)


@search_api.route('/', methods=['POST'])
@Request.json('serial_no', 'dept_code', 'domn_code', 'name', 'time')
def search_courses(serial_no=None, dept_code=None, domn_code=None, name=None, time=None):
    try:
        courses = []

        if serial_no is not None:
            course = PublicCourse(str(serial_no)).obj
            if course is not None:
                courses = [ course ]
        else:
            courses = PublicCourse.get_courses(dept_code, domn_code, name)

        data = [
            *map(
                lambda course: {
                    'name': course.v_chn_name,
                    'serialNo': course.serial_no,
                    'courseCode': course.course_code,
                    'timeInfo': course.time_info,
                    'deptCode': course.dept_code,
                    'vDeptChiabbr': course.v_dept_chiabbr,
                    'teacher': course.teacher,
                    'vComment': course.v_comment,
                    'vLimitCourse': course.v_limit_course
                }, courses)
        ]
        return HTTPResponse('Success.', data=data)
    except Exception as ex:
        return HTTPError('The error reason: ' + str(ex), 404)