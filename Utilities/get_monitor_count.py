from screeninfo import get_monitors

def get_monitor_count():
    monitors_available = 0
    try:
        for m in get_monitors():
            print(str(m))
            monitors_available += 1
    except:
        monitors_available = 0
    print("Monitors available: {}".format(monitors_available))


# Call get_monitor_count if called directly from command line
if __name__ == '__main__':
    get_monitor_count()