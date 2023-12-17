import requests

url = "https://notify-api.line.me/api/notify" 
token = "48Mb58nlDzAqMoAjoxNnMlAgJVNZVIn11JOhd7T86ZN"
headers = {"Authorization" : "Bearer "+ token} 
message =  "テスト" 
payload = {"message" :  message} 
r = requests.post(url, headers = headers, params=payload)