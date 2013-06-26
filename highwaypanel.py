# -*- coding: utf-8 -*-
'''
Created on Jun 25, 2013

@author: pset
'''
import json
import requests
import unittest
import collections

from grub_jtcx import encode_lonlat, decode_lonlat, response2json, distance


class HighwayPanel(collections.namedtuple('HighwayPanel', 'name location image_url distance')):
    pass

    
class HighwayPanelService(object):
    
    def fetch(self, location):
                
        session = requests.Session()
        response = session.get('http://sis.jtcx.sh.cn/sisserver?highLight=false'\
                               '&srctype=USERPOI&eid=9070&extId=&agentId=&tempid=52&config=BESN'\
                               '&searchName=&cityCode=021&searchType=&number=100&batch=1'\
                               '&a_k=cb02363e90e02da4b5f3cc9dcc7f5cd0881012bd4ec0dbe0f2b5a87cea3602ad70431a4938633d15'\
                               '&resType=JSON&enc=utf-8&sr=0&ctx=1&a_nocache=')
    
        data = response2json(response.text)
        
        ret = list()

        for poi in data['poilist']:
#             if poi['uxml']['INTELLIGTYPE'] != u'高架':
#                 continue 

            loc = decode_lonlat(poi['x']), decode_lonlat(poi['y'])
            
                                            
            panel = HighwayPanel(name=poi['uxml']['INFORMATION'],
                                 location=loc,
                                 image_url='http://vms.jtcx.sh.cn:8089/VmsPic/vms/%s.gif' % poi['uxml']['INTELLIGID'],
                                 distance=distance(location, loc)
                                 )
            ret.append(panel)
            
        ret.sort(key=lambda p:p.distance)
            
        return ret[:10]


class TestHighwayPanelService(unittest.TestCase):

    def testFetch(self):
        service = HighwayPanelService()
        for panel in service.fetch((121.458989, 31.22085)):
            print panel.name, panel.location, panel.image_url


if __name__ == '__main__':
    unittest.main()