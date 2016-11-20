#!/usr/bin/python
import sys
import MySQLdb
import ConfigParser

class KeyManager:
    def __init__(self, host, uname, passwd, name):
        # Open database connection
        try:
            self.dConn = MySQLdb.connect(
                host=host,
                user=uname,
                passwd=passwd,
                db=name)
        except Exception as e:
            print "Error: MySQL Server connect failed :" + e
            sys.exit(1)

    def checkKey(self, keyValue):
        # Init query
        dQuery = self.dConn.cursor()

        # Execute query
        if(dQuery.execute("SELECT keyType, keyComment FROM keyList WHERE keyValue = %s", [keyValue]) != 0):
            sAnsw = dQuery.fetchone()

            # Get key type, !: Admin, 1: One time use, @: Hour check, %: Duration
            if (sAnsw[0] == '!'):
                return True

            if (sAnsw[0] == '1'):
                dQuery.execute("DELETE FROM keyList WHERE keyValue = %s", [keyValue])
                self.dConn.commit()
                return True

            if (sAnsw[0] == '@'):
                return True

            if (sAnsw[0] == '%'):
                return True

        return False;

class SMSHandler:
    def __init__(self):
        print ""

# Loading config file
Config = ConfigParser.ConfigParser()
Config.read('config.cfg')

if __name__ == '__main__':
    keyMgr = KeyManager( # Init the keyManager
        Config.get("db", "host"),
        Config.get("db", "uname"),
        Config.get("db", "passwd"),
        Config.get("db", "name"))

    print(keyMgr.checkKey("AG4575"))
