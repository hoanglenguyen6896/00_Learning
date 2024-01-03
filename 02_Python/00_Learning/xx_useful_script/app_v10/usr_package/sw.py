import requests
import json
import time

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
    "task_end":     "/currentTasks",
    "start_charge": "https://wes-agv-portal-gateway.iherbscs.net/api/Fleet/Bots/",
    "start_ch_end": "/SendBotToCharger",
    "stop_charge":  "https://wes-agv-portal-gateway.iherbscs.net/api/fleet/bots/",
    "stop_ch_end":  "/stopCharging"

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
    headers = {"accept":"*/*"}
    try:
        resp = requests.post(url, headers=headers, timeout = rq_timeout)
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

def send_bot_to_charger(bot_id):
    """
    https://wes-agv-portal-gateway.atlanta.iherb.net/api/Fleet/Bots/7feee09f-38ef-4ae6-82b3-017de24ea07f/SendBotToCharger
    https://wes-agv-portal-gateway.iherbscs.net/api/Fleet/Bots/b6186267-d217-4d48-9099-017ce15cf413/SendBotToCharger
    """
    cmd = cmd_url["start_charge"] + bot_id + cmd_url["start_ch_end"]
    try:
        resp = requests.put(cmd, timeout = rq_timeout)
    except requests.exceptions.Timeout:
        return 998
    except:
        return 999
    else:
        return resp.status_code

def stop_bot_charging(bot_id):
    """
    https://wes-agv-portal-gateway.atlanta.iherb.net/api/fleet/bots/aba101ac-31df-4866-bf28-017ca8e3182f/stopCharging
    https://wes-agv-portal-gateway.iherbscs.net/api/fleet/bots/38f79498-7285-411b-ae97-017d25074096/stopCharging
    """
    cmd = cmd_url["stop_charge"] + bot_id + cmd_url["stop_ch_end"]
    headers = {"accept":"*/*"}
    try:
        resp = requests.post(cmd, headers=headers, timeout = rq_timeout)
    except requests.exceptions.Timeout:
        return ('Server timeout', 998)
    except:
        return ('Post Error ...', 999)
    else:
        return (resp.text, resp.status_code)

POWER_SAVER_BIT_SLEEP = "1B"
POWER_SAVER_BIT_WAKE = "1F"

def power_debug(bot_ip, opt):
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    data = '{"enable":"' + opt + '"}'
    try:
        resp = requests.put("http://" + bot_ip + ":8081/v1/debugMode", headers=headers, data=data, timeout=rq_timeout)
        # print(bot_ip + "--")
    except requests.exceptions.Timeout:
        return ('Server timeout', 998)
    except Exception as e:
        print(e)
        return ('Put Error ...', 999)
    else:
        return(resp.text, resp.status_code)

def power_bit_set(bot_ip, bit_stt):
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    data = '{"bits":"' + bit_stt + '"}'
    try:
        resp = requests.put("http://" + bot_ip + ":8081/v1/sup/powerstatus", headers=headers, data=data, timeout=rq_timeout)
    except requests.exceptions.Timeout:
        return ('Server timeout', 998)
    except Exception as e:
        print(e)
        return ('Put Error ...', 999)
    else:
        return(resp.text, resp.status_code)

def reset_motion(bot_ip):
    url = "http://172.17.35.111:8081/v1/motion/reset"
    headers = {"Content-Length":"0"}
    try:
        resp = requests.post("http://" + bot_ip + ":8081/v1/motion/reset", headers=headers, timeout=rq_timeout)
    except requests.exceptions.Timeout:
        return ('Server timeout', 998)
    except Exception as e:
        print(e)
        return ('Post Error ...', 999)
    else:
        return(resp.text, resp.status_code)

    print(resp.status_code)

def enter_sleep_mode(bot_ip):
    txt , vl = power_debug(bot_ip, "true")
    txt2, vl2 = power_bit_set(bot_ip, POWER_SAVER_BIT_SLEEP)
    return(txt, txt2)

def exit_sleep_mode(bot_ip):
    txt , vl = power_debug(bot_ip, "true")
    txt2, vl2 = power_bit_set(bot_ip, POWER_SAVER_BIT_WAKE)
    txt3, vl3 = reset_motion(bot_ip)
    txt4 , vl4 = power_debug(bot_ip, "false")
    return(txt, txt2, txt3, txt4)

if __name__ == '__main__':
    # import threading
    # ip_list = ["172.16.28.115", "172.16.28.75", "172.16.28.25"]
    # for bot_ip in ip_list:
    #     print(bot_ip)
    #     t = threading.Thread(target = exit_sleep_mode, args = (bot_ip,))
    #     t.start()
        # enter_sleep_mode(bot_ip)
    pass