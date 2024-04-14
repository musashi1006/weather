import requests
import datetime
from urllib.parse import urljoin
import argparse

parser = argparse.ArgumentParser('Weather app')
parser.add_argument('-p', '--point', help='observation point number', type=int, default=63331)
args = parser.parse_args()

#print(args.point)

# URL for latest time data
url_latest_time = "https://www.jma.go.jp/bosai/amedas/data/latest_time.txt"

# Function to extract time from the latest time data
def get_target_time(url):
    response = requests.get(url)
    latest_time = response.text.strip()  # Remove leading/trailing whitespace

    # Extract date and time components
    date_parts = latest_time.split("T")
    date_str, time_str = date_parts[0], date_parts[1]
    #print(f"time_str:{time_str}")
    # "+"で分割
    parts = time_str.split("+")
    # 最初の要素のみを結合
    time_str = "".join(parts[:1])
    year, month, day = map(int, date_str.split("-"))
    hour, minute, second = map(int, time_str.split(":"))
    hour = hour // 3 * 3

    # Calculate target time (3 hours before)
    target_time = datetime.datetime(year, month, day, hour, minute, second)

    return target_time.strftime("%Y%m%d_%H")  # Format as YYYYMMDD_HH

# Specify the desired AMEDAS station ID (replace with your desired ID)
station_id = args.point #"63331"
print(f"station_id:{station_id}")

# Construct the URL for the target time data
target_datetime = get_target_time(url_latest_time)
#print(f"target_datetime:{target_datetime}")
url_target_data = urljoin("https://www.jma.go.jp/bosai/amedas/data/point/", f"{station_id}/{target_datetime}.json")

# Fetch the target time data
response = requests.get(url_target_data)
data = response.json()

# Calculate average temperature (assuming 'temp' key holds temperature data)
if data:
    #for item in data.values():
     #   print(item["temp"][0])
    temperatures = [item["temp"][0] for item in data.values()]  # Extract temperatures from each data point
    average_temp = sum(temperatures) / len(temperatures)
    print(f"Average temperature (past 3 hours): {average_temp:.2f}")  # Print with 2 decimal places
else:
    print("No data found for the specified time.")

from urllib.parse import urlencode
from urllib.request import urlopen, Request

url = "https://notify-api.line.me/api/notify"

headers = {
        'Authorization':' Bearer シークレットコード'
}

request = Request(url, headers=headers)

data = {
        'message':f'観測地点[西脇]直近の平均気温{average_temp:.2f}',
}

data = urlencode(data).encode("utf-8")

response = urlopen(request, data)

