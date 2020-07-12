# Related third party imports
from flask import Blueprint, request

# Local application
from mongo import *
from .utils import *
from .auth import login_required

__all__ = ['profile_api']

profile_api = Blueprint('profile_api', __name__)


@profile_api.route('/times', methods=['GET'])
@login_required
def get_times(user):
    try:
        data = [
            { 'key': '初次登入', 'value': user.obj.first_login_time.timestamp() },
            { 'key': '最後登入', 'value': user.obj.last_login_time.timestamp() }
        ]
        return HTTPResponse('Success.', data=data)
    except Exception as ex:
        return HTTPError('The error reason: ' + str(ex), 404)

@profile_api.route('/watchings', methods=['GET'])
@login_required
def get_watchings(user):
    try:
        data = [ {
            'name': wc.name,
            'serialNo': wc.serial_no,
            'timeInfo': wc.time_info,
            'teacher': wc.teacher,
            'vDeptChiabbr': wc.v_dept_chiabbr,
            'credit': wc.credit,
            'vComment': wc.v_comment,
            'vLimitCourse': wc.v_limit_course
        } for wc in user.obj.watching_courses ]

        return HTTPResponse('Success.', data=data)
    except Exception as ex:
        return HTTPError('The error reason: ' + str(ex), 404)

@profile_api.route('/takings', methods=['GET'])
@login_required
def get_takings(user):
    try:
        data = [ {
            'status': ctr.status,
            'name': ctr.name,
            'serialNo': ctr.serial_no,
            'domain': ctr.domain,
            'timeInfo': ctr.time_info,
            'teacher': ctr.teacher,
            'applyTime': ctr.apply_time.timestamp(),
            'revokeTime': ctr.revoke_time.timestamp() if ctr.revoke_time != None else None
        } for ctr in user.obj.course_taking_records ]

        return HTTPResponse('Success.', data=data)
    except Exception as ex:
        return HTTPError('The error reason: ' + str(ex), 404)

@profile_api.route('/lists', methods=['GET'])
@login_required
def get_lists(user):
    try:
        data = {
            'watchingList': user.watching_list,
            'takingList': user.taking_list
        }
        return HTTPResponse('Success.', data=data)
    except Exception as ex:
        return HTTPError('The error reason: ' + str(ex), 404)

@profile_api.route('/addwatch', methods=['POST'])
@login_required
@Request.json('serial_no: str')
def add_watch(user, serial_no):
    try:
        course = PublicCourse(serial_no).obj
        if course is None:
            return HTTPError('The error reason: PublicCourse not exist.', 403)

        if course.serial_no in user.watching_list:
            return HTTPError('The error reason: Course already watching.', 403)

        user.add_watching_course(serial_no)
        return HTTPResponse('Success.')

    except Exception as ex:
        return HTTPError('The error reason: ' + str(ex), 404)

@profile_api.route('/cancelwatch', methods=['POST'])
@login_required
@Request.json('serial_no: str')
def cancel_watch(user, serial_no):
    try:
        user.cancel_watching_course(serial_no)
        return HTTPResponse('Success.')
    except Exception as ex:
        return HTTPError('The error reason: ' + str(ex), 404)

@profile_api.route('/addtake', methods=['POST'])
@login_required
@Request.json('serial_no: str', 'domain: str')
def add_take(user, serial_no, domain):
    try:
        course = PublicCourse(serial_no).obj
        if course is None:
            return HTTPError('The error reason: PublicCourse not exist.', 403)

        if course.dept_code == 'GU' and domain == '':
            return HTTPError('The error reason: General course without domain.', 403)

        taking_course = TakingCourse(serial_no)
        if user.student_id != 'test':
            if taking_course.obj is None:
                taking_course.new_course(user, domain)
            else:
                taking_course.add_user(user, domain)

        user.add_taking_course(serial_no, domain)
        return HTTPResponse('Success.')

    except ValueError:
        return HTTPError('The error reason: Course already taking.', 403)

    except Exception as ex:
        return HTTPError('The error reason: ' + str(ex), 404)

@profile_api.route('/canceltake', methods=['POST'])
@login_required
@Request.json('serial_no: str')
def cancel_take(user, serial_no):
    try:
        if user.student_id != 'test':
            taking_course = TakingCourse(serial_no)
            if taking_course.obj is None:
                return HTTPError('The error reason: TakingCourse not exist.', 403)
            taking_course.remove_user(user)
        
        user.revoke_taking_course(serial_no)

        return HTTPResponse('Success.')

    except Exception as ex:
        return HTTPError('The error reason: ' + str(ex), 404)

@profile_api.route('/notifications', methods=['GET'])
@login_required
def get_notifications(user):
    try:
        data = [ {
            'read': n.read,
            'time': n.time.timestamp(),
            'content': n.content
        } for n in user.obj.notifications ]

        return HTTPResponse('Success.', data=data)
    except Exception as ex:
        return HTTPError('The error reason: ' + str(ex), 404)