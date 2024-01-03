import re

text = "Oct 18 13:19:14 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:19:14.964     wifi_main_dump_status_payload:303    [ASYN] lastCmdInst:94\
Oct 18 13:19:14 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:19:14.964     wifi_main_dump_status_payload:311    [ASYN] curCmdInst: 0 curCmd: 0\
Oct 18 13:19:21 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:19:21.147           ManagerFSMExecute:922          [ASYN] Currently in state: MGR_IDLE for over 2823 seconds\
Oct 18 13:19:45 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:19:45.421     wifi_main_dump_status_payload:299    [ASYN] (104-58) West Status:Idle Charge:77 plate:Down pod:0 podDir: Invalid\
Oct 18 13:19:45 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:19:45.421     wifi_main_dump_status_payload:303    [ASYN] lastCmdInst:94\
Oct 18 13:19:45 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:19:45.422     wifi_main_dump_status_payload:311    [ASYN] curCmdInst: 0 curCmd: 0\
Oct 18 13:19:51 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:19:51.200           ManagerFSMExecute:922          [ASYN] Currently in state: MGR_IDLE for over 2853 seconds\
Oct 18 13:20:15 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:20:15.868     wifi_main_dump_status_payload:299    [ASYN] (104-58) West Status:Idle Charge:77 plate:Down pod:0 podDir: Invalid\
Oct 18 13:20:15 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:20:15.868     wifi_main_dump_status_payload:303    [ASYN] lastCmdInst:94\
Oct 18 13:20:15 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:20:15.869     wifi_main_dump_status_payload:311    [ASYN] curCmdInst: 0 curCmd: 0\
Oct 18 13:20:21 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:20:21.400           ManagerFSMExecute:922          [ASYN] Currently in state: MGR_IDLE for over 2883 seconds\
Oct 18 13:20:46 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:20:46.276     wifi_main_dump_status_payload:299    [ASYN] (104-58) West Status:Idle Charge:77 plate:Down pod:0 podDir: Invalid\
Oct 18 13:20:46 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:20:46.276     wifi_main_dump_status_payload:303    [ASYN] lastCmdInst:94\
Oct 18 13:20:46 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:20:46.276     wifi_main_dump_status_payload:311    [ASYN] curCmdInst: 0 curCmd: 0\
Oct 18 13:20:51 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:20:51.588           ManagerFSMExecute:922          [ASYN] Currently in state: MGR_IDLE for over 2913 seconds\
Oct 18 13:21:00 iHerbBot-C0EE4066E6E8 user.warn agv_exec:   BOT_206 13:21:00.677              log_reader:422              [   0]            25149935:         mot: lost heartbeat ACK\
Oct 18 13:21:16 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:21:16.722     wifi_main_dump_status_payload:299    [ASYN] (104-58) West Status:Idle Charge:77 plate:Down pod:0 podDir: Invalid\
Oct 18 13:21:16 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:21:16.722     wifi_main_dump_status_payload:303    [ASYN] lastCmdInst:94\
Oct 18 13:21:16 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:21:16.722     wifi_main_dump_status_payload:311    [ASYN] curCmdInst: 0 curCmd: 0\
Oct 18 13:21:21 iHerbBot-C0EE4066E6E8 user.info agv_exec:   BOT_206 13:21:21.788           ManagerFSMExecute:922          [ASYN] Currently in state: MGR_IDLE for over 2944 seconds"

pattern = r'\) '

result = re.finditer(pattern, text)
a = list(result)
ori = a[-1].span(0)[1]
print(a[-1].span(0)[1])
print(type(ori))
print(text[ori:ori+5:])
# print(list(result))


# cmd_list = (
#     "RST", "KILL", "PWR", "WTCL", "P71", "LOG", "FWT",
#     "GFWN", "GPWRAB", "GBORDIR",
#     "BUF", "BUFI", "BRLC", "BRLCI", "BF", "BFI", "BUP", "BUPI",
#     "BE", "BEI", "BD", "BDI", "BIG", "BUIG", "BINF",
#     "GBDAB", "GBEAB", "GBUPAP", "GBRLCI", "GBUFAF", "GBFAF",
#     "R180CW"
# )

# cmd = "rst"

# if cmd.upper() in cmd_list:
#     print("1111p")