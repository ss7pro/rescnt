import libvirt
from xml.etree import ElementTree


class LibVirtVMCounters(object):

    def __init__(self):
        self.conn = libvirt.open('qemu:///system')
        self.domIDs = None

    def get_domID(self):
        if not self.domIDs:
            self.domIDs = iter(self.conn.listDomainsID())
        return self.domIDs

    def get(self,domID):
        dom = self.conn.lookupByID(domID)
        r = {}
        r['name'] = dom.name()
        c = self._get(dom)
        r['counters'] = c
        return r

    def _get(self,dom):
        tree=ElementTree.fromstring(dom.XMLDesc(0))
        try:
            disk = self.getDiskCounters(dom,tree)
            interface = self.getInterfaceCounters(dom,tree)
        except:
            raise
        r = {}
        r['disk'] = disk
        r['interface'] = interface
        return r

    def getDiskCounters(self,dom,tree):

        r = {}
        for target in tree.findall('devices/disk/target'):
            dev = target.get('dev')
            r[dev] = dom.blockStats(dev)
        return r

    def getInterfaceCounters(self,dom,tree):

        r = {}
        for target in tree.findall('devices/interface/target'):
            dev = target.get('dev')
            r[dev] = dom.interfaceStats(dev)
        return r

    def __del__(self):
        try:
            self.conn.close()
        except AttributeError:
            pass
