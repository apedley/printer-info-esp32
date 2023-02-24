def connect():
    import network
    import config
    
    ssid = config.WIFI_SSID
    password = config.WIFI_PASSWORD

    station = network.WLAN(network.STA_IF)
 
    if station.isconnected() == True:
        print("Already connected")
        return
 
    station.active(True)
    station.connect(ssid, password)
 
    while station.isconnected() == False:
        pass
 
    print("Connection successful")
    print(station.ifconfig())
    

def connect_wifi():
    led_pin.value(1)
    
    station = network.WLAN(network.STA_IF)
    if station.active() and station.isconnected():
        station.disconnect()
        time.sleep(1)
    station.active(False)
    time.sleep(1)
    station.active(True)

    station.connect('Wi Believe I Can Fi', 'intertubes')
    time.sleep(1)

    connection_timeout = 10 * 1000    # WiFi connection timeout in milliseconds
    start_ms = time.ticks_ms()
    while (time.ticks_diff(time.ticks_ms(), start_ms) <= connection_timeout):
        print('Waiting for WiFi connection...')
        if station.isconnected():
            print('Connected to WiFi')
            print(station.ifconfig())
            break
        time.sleep(1)

    result = station.isconnected()
    # force an accesspoint creation
    # result = False

    if result is False:
        # disconnect as/from station and disable WiFi for it
        station.disconnect()
        station.active(False)
        time.sleep(1)

        # create a true AccessPoint without any active Station mode
        accesspoint = network.WLAN(network.AP_IF)

        # activate accesspoint if not yet enabled
        if not accesspoint.active():
            accesspoint.active(True)

        accesspoint_name = "MicroPython AP"
        accesspoint.config(essid=accesspoint_name,
                           authmode=network.AUTH_OPEN,
                           password='',
                           channel=11)

        print('Created Accesspoint: {}'.format(accesspoint_name))

    # turn onboard LED off
    led_pin.value(0)


