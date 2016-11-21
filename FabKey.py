#!/usr/bin/python
import os, sys
import serial
import MySQLdb
import ConfigParser
from datetime import datetime

if not os.geteuid() == 0: # Check if is started as root
    sys.exit('Must be run as root.')

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
            sys.exit("Error: MySQL Server connect failed : " + str(e))

    def isValid(self, keyValue):
        # Init query
        dQuery = self.dConn.cursor()

        # Execute query
        if(dQuery.execute("SELECT keyType, keyOwner FROM keyList WHERE keyValue = %s", [keyValue]) != 0):
            sAnsw = dQuery.fetchone()

            if (not self.isExpired(keyValue)):
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
                        print("Warning: Key '" + keyValue + "' has no keyType parameter, expected parameter.")
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

                    if (startTime < nowTime and endTime > nowTime): # If in time range
                        return True
                    else:
                        return False
            else:
                return False
        else:
            print("Warning: No key found for '" + keyValue + "'.")
            return True

    def isExpired(self, keyValue):
        # Init query
        dQuery = self.dConn.cursor()

        # Execute query
        if(dQuery.execute("SELECT keyExpiry FROM keyList WHERE keyValue = %s", [keyValue]) != 0):
            keyExpiry = dQuery.fetchone()[0]
            if (keyExpiry != "*"): # If key is expirable
                nowDate = datetime.now().date()
                try:
                    expiryDate = datetime.strptime(
                        keyExpiry, "%d-%m-%y").date()
                except Exception:
                    print("Error: Key expiry date for '"
                        + keyValue + "' is invalid, please use * for unexpirable or date like this: DD-MM-YY.")
                    return True

                if (expiryDate > nowDate): # If not expired
                    return False
                else: # If expired
                    dQuery.execute("DELETE FROM keyList WHERE keyValue = %s", [keyValue])
                    self.dConn.commit()
                    print("Warning: Expired key '" + keyValue + "', removed from database.")
                    return True
            else: # If key is unexpirable
                return False
        else:
            print("Warning: No key found for '" + keyValue + "'.")
            return True

class SMSHandler:
    def __init__(self, serialPort):
        # Preconfigure serial
        self.serIO = serial.Serial()
        self.serIO.baudrate = 19200
        self.serIO.port = serialPort

        # Connect to serial port
        try:
            self.serIO.open()
        except Exception as e:
            sys.exit("Error: Failed to open serial port '" + serialPort + "' : " + str(e))

# Loading config file
Config = ConfigParser.ConfigParser()
Config.read('config.cfg')

if __name__ == '__main__':
    keyMgr = KeyManager( # Init the keyManager
        Config.get("db", "host"),
        Config.get("db", "uname"),
        Config.get("db", "passwd"),
        Config.get("db", "name"))

    smsHandler = SMSHandler("/dev/tty1")
