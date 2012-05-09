import sys
import exc
import MySQLdb

class Db(object):

    def __init__(self):

        self.username = 'resourcecounters'
        self.password = 'PASSWORD'
        self.host = '127.0.0.1'
        self.database = 'resourcecounters'
        self.connect()

    def connect(self):

        self.db = None
        self.db = MySQLdb.connect(host=self.host,user=self.username,
                                        passwd=self.password,db=self.database,
                                        connect_timeout=1)
        self.db.autocommit(True)
        return self.db

    def close(self):

        try:
            self.db.close()
        except AttributeError:
            pass

    def get_resource_id(self,type,zone,name,parent=None):

        r = None
        c = self.db.cursor()
        if parent:
            c.execute("""SELECT id FROM resources WHERE type = %(type)s
                        AND zone = %(zone)s AND value = %(value)s
                        AND parent = %(parent)s""",
                        dict(type=type,zone=zone,value=name,parent=parent))
        else:
            c.execute("""SELECT id FROM resources WHERE type = %(type)s
                        AND zone = %(zone)s AND value = %(value)s""",
                        dict(type=type,zone=zone,value=name))
        if c.rowcount == 1:
            r = c.fetchone()[0]
        elif c.rowcount > 1:
            c.close()
            raise exc.ResourceDbExc('Db.get_resource_id(): More than one '
                                    'result.', dict(type=type,zone=zone,
                                    value=name,parent=parent))
        c.close()
        return r

    def add_resource(self,type,zone,name,parent=None):
        c = self.db.cursor()
        if parent:
            c.execute("""INSERT INTO resources (type,zone,value,parent,
                        added) VALUES(%(type)s,%(zone)s,%(value)s
                        ,%(parent)s,NOW())""",
                        dict(type=type,zone=zone,value=name,parent=parent))
        else:
            c.execute("""INSERT INTO resources (type,zone,value,added)
                         VALUES(%(type)s,%(zone)s,%(value)s,NOW())""",
                         dict(type=type,zone=zone,value=name))
        c.close()

    def get_last_counter_entry(self,resource_id,type):
        r = None
        c = self.db.cursor()
        c.execute("""SELECT value,UNIX_TIMESTAMP(added) FROM counters WHERE
                    resource = %(resource)s AND type = %(type)s
                    ORDER BY added DESC LIMIT 1""", dict(
                    resource=resource_id,type=type))
        if c.rowcount == 1:
            cr = c.fetchone()
            r = {}
            r['value'] = cr[0]
            r['added'] = cr[1]
        c.close()
        return r

    def add_counter_entry(self,resource_id,type,value,delta,added,prevadded):
        c = self.db.cursor()
        c.execute("""INSERT INTO counters (resource,type,value,delta,added,
                        prev) VALUES(%(resource)s,%(type)s,%(value)s,%(delta)s,FROM_UNIXTIME(%(added)s),FROM_UNIXTIME(%(prev)s))""", dict(
                        resource=resource_id,type=type,value=value,
                        delta=delta,added=added,prev=prevadded))
        c.close()

    def __del__(self):
        self.close()
