import PyNUTClient
from pprint import pprint

client = PyNUTClient.PyNUT.PyNUTClient(host = "221.111.16.123")
myList = client.GetUPSNames()

for myName in myList:
    vars = client.GetUPSVars(ups = myName)
    pprint(vars)