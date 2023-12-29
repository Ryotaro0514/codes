import time
import datetime
import board
import adafruit_dht
from google.cloud import bigquery

def get_data():
   dhtDevice = adafruit_dht.DHT22(board.D22)
   while True:
      try:
          temperature_c = dhtDevice.temperature
          humidity = dhtDevice.humidity
          print("Temp: {:.1f} C    Humidity: {}% ".format(temperature_c, humidity))
          return temperature_c, humidity
      except RuntimeError as error:
          print(error.args[0])
          time.sleep(2.0)
          continue
      except Exception as error:
          dhtDevice.exit()
          raise error
      time.sleep(2.0)

def to_gbq(temperature_c, humidity):
   client = bigquery.Client()
   table_id = 'rpi-sensor-292407.SensorDataset.DHT22SensorData' #プロジェクトID.データセットID.テーブルID
   dt_now = datetime.datetime.now()
   rows_to_insert = [{'time': dt_now.strftime('%Y-%m-%d %H:%M:%S'),
            'temp': temperature_c,
            'humidity': humidity}]
   errors = client.insert_rows_json(table_id, rows_to_insert)
   if errors == []:
       print("New rows have been added.")
   else:
       print("Encountered errors while inserting rows: {}".format(errors))

def main():
   temperature_c, humidity = get_data()
   to_gbq(temperature_c, humidity)

if __name__ == '__main__':
   main()
