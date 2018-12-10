#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import websocket
import time
import json
import pymysql.cursors
from datetime import datetime
from pandas.io.json import json_normalize

connection = pymysql.connect(host='localhost',
                             user='USER',
                             password='PASSWORD',
                             db='polo',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")
    connection.close()

def on_open(ws):
    print("ONOPEN")
    ws.send(json.dumps({'command':'subscribe','channel':'BTC_ETH'}))

def on_message(ws, message):
    d1 = time.time()
    d2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    message = json.loads(message)
    print(message)
    if message[2]:
        seq = int(message[1])
        for k in message[2]:
            print(k)
            #dat = message[2][i]
            #print(dat)
            #print(dat[1])
            if len(k) == 4:
                try:
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO `zerozerozero` (`typeOT`, `typeSB`, `rate`, `amount`,`seq`, `timeDateOTe`, `timeDateOTh`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, (k[0], k[1], k[2], k[3], seq, d1, d2))
                        connection.commit()
                        cursor.close()
                finally:
                    pass

            elif len(k) == 6:
                try:
                    with connection.cursor() as cursor:
                        sql1 = "INSERT INTO `zerozerozero` (`typeOT`, `tradeID`, `typeSB`, `rate`, `amount`, `timeDateT`,`seq`, `timeDateOTe`, `timeDateOTh`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        d3 = int(k[5])
                        cursor.execute(sql1, (k[0], k[1], k[2], k[3], k[4], d3, seq, d1, d2))
                        connection.commit()
                        cursor.close()
                finally:
                    pass
            else:
                
websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
ws.on_open = on_open
ws.run_forever()
