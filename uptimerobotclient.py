#import logging
#logging.basicConfig(level=logging.DEBUG)
import sys
from os import name
import requests
import json
import os
TOKEN = (os.getenv("UPTIMEROBOT_API_KEY") or "")
DEBUG = True
API_ENDPOINT = "https://api.uptimerobot.com/v2/"
VALID_ACTIONS = ["add_monitor", "remove_monitor", "get_monitor"]
def print_banner():
  print(sys.argv[0], ": a non-interactive cli tool for uptimerobot")
def print_usage():
  print("usage: " + sys.argv[0] + " <add_monitor|remove_monitor|get_monitor> <url>")
def validate_params(list_of_args = []):
  if (len(list_of_args) <=1) or (list_of_args[1] not in VALID_ACTIONS):
    print_usage()
    print("invalid params; exiting.")
    exit(1)
  print("invoked with action: " + list_of_args[1] + " and url: " + list_of_args[2])
def make_http_call(resource = "", additional_payload = ""):
  endpoint_url = API_ENDPOINT + resource
  payload = "api_key=" + TOKEN + "&format=json&logs=1&" + additional_payload 
  headers = {"content-type": "application/x-www-form-urlencoded", "cache-control": "no-cache"}
  print("making http POST request to endpoint: " + endpoint_url + " with payload: " + payload)
  response = requests.request("POST", endpoint_url, data=payload, headers=headers)
  print("response code: " + str(response.status_code))
  if DEBUG:
    print("response content: " + response.text)
  if response.status_code != 200:
    return None
  return response.text
def get_monitor(url = ""):
  method_name = "getMonitors"
  print("calling make_http_call with method: " + method_name)
  raw_response = make_http_call(method_name)
  if raw_response is None:
    print("call failed; as response is None. exiting.")
    exit(1)
  response = json.loads(raw_response)
  monitor_id = -1
  if len(response["monitors"]) > 0:
    for monitor in response["monitors"]:
      if monitor["url"] == url:
        monitor_id = monitor["id"]
        break
  final_response = {url: monitor_id}
  print("final_response for get_monitor: " + str(final_response))
  return final_response

def add_monitor(url ,friendly_name ): 
    method_name = "newMonitor"
    additional_payload = "type=1&url={}&friendly_name={}".format(url,friendly_name)
    print("calling make_http_call with method: " + method_name + additional_payload)
    raw_response = make_http_call(method_name,additional_payload)
    if raw_response is None:
      print("call failed; as response is None. exiting.")
      exit(1)
    response = json.loads(raw_response)
    return response

def delete_monitor(url = ""):
  method_name = "deleteMonitor"
  print("calling make_http_call with method: " + method_name)
  final_response = get_monitor(url)
  my_id = final_response[url]
  additional_payload = "id={}".format(my_id)
  raw_response = make_http_call(method_name,additional_payload)
  if raw_response is None:
    print("call failed; as response is None. exiting.")
    exit(1)
  response = json.loads(raw_response)
  pass
if __name__ == "__main__":
  print_banner()
  list_of_args = sys.argv
  validate_params(list_of_args)
  action = list_of_args[1]
  url = list_of_args[2]
  if(action == "get_monitor"):
    resp = get_monitor(url)
    if ( resp[url] == -1):
      print("monitor not found!")
    else:
      print("monitor found: " + str(resp[url]))
  elif(action == "add_monitor"):
    friendly_name = list_of_args[3]
    print(add_monitor(url,friendly_name))
  else:
    print(delete_monitor(url))

