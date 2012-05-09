from rescnt import resource
from rescnt import exc
from rescnt import db

class Counter(object):

    def __init__(self):

        self.db = db.Db()
        self.resource = resource.Resource(self.db)

    def add(self,resource_id,type,value,added):
        """Add counter to the databases. Count delta if previous entry present.

        """
        r = self.db.get_last_counter_entry(resource_id,type)
        if not r:
            r = {}
            r['added'] = None
            delta = 0
        else:
            delta = value - r['value']
        if delta < 0:
            # This could happen on compute machine reboot, vm hard reboot,
            # vm live migration or just counter overrun.
            # As code tries to be as universal as it can be it's enough safe
            # to assume that in a such situation counter started from zero. 
            delta = value

        return self.db.add_counter_entry(resource_id,type,value,delta,added,r['added'])

    def ensure_resource(self,type,zone,name,parent=None):
        """Ensure resource is present in the database
        """
        return self.resource.ensure(type,zone,name,parent)
