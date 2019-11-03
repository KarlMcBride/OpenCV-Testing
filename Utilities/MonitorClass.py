from screeninfo import get_monitors

class MonitorClass:
    def GetMonitorCount(self):
        monitors_available = 0
        try:
            for m in get_monitors():
                print(str(m))
                monitors_available += 1
        except:
            monitors_available = 0
        print("Monitors available: {}".format(monitors_available))


# Call GetMonitorCount if called directly from command line
if __name__ == '__main__':
    monClassInstance = MonitorClass()
    monClassInstance.GetMonitorCount()
