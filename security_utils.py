import hashlib


def md5(string):
    m=hashlib.md5()
    m.update(string)
    return str(m.hexdigest())
def sha1(string):
    m=hashlib.sha1()
    m.update(string)
    return str(m.hexdigest())

def sha256(string):
    m=hashlib.sha256()
    m.update(string)
    return str(m.hexdigest()) 

def sha512(string):
    m=hashlib.sha512()
    m.update(string)
    return str(m.hexdigest()) 