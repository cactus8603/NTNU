from . import engine

__all__ = ['PublicCourse']


class PublicCourse:
    def __init__(self, serial_no):
        self.serial_no = serial_no

    @property
    def obj(self):
        try:
            obj = engine.PublicCourse.objects.get(serial_no=self.serial_no)
        except:
            return None
        return obj

    def get_courses(deptCode, domnCode, name):
        
        courses = engine.PublicCourse.objects.order_by('serial_no')
        
        if name is not None:
            courses = [ c for c in courses if name in c.chn_name ]
        
        if deptCode is not None and deptCode != 'ALL':
            courses = [ c for c in courses if c.dept_code == deptCode ]
            if deptCode == 'GU' and domnCode is not None and domnCode != 'ALL':
                courses = [ c for c in courses if domnCode in c.courseCode ]

        return courses