import requests
import json

cmd_url = {
    "retry":        "https://wes-agv-fleet.iherbscs.net/api/Bots/",
    "retry_end":    "/commands/retry-task",
    "enable":       "https://wes-agv-iherbdriver.iherbscs.net/api/Bots/",
    "enable_end":   "/enable",
    "disable":      "https://wes-agv-iherbdriver.iherbscs.net/api/Bots/",
    "disable_end":  "/disable",
    "unfault":      "https://wes-agv-portal-gateway.iherbscs.net/api/Fleet/Bots/",
    "unfault_end":  "/Unfault",
    "unpause":      "https://wes-agv-iherbdriver.iherbscs.net/api/Bots/commands/unpause-bot/",
    "unpause_end":  "",
    "task":         "https://wes-agv-fleet.iherbscs.net/api/Bots/",
    "task_end":     "/currentTasks"
}
cmd_query = {
    "field":        "https://wes-agv-portal-gateway.iherbscs.net/api/Field",
    "bot_live":     "https://wes-agv-portal-gateway.iherbscs.net/api/Fleet/liveUpdates",
    "connect":      "https://wes-agv-portal-gateway.iherbscs.net/api/bots/connected",
    "estop":        "https://wes-agv-portal-gateway.iherbscs.net/api/bots/emergencystop"
}
rq_timeout = 10
warehouse = "Elgin"

def init(sw_config):
    global cmd_url
    global cmd_query
    global rq_timeout
    global warehouse

    if sw_config != 0:
        warehouse = sw_config["warehouse"]
        cmd_url = sw_config[warehouse]["cmd"]
        cmd_query = sw_config[warehouse]["query"]
        rq_timeout = sw_config["timeout"]
    else:
        print("SW: Default - Elgin")

# Retry last cmd
def retry(bot_id):
    try:
        resp = requests.put(cmd_url["retry"] + bot_id + cmd_url["retry_end"], timeout = rq_timeout)
    except requests.exceptions.Timeout:
        return 998
    except:
        return 999
    else:
        return resp.status_code

# Enable/Reconnect a bot
def enable(bot_name):
    try:
        resp = requests.put(cmd_url["enable"] + bot_name + cmd_url["enable_end"], timeout = rq_timeout)
    except requests.exceptions.Timeout:
        return 998
    except:
        return 999
    else:
        return resp.status_code

# Disable/Disconnect a bot
def disable(bot_name):
    try:
        resp = requests.put(cmd_url["disable"] + bot_name + cmd_url["disable_end"], timeout = rq_timeout)
    except requests.exceptions.Timeout:
        return 998
    except:
        return 999
    else:
        return resp.status_code

# Unpause a bot
def unpause(bot_name):
    url = cmd_url["unpause"] + bot_name + cmd_url["unpause_end"]
    try:
        if warehouse == "Elgin":
            headers = {"accept":"*/*"}
            resp = requests.post(url, headers=headers, timeout = rq_timeout)
        elif warehouse == "Atlanta":
            headers = {"authority":"wes-agv-portal-gateway.atlanta.iherb.net","accept":"*/*",\
                        "access-control-request-method":"POST",\
                        "access-control-request-headers":"authorization,content-type",\
                        "origin":"https://wes-agv-portal.atlanta.iherb.net"}
            resp = requests.options(url, headers=headers, timeout = rq_timeout)
    except requests.exceptions.Timeout:
        return ('Server timeout', 998)
    except:
        return ('Post Error ...', 999)
    else:
        return (resp.text, resp.status_code)

# Unfault a bot
def unfault(bot_id):
    headers = {"accept":"application/json", "Content-Type":"application/json-patch+json"}
    data = '{ "botId": "' + bot_id + '"}'
    try:
        resp = requests.patch(cmd_url["unfault"] + bot_id + cmd_url["unfault_end"], headers = headers, data = data, timeout = rq_timeout)
    except requests.exceptions.Timeout:
        return ('Server timeout', 998)
    except:
        return ("Can't Unfault", 999)
    else:
        return (resp.text[12:-13], resp.status_code)

def task(bot_id):
    try:
        resp = requests.get(cmd_url["task"] + bot_id + cmd_url["task_end"], timeout = rq_timeout)
    except requests.exceptions.Timeout:
        return ('Server timeout', 998)
    except:
        return ("Can't get task",999)
    else:
        return (resp.json(), resp.status_code)

def estop_status():
    try:
        estop_rsp = requests.get(cmd_query["estop"], timeout = rq_timeout)
    except requests.exceptions.Timeout:
        return ('Server timeout', 998)
    except:
        return ("Can't get estop status",999)
    else:
        return (estop_rsp.json()["isEmergencyStopped"], estop_rsp.status_code)