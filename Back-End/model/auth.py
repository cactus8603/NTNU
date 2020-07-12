# Standard library
from functools import wraps

# Related third party imports
from flask import Blueprint, request

# Local application
from mongo import *
from .utils import *

__all__ = ['login_required', 'auth_api']

auth_api = Blueprint('auth_api', __name__)


def login_required(func):
    '''Check if the user is login
    Returns:
        - A wrapped function
        - 403 Not logged in
        - 403 Invalid token
        - 403 Authorization expired
    '''
    @wraps(func)
    @Request.cookies(vars_dict={'token': 'piann'})
    def wrapper(token, *args, **kwargs):
        if token is None:
            return HTTPError('Not logged in.', 403)
        json = jwt_decode(token)
        if json is None or not json.get('secret'):
            return HTTPError('Invalid token.', 403)
        user = User(json['data']['studentId'], json['data']['password'])
        if json['data'].get('password') != user.obj.password:
            return HTTPError('Authorization expired.', 403)
        kwargs['user'] = user
        return func(*args, **kwargs)

    return wrapper


@auth_api.route('/session', methods=['GET', 'POST'])
def session():

    def logout():
        cookies = {'piann': None, 'jwt': None}
        return HTTPResponse('Goodbye!', cookies=cookies)

    @Request.json('student_id: str', 'password: str')
    def login(student_id, password):
        try:
            version = Number("User data version").obj.number

            user = User(student_id, password)

            if user.obj is None:
                user.new_coming()
            # Not a good method (Only use for development)
            elif user.obj.now_version is not version:
                user.update_data() # , account.major)
            elif user.obj.vip_level < 1:
                raise Exception
            else:
                user.login()

            # data = account.major

            cookies = { 'piann': user.secret, 'jwt': user.cookie }
            return HTTPResponse('Success.', cookies=cookies) # , data=data)

        except ValueError:
            return HTTPError('The error reason: Id or password invalid.', 403)

        except Exception as ex:
            return HTTPError('The error reason: ' + str(ex), 404)

    methods = { 'GET': logout, 'POST': login }
    return methods[request.method]()