from screeninfo import get_monitors

def GetMonitorCount():
    monitors_available = 0
    try:
        for m in get_monitors():
            print(str(m))
            monitors_available += 1
    except:
        monitors_available = 0
    return monitors_available


# Call GetMonitorCount if called directly from command line
if __name__ == '__main__':
    print("Monitors available: {}".format(GetMonitorCount()))
