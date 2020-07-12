from . import engine, user

__all__ = ['TakingCourse']


class TakingCourse:
    def __init__(self, serial_no):
        self.serial_no = serial_no

    @property
    def obj(self):
        try:
            obj = engine.TakingCourse.objects.get(serial_no=self.serial_no)
        except:
            return None
        return obj

    def new_course(self, user, domain):
        user = user.obj
        if domain is '':
            request = engine.Request(user=user)
            engine.TakingCourse(serial_no=self.serial_no,
                                request_list=[request]).save(force_insert=True)
        else:
            request = engine.Request(user=user, domain=domain)
            engine.TakingCourse(serial_no=self.serial_no,
                                is_general=True,
                                request_list=[request]).save(force_insert=True)

    def add_user(self, user, domain):
        taking_course = self.obj
        user_list = [ r.user for r in taking_course.request_list ]
        user = user.obj
        
        if user in user_list:
            raise ValueError
        
        if domain is '':
            request = engine.Request(user=user)
        else:
            request = engine.Request(user=user, domain=domain)

        taking_course.request_list.append(request)
        taking_course.is_performing = True
        taking_course.request_list = \
            sorted(taking_course.request_list, key = lambda r : r.user.vip_level, reverse=True)
        taking_course.save()

    def remove_user(self, user):
        taking_course = self.obj
        taking_course.request_list = [ r for r in taking_course.request_list if r.user != user.obj ]
        if len(taking_course.request_list) == 0:
            taking_course.is_performing = False
        taking_course.save()