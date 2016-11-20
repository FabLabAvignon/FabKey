#!/usr/bin/python
import sys
import MySQLdb
import ConfigParser
from datetime import datetime

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
            print("Error: MySQL Server connect failed : " + str(e))
            sys.exit(1)

    def checkKey(self, keyValue):
        # Init query
        dQuery = self.dConn.cursor()

        # Execute query
        if(dQuery.execute("SELECT keyType, keyOwner, keyExpiry FROM keyList WHERE keyValue = %s", [keyValue]) != 0):
            sAnsw = dQuery.fetchone()

            # Check if key is expired
            keyExpiry = sAnsw[2]

            if (keyExpiry != "*"): # If key is expirable
                nowDate = datetime.now().date()
                try:
                    expiryDate = datetime.strptime(
                        keyExpiry, "%d-%m-%y").date()
                except Exception:
                    print("Error: Key expiry date for '"
                        + keyValue + "' is invalid, please use * for unexpirable or date like this: DD-MM-YY.")
                    return False

                if (expiryDate > nowDate): # If not expired
                    return self._validateKey(keyValue, sAnsw, dQuery)
                else: # If expired
                    dQuery.execute("DELETE FROM keyList WHERE keyValue = %s", [keyValue])
                    self.dConn.commit()
                    print("Warning: Expired key '" + keyValue + "', removed from database.")
                    return False
            else: # If key is unexpirable
                return self._validateKey(keyValue, sAnsw, dQuery)

        else:
            print("Warning: No key found for '" + keyValue + "'.")
            return False

    def _validateKey(self, keyValue, sAnsw, dQuery):
        keyType = sAnsw[0].split(":", 1)[0]

        # Get key type, !: Admin, 1: One time use, @: Hour check
        if (keyType == '!'):
            return True

        if (keyType == '1'):
            dQuery.execute("DELETE FROM keyList WHERE keyValue = %s", [keyValue])
            self.dConn.commit()
            return True

        if (keyType == '@'):
            try:
                keyParam = sAnsw[0].split(":", 1)[1]
            except Exception:
                print("Warning: Key '" + keyValue + "' has no parameter, expected parameter.")
                return False

            nowTime = datetime.now().time()

            try:
                startTime = datetime.strptime(
                    keyParam.split("|", 1)[0], "%H-%M").time()
                endTime = datetime.strptime(
                    keyParam.split("|", 1)[1], "%H-%M").time()
            except Exception as e:
                print("Warning: Key '" + keyValue + "' has configuration problem : " + str(e))
                return False

            if (startTime < nowTime and endTime > nowTime):
                return True
            else:
                return False

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

    print(keyMgr.checkKey("TC0989"))
