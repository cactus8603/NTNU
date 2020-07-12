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

    def remove_user(self, user):
        taking_course = self.obj
        taking_course.request_list = [ r for r in taking_course.request_list if r.user != user.obj ]
        if len(taking_course.request_list) == 0:
            taking_course.is_performing = False
        taking_course.save()