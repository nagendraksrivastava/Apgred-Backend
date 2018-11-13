# -*- coding: utf-8 -*-
import hashlib


def verify_digest(list, hashcode):
    list.reverse()
    list_as_string = ' '.join(list)
    hash_obj = hashlib.sha1(list_as_string)
    digest = hash_obj.hexdigest()
    if digest == hashcode:
        return True
    else:
        return False
