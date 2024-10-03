import PyNUTClient, os, time, logging
from wakeonlan import send_magic_packet

logName = 'myapp.log'

logger = logging.getLogger(__name__)

host = os.getenv("UPS_IP", "127.0.0.1")
logger.debug('host is %s', host)

sleepers = os.getenv("SLEEPER_LIST", "a0:36:9f:50:a1:e1").split(",")
logger.debug('Mac Addresses to wake: %s', sleepers)

batteryThreshold = int(os.getenv("BATT_THRESHOLD", "30"))
logger.debug('Battery Threshold %s', batteryThreshold)

sleepDelay = int(os.getenv("DELAY", "120"))
logger.debug('Sleep delay: %s', sleepDelay)

logLevel = eval('logging.' + os.getenv("LOGGING_LEVEL", "DEBUG").upper())
logger.info('Log level is %s', logLevel)

host = "nightblood" # TODO Remove this line.

logging.basicConfig( 
    format = '%(asctime)s %(levelname)-8s %(message)s', 
    level = logLevel, 
    datefmt = '%Y-%m-%d %H:%M:%S'
    )

client = PyNUTClient.PyNUT.PyNUTClient(host = host)
myList = client.GetUPSNames()

def main():
    with open(logName, "r+") as history:

        oldBatteryPercentage = history.readline()
        logger.debug('Previous Battery Percentage %s', oldBatteryPercentage)

        for thisUPSName in myList:
            vars = client.GetUPSVars(ups = thisUPSName)
            batteryPercentage = vars[b'battery.charge'].decode('utf-8')
            logger.debug('This UPS (%s) has a batttery percentage of %s', thisUPSName, batteryPercentage)

        history.seek(0)
        history.write(batteryPercentage)
        history.truncate()

    if oldBatteryPercentage < batteryPercentage and batteryPercentage >= batteryThreshold:
        try:
            send_magic_packet(sleepers) # TODO this wont work if sleepers is a list
        except Exception as e:
            logger.error('An Error Occured when sending the magic packet. Error: %s', e)    
        else:
            logger.debug('The magic packet was sent without error.')

while __name__ == "__main__":
    main()
    logger.debug('Sleeping for %s seconds', sleepDelay) 
    time.sleep(sleepDelay)