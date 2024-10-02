import PyNUTClient
# import logging

logName = 'myapp.log'

host = "221.111.16.123"
host = "nightblood"

# logger = logging.getLogger(__name__)
# logging.basicConfig(filename=logName, format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

history = open(logName, "r+")

oldBatteryPercentage = history.readline()

client = PyNUTClient.PyNUT.PyNUTClient(host = host)
myList = client.GetUPSNames()

for thisUPSName in myList:
    vars = client.GetUPSVars(ups = thisUPSName)
    batteryPercentage = vars[b'battery.charge'].decode('utf-8')
    # logger.info("Battery Percentage: %s", batteryPercentage)
    history.seek(0)
    history.write(batteryPercentage)
    history.truncate()
