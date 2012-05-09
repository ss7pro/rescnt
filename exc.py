import sys


class ResourceExc(Exception):

    def __init__(self,where,res):
            self.where = where
            self.value = ('Resource: type=%(type)s zone=%(zone)s'
                            ' value=%(value)s parent=%(parent)s' % res) + (
                            'ExcInfo: %s' % sys.exc_info()[1])

    def __str__(self):
            return 'where:' + self.where + ' msg: ' + self.value
