########################################################
#  Databse interface class
#  10/12/16  John Lamb
########################################################

import base64
import MySQLdb

class Mysql(object):
    __instance = None
    
    __host = None
    __user = None
    __password = None
    __database = None
    __dict = None
    
    __cursor = None
    __connection = None
    
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Mysql, cls).__new__(cls, *args, **kwargs)
        return cls.__instance
    
    def __init__(self, host = 'localhost', user='appuser', password='', database='', dict = False):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        self.__dict = dict
        
    def _open(self):
        try:
            conn = MySQLdb.connect(host=self.__host, user=self.__user, passwd=self.__password, db=self.__database)
            
            self.__connection = conn
            if self.__dict:
                self.__cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            else:
                self.__cursor = conn.cursor()
        except MySQLdb.Error as err:
            if err.errno == errorcode.ER_DBACCESS_DENIED_ERROR:
                print 'Oops, looks like there''s a problem with your username or password'
            elif err.errno == errorcode.ER_NO_DB_ERROR:
                print 'Oops, this is not the database you are looking for'
            else:
                print err
    
    def _close(self):
        self.__cursor.close()
        self.__connection.close()
    
    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %S " % table
        if kwargs:
            keys = kwargs.keys()
            values = kwargs.values()
            query += "(" + ",".join(["'%s'"]*len(keys)) % tuple(keys) + ") VALUES (" + ",".join(["%s"]*len(values)) + ")"
        elif args:
            values = args
            query += " VALUES (" + ",".join(["%s"]*len(values)) + ")"
            
        if not self.__cursor:
            self._open()
        
        self.__cursor.execute(query, values)
        self.__connection.commit()
        self._close()
        return self.__session.lastrowid
    
    def select(self, table, where=None, *args):
        result = None
        query = "SELECT "
        keys = args
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += ""+key+""
            if i < l:
                query += ','
        query += " FROM %s" % table
        if where:
            query += " WHERE %s" %where
        print query
        if not self.__cursor:
            self._open()
        self.__cursor.execute(query)
        #self.__connection.commit()
        #for row in self.__cursor.fetchall():
        #    print row
        result = self.__cursor.fetchall()
        self._close()
        return result
    
    def update(self, table, index, **kwargs):
        query = "UPDATE %s SET" %table
        keys = kwargs.keys()
        values = kwargs.values()
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "'"+key+"'%s"
            if i < l:
                query += ","
        query += " WHERE index =%d" %index
        if not self.__cursor:
            self.open()
        self.__cursor.execute(query, values)
        self.__connection.commit()
        self._close()
        
    def delete(self, table, index):
        query = "DELETE FROM %s WHERE uuid=%d" % (table, index)
        if not self.__cursor:
            self.open()
        self.__cursor.execute(query)
        self.__connection.commit()
        self._close()
    
    def call_store_procedure(self, name, *args):
        result_sp = None
        if not self.__cursor:
            self.open()
        self.__cursor.callproc(name, args)
        self.__connection.commit()
        for result in self.__session.stored_results():
            result_sp = result.fetchall()
        self._close()
        return result_sp
        