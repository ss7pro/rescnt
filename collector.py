import time

from rescnt import libvirtcnt
from rescnt import counter


class Collector(object):

    def __init__(self):
        self.zone = 'r4cz1'
        self.counter = counter.Counter()
        pass

    def run(self):
        """Run collect process and record counters in the database."""
        lv = libvirtcnt.LibVirtVMCounters()
        for domID in lv.get_domID():
            cnt = lv.get(domID)
            self.store(cnt)

    def store(self,cnt):
        """Store collected counters in the database."""
        # instance name is a parent resource
        instance_resource_id = self.counter.ensure_resource('instance', self.zone, cnt['name'])
        ct = time.time()
        if cnt['counters'].get('interface'):
            self.store_interface_counters(cnt['counters']['interface'],
                                            instance_resource_id,ct)
        if cnt['counters'].get('disk'):
            self.store_disk_counters(cnt['counters']['disk'],
                                            instance_resource_id,ct)

    def store_interface_counters(self,cnt,parent_id,ct):
        """Store interface counters in the database.

            Data is stored kilo units:
                        kreq - kilo requestes / 1000
                        kbytes - kilo bytes / 1024
        """
        for i in cnt.keys():
            rid = self.counter.ensure_resource('interface', self.zone, i, parent_id)
            self.counter.add(rid,'rx_kbytes',cnt[i][0]/1024,ct)
            self.counter.add(rid,'rx_kpackets',cnt[i][1]/1000,ct)
            self.counter.add(rid,'tx_kbytes',cnt[i][4]/1024,ct)
            self.counter.add(rid,'tx_kpackets',cnt[i][5]/1000,ct)

    def store_disk_counters(self,cnt,parent_id,ct):
        """Store disk counters in the database.

            Data is stored kilo units:
                        kreq - kilo requestes / 1000
                        kbytes - kilo bytes / 1024
        """
        for i in cnt.keys():
            rid = self.counter.ensure_resource('disk', self.zone, i, parent_id)
            self.counter.add(rid,'rd_kreq',cnt[i][0]/1000,ct)
            self.counter.add(rid,'rd_kbytes',cnt[i][1]/1024,ct)
            self.counter.add(rid,'wr_kreq',cnt[i][2]/1000,ct)
            self.counter.add(rid,'wr_kbytes',cnt[i][3]/1024,ct)
