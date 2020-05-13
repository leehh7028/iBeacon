#!/usr/bin/env python
# test BLE Scanning software
# jcs 6/8/2014
import blescan
import sys
import bluetooth._bluetooth as bluez
import pymysql
from time import sleep
import threading
import os

class DB_sending:
    def __init__(self):
        self.url = ""
        self.id = ''
        self.password = ''
        self.dbName = ''
    def creat_connet(self):
        self.db = pymysql.connect(host=self.url, port=3306, user=self.id, passwd=self.password, db=self.dbName, charset='utf8')
        self.cursor = self.db.cursor()

    def calcualte_distance_rssi(self, txPower, rssi):
        txPower_num =  int(txPower)
        rssi_num = int(rssi)
        if rssi_num is 0 :
            return -1

        ratio = rssi_num * 1.0 / txPower_num
        if ratio < 1.0 :
            return str(ratio**10)
        else:
            distance = (0.89976) * (ratio**7.7095) + 0.111
            return str(distance)

    def insert_unique_data(self, mac, uuid, major, minor):
        sql = "insert into device_unique_info_tb (macAddress, UUID, major, minor) " \
                "select '"+ mac+"' ,'"+uuid+"' ,'"+major+"' ,'"+minor+"' from dual where not exists" \
                "( select * from device_unique_info_tb where macAddress = '"+mac+"' and UUID = '"+uuid+"')"
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        print(self.cursor.lastrowid)

    def insert_valiable_data(self, mac, rssi, txpower, accuracy):
        sql = "INSERT INTO `device_variable_info_tb` (`macaddress`, `rssi`, `txpower`, `accuracy`, `time`) VALUES ('"+ mac +"', '"+ rssi +"', '"+ txpower +"', '"+ accuracy +"', CURRENT_TIMESTAMP);"
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        print(self.cursor.lastrowid)

    def run_sensor_thread(self):
        os.system("sudo python3 /home/pi/sensorDataToDB.py")


dev_id = 0
conn = DB_sending()

try:
    sock = bluez.hci_open_dev(dev_id)
    print("ble thread started")

except:
    print("error accessing bluetooth device...")
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

try:
    sensor_thread = threading.Thread(target=conn.run_sensor_thread)
    sensor_thread.start()
    print("sensor data transmission start")
except:
    print("error on sensor thread...")
    sys.exit(1)



while True:
    returnedList = blescan.parse_events(sock, 10)
    for beacon in returnedList:
        print(beacon)
        beacon_split = beacon.split(',')
        # [0]MAC [1]UUID [2]Major [3]Minor [4]RSSI [5]Tx Power
        #if beacon_split[1] == "000021ace8b4e0c27d20b611b611c774" :
        if beacon_split[2] in [40001]:
        #if beacon_split[3] in [30530]:
            conn.creat_connet()
            conn.insert_unique_data(beacon_split[0], beacon_split[1], beacon_split[2], beacon_split[3])
            conn.insert_valiable_data(beacon_split[0], beacon_split[5], beacon_split[4], conn.calcualte_distance_rssi(beacon_split[4],beacon_split[5]))
            print("send tag info")
            conn.db.close()

