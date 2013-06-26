# -*- coding: utf-8 -*-
'''
Created on Jun 25, 2013

@author: pset
'''

import json
import requests

import eventlet
eventlet.monkey_patch()

from grub_jtcx import response2json, decode_lonlat

def baidu_loc_fix(session, loc, name):
    response = session.get('http://api.map.baidu.com/place/v2/search',
                           params={
                               'ak':'0F8a41e08f0815c42b694978a36c0269',
                               'output': 'json',
                               'page_size': 1,
                               'page_num': 0,
                               'scope': 1,
                               'region': '上海',
                               'query': name,
                             }
                           )
    try:
        locdata = json.loads(response.text)
    except Exception:
        print 'XXX: Bad response', response.text
        return loc
    
    for r in locdata['results']:
        if 'location' in r:
            return r['location']['lng'],r['location']['lat']           
    else:
        print 'XXX: No baidu location found'    
    return loc
    
def main():
    query = 'http://sis.jtcx.sh.cn/sisserver?highLight=false' \
            '&srctype=USERPOI&eid=9070&extId=&agentId='\
            '&tempid=8&config=BESN&searchName= '\
            '&cityCode=021&cenName=&searchType='\
            '&number=10&batch=%(batch)d'\
            '&a_k=cb02363e90e02da4b5f3cc9dcc7f5cd0881012bd4ec0dbe0f2b5a87cea3602ad70431a4938633d15'\
            '&resType=JSON&enc=utf-8&sr=0&range=1000&naviflag=0&ctx=123456&a_nocache=104504017251&='
    session = requests.Session()
    
    result_pois = dict()
    
    count = 0
    
    for b in range(1, 105):
        q = query % dict(batch=b)
        print q
        response = session.get(q)
        try:
            pois = response2json(response.text)
        except Exception:
            print 'XXX: Bad response'
            continue
        
        for poi in pois['poilist']:
            
            count += 1
            
            loc = lon, lat = (decode_lonlat(poi['x']), decode_lonlat(poi['y']))
            
            baidu_loc = baidu_loc_fix(session, loc, poi['name'])
                
            try:   
                extid = int(float(poi['extid']))
            except Exception as e:
                print  poi['name'], 'XXX', poi
                continue
#                 raise
            poi_data = dict(name=poi['name'],
                            extid=extid,
                            address=poi['address'],
                            location=(lon, lat),
                            baidu_loc=baidu_loc,
                            )
#             print poi_data
            if extid in result_pois:
                print '***', poi['name'], extid
            result_pois[extid] = poi_data
    else:
        with open('all_parking_lots.json', 'wb') as fp:
            json.dump(result_pois, fp, ensure_ascii=False, indent=2)
if __name__ == '__main__':
    main()
