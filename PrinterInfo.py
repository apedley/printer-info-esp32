import urequests

# quickStatsURL = "http://10.0.0.6:7125/printer/objects/query?webhooks=state&virtual_sdcard=progress,is_active&print_stats=filename,print_duration,state&heater_bed=temperature,target&extruder=temperature,target"
quickStatsURL = "http://10.0.0.6:7125/printer/objects/query?webhooks=state&display_status=progress&virtual_sdcard=progress,is_active&print_stats=filename,print_duration,state&heater_bed=temperature,target&extruder=temperature,target"

def get_stats():
    response = urequests.get(quickStatsURL)
#     print(response.status_code)
#     print(response.reason)
    parsed = response.json()
    response.close()
#     state = parsed['result']['status']['print_stats']['state']
#     filename = parsed['result']['status']['print_stats']['filename']
#     print_duration = parsed['result']['status']['print_stats']['print_duration']
#     progress = parsed['result']['status']['virtual_sdcard']['progress']
# 
#     bed = parsed['result']['status']['heater_bed']
#     extruder = parsed['result']['status']['extruder']

    duration = parsed['result']['status']['print_stats']['print_duration']
#     progress = parsed['result']['status']['virtual_sdcard']['progress']
    progress = parsed['result']['status']['display_status']['progress']
#     print(parsed)
    if (progress == 0):
        totalTime = 0
    else:
        totalTime = duration / progress
    eta = totalTime - duration
    
    stats = {
        "state": parsed['result']['status']['print_stats']['state'],
        "filename": parsed['result']['status']['print_stats']['filename'],
        "print_duration": round(duration, 2),
        "progress": round(progress, 2),
        "totalTime": totalTime,
        "eta": eta,
        "bed": parsed['result']['status']['heater_bed'],
        "extruder": parsed['result']['status']['extruder']
    }
    return stats
