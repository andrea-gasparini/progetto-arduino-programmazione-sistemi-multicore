from DynamicGraph import DynamicGraph
import time

tempFileName = 'temperature_data.txt'
lightFileName = 'light_data.txt'
potenFileName = 'potentiometer_data.txt'

tempGraph = DynamicGraph('Average Temperature', 'Celsius Temperature')
lightGraph = DynamicGraph('Dark Level', 'Photoresistor value')
potenGraph = DynamicGraph('Potentiometer Value', 'Potentiometer Value')

while True:
    tempFile = open('../data/' + tempFileName, 'r')
    lightFile = open('../data/' + lightFileName, 'r')
    potenFile = open('../data/' + potenFileName, 'r')

    try:
        tempGraph.addValue(float(tempFile.read().splitlines()[-1]))
        lightGraph.addValue(float(lightFile.read().splitlines()[-1]))
        potenGraph.addValue(float(potenFile.read().splitlines()[-1]))
    except IndexError:
        continue

    tempFile.close()
    lightFile.close()
    potenFile.close()

    time.sleep(1)
