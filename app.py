from flask import Flask  , request
import csv 
import itertools
from datetime import datetime

# Date,Time,ModbusID,voltage,current,active_power,power_factor,apperant_power,active_energy


CSV_file = 'data.csv'
CURRENT_DATA = itertools.cycle(["voltage" , "current" , "active_power" , "power_factor" , "apperant_power" , "active_energy" ])
CURRENT_DATA2 = itertools.cycle(["voltage" , "current" , "active_power" , "power_factor" , "apperant_power" , "active_energy" ])
CURRENT_DATA3 = itertools.cycle(["voltage" , "current" , "active_power" , "power_factor" , "apperant_power" , "active_energy" ])
CURRENT_DATA4 = itertools.cycle(["voltage" , "current" , "active_power" , "power_factor" , "apperant_power" , "active_energy" ])
app = Flask(__name__)

temp_data_2 = []
temp_data_3 = []
temp_data_4 = []
temp_data = []

def modify_data1(data):
    parameter = next(CURRENT_DATA)
    if parameter == "voltage":
        if temp_data:
            write_to_csv(temp_data)
            temp_data.clear()
        temp_data.extend(data)
    else:
        temp_data.append(data[3])
    
    # print("Parameter : " , parameter , "==Data : " , data)
    # pass


def modify_data2(data):
    parameter = next(CURRENT_DATA2)
    if parameter == "voltage":
        if temp_data_2:
            write_to_csv(temp_data_2)
            temp_data_2.clear()
        temp_data_2.extend(data)
    else:
        temp_data_2.append(data[3])


    

def modify_data3(data):
    parameter = next(CURRENT_DATA3)
    if parameter == "voltage":
        if temp_data_3:
            write_to_csv(temp_data_3)
            temp_data_3.clear()
        temp_data_3.extend(data)
    else:
        temp_data_3.append(data[3])


def modify_data4(data):
    parameter = next(CURRENT_DATA4)
    if parameter == "voltage":
        if temp_data_4:
            write_to_csv(temp_data_4)
            temp_data_4.clear()
        temp_data_4.extend(data)
    else:
        temp_data_4.append(data[3])


def write_to_csv(data):
    print("writing to csv" , data)
    try:
        with open(CSV_file, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)
    except Exception as e:
        print("Error While Writing As : ",e)
        pass 

def read_from_csv():
    try:
        with open(CSV_file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            data = []
            for row in reader:
                data.append(row)
        return data
    except Exception as e:
        print("Error While reading As : ",e)
        return []

@app.route('/' , methods=['GET' , 'POST' ])
def getData():
    try:
        data = request.json
    except:
        try:
            data = request.form.to_dict()
        except:
            data = None

    # print(data)
    # d = [('{"TS" : "1669442071", "D": "26/11/2022 05:54:31", "ModbusID": "1","voltage": "[239.590286,238.094696,240.652374]"}', '')]
    if data is not None:
        # print("Eval Data : ",data)
        # Eval Data :  {'{"TS": "1674886509", "D": "28/01/2023 06:15:09", "ModbusID": "1","VIP": "[460587.000000]" }': ''}
        data = list(data.keys())[0]
        data = eval(data)
        # print("lastdata" , type(data))
        # data = dict(data)

        timestamp = int(data['TS'])
        dt_object = datetime.fromtimestamp(timestamp)
        date = dt_object.strftime("%d-%m-%Y")
        time = dt_object.strftime("%H:%M:%S")

        csv_data = [date, time, data['ModbusID'], data['VIP']]


        if csv_data[2] == "1":
            modify_data1(csv_data)
        elif csv_data[2] == "2":
            modify_data2(csv_data)
        elif csv_data[2] == "3":
            modify_data3(csv_data)
        elif csv_data[2] == "4":
            modify_data4(csv_data)
        else:
            print("No ID Found")
        return "OK"
    else:
        return "Data is None"



if __name__ == '__main__':
    app.run(host= "0.0.0.0" ,port=8000, debug=True)