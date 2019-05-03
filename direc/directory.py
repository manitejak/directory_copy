import os
import shutil
import sqlite3
import glob
import time
import logging

logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler=logging.FileHandler('directorylog.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


src = 'E:\\staticmobile'
dst = 'F:\\python bin\\mobile\\mobile'


def dbconnect(a):
    '''database is to store all the creation,modification if any and
     destination timestamps of all the file and directories names in it.'''
    conn = sqlite3.connect('directory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS timestamp (id BLOB,name BLOB UNIQUE, ct BLOB,dt BLOB,mt BLOB,path BLOB)''')
    try:
        c.execute('''INSERT INTO timestamp(name,ct,dt,mt,path) VALUES(?,?,?,?,?)''',a)
    except sqlite3.IntegrityError:
        print('trying to add duplicates')
        logger.exception('trying to add duplicates error integrity error')
        pass
    conn.commit()
    conn.close()


def directory_main(sr,ds):
    """it is for creation of directory for the first time as well as
    updating directories or files in the main directory"""
    src_dr = os.listdir(sr)
    print(src_dr)
    for x in src_dr:
        logger.info(x)
        y = os.path.join(sr,x)
        z = os.path.join(ds,x)
        print(y)
        print(z)
        if os.path.isdir:
            try:
                shutil.copytree(y, z, symlinks=False, ignore=None)
            except NotADirectoryError:
                if os.path.isfile(y):
                    shutil.copy(y, ds)
            except FileExistsError:
                pass
        ct = time.ctime((os.path.getctime(y)))
        print('created dir time:', ct)
        mt = time.ctime((os.path.getmtime(y)))
        print('modified time dir:', mt)
        dt = time.ctime(os.path.getctime(dst))
        print('dest time is:', dt)
        yield x,ct,mt,dt,ds


t = list(directory_main(src, dst))
""" It adds all the yield returns in the main directory function and 
adds all those to the list and using for loop it sends to databse and log files  """
print(t)
for i in t:
    print(i)
    logger.info(i)
    dbconnect(i)


def subdirec(srce,dste):
    """It creates sub directories for the existed directories in the
    destination path and is creates the log files for the copied files and directories"""
    cd = os.getcwd()
    print(cd)
    os.chdir(srce)
    a = os.getcwd()
    print(a)
    dire = glob.glob('*/')
    print(dire)
    os.chdir(cd)
    b = os.getcwd()
    print(b)
    for x in dire:
        y = os.path.join(srce, x)
        z = os.path.join(dste, x)
        j = list(directory_main(y,z))
        for p in j:
            print(p)
            logger.info(p)
            dbconnect(p)


def subsubdirec():
    """ Creates sub sub directories in the destination path
    directories and calls the subdirecotry function """
    x=next(os.walk(src))[1]
    print(x)
    for m in x:
        p=os.path.join(src,m)
        print(p)
        q=os.path.join(dst,m)
        print(q)
        subdirec(p,q) #calls subdirectory function


if not os.path.exists(dst):
    """if directory not exixts it creates new directory path and directories"""
    os.makedirs(dst)
    print('dir created')
    directory_main(src,dst)

elif os.path.exists(dst):
    """if path exixts updates directories,subsirectories and 
    sub sub directories in the existing path by calling the below functions"""
    directory_main(src,dst)
    subdirec(src,dst)
    subsubdirec()
    print('aready dir available')
    pass
