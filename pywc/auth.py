'''
Created on Jun 17, 2013

@author: Kotaimen
'''

import hashlib

class AuthenticationError(Exception):
    pass

def server_authentication(token, args):
    try:
        signature = args['signature']
        timestamp = args['timestamp']
        nonce = args['nonce']
    except KeyError as e:
        raise AuthenticationError('Invalid request arg "%s"' % e)

    h = hashlib.sha1()
    h.update(''.join(sorted([token, timestamp, nonce])))
    digest = h.hexdigest()

    if digest != signature:
        raise AuthenticationError('Invalid server authentication')
