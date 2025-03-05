import websocket
import json
from calculations import calculateEma 
from config import main15mcsv 
import csv

def dataStreamStart (symbol) :
    def on_open(ws):
        subMsg = {"method": "SUBSCRIBE","params":[f"{symbol}"+"@markPrice@1s"],"id": 1}
        ws.send(json.dumps(subMsg))
        print("Opened connection")

    def on_message(ws, message):
        data = json.loads(message)
        print(data["p"])

    url = "wss://fstream.binance.com/ws"
    ws = websocket.WebSocketApp(url,on_open=on_open,on_message=on_message)
    ws.run_forever()

def calculatingCurrentEma(timeStamp , price , signal ):
    with open(main15mcsv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        datas = []
        for row in csv_reader:
            data = {"timeStamp":int(row[0] ), "closeTime": float(row[4])}
            datas.append(data)
        csv_file.close()
    for index, data in enumerate(datas) :
        datatimestamp = timeStamp - data['timeStamp']
        if datatimestamp < 0 :
            del datas[index - 1 :]
            break
    datas.append({"timeStamp":timeStamp, "closeTime": price})
    emaDataOfDay = calculateEma(datas,5)
    emaDatas = [emaDataOfDay[-2],emaDataOfDay[-1]]
    if signal == "short" :
        emaDatas = list(map(lambda x: -1 * x, emaDatas))
    if emaDatas [-1] < emaDatas[-2] :
        protectProcess = True
    return protectProcess

def updateEma(newPrice , signal , organisedEmaValues ):
    for values in organisedEmaValues :
        result = False
        if values["timestamp"] == signal[1] :
            previousEma = values["ema5"]
            break
    multiplier = 2 / (15 + 1)
    updatedEma = (newPrice - previousEma) * multiplier + previousEma
    if signal[0] == "short" :
        updatedEma = - updatedEma
        previousEma = - previousEma
    if updatedEma < previousEma :
        result = True

    return result
