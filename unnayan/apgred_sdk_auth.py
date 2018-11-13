# -*- coding: utf-8 -*-
import hashlib


def verify_digest(list, hashcode):
    list.reverse()
    hash_obj = hashlib.sha1(list)
    digest = hash_obj.hexdigest()
    if digest == hashcode:
        return True
    else:
        return False
