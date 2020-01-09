import time, serial, math, argparse
from DynamicGraph import DynamicGraph

parser = argparse.ArgumentParser(description='A Serial Reader for Arduino!')
parser.add_argument('-t', '--temp', default=20, type=int, help="this is the temperature limit")
parser.add_argument('-l', '--light', default=500, type=int, help="this is the light limit")
parser.add_argument('-g', '--graphs', default=False, action="store_true", help="stores data to enable dynamic graphics")
args = parser.parse_args()

serialPort = 'COM7'
ser1 = serial.Serial(serialPort, 9600)

tempFileName = 'temperature_data.txt'
lightFileName = 'light_data.txt'
potenFileName = 'potentiometer_data.txt'

tempLimit = args.temp
lightLimit = args.light

if args.graphs:
    tempFile = open('../data/' + tempFileName, 'w')
    tempFile.close()
    lightFile = open('../data/' + lightFileName, 'w')
    lightFile.close()
    potenFile = open('../data/' + potenFileName, 'w')
    potenFile.close()

def main():
    while True:
        # data == DHT11Temp|ThermistorValue|PhotoresistorValue|PotentiometerValue
        data = ser1.readline().decode().strip()
        values = data.split('|');

        if values[0] == 'nan':
            # First value is missing! Skipping this iteration..
            continue

        try:
            temp = float(values[0])
            thermistorTemp = calcThermistorTemp(float(values[1]))
            averageTemp = round((temp + thermistorTemp) / 2, 2)
            photoresistorValue = float(values[2])
            potentiometerValue = int(values[3])
        except:
            # Some values are missing! Skipping this iteration..
            continue

        if args.graphs:
            tempFile = open('../data/' + tempFileName, 'a')
            lightFile = open('../data/' + lightFileName, 'a')
            potenFile = open('../data/' + potenFileName, 'a')

            tempFile.write(str(averageTemp) + '\n')
            lightFile.write(str(photoresistorValue) + '\n')
            potenFile.write(str(potentiometerValue) + '\n')

            tempFile.close()
            lightFile.close()
            potenFile.close()

        #print('Temperatura =', temp, 'Temperatura Termistore =', thermistorTemp, '\nTemperatura Media =', averageTemp)
        #print('Luce =', photoresistorValue)
        #print('Potenziometro =', potentiometerValue)

        if averageTemp > tempLimit and photoresistorValue < lightLimit:
            if potentiometerValue < 250:
                ser1.write('OFF'.encode())
                #print('FAN OFF..', end='\n\n')
            elif 250 < potentiometerValue < 500:
                ser1.write('LOW'.encode())
                #print('FAN LOW SPEED!', end='\n\n')
            elif 500 < potentiometerValue < 750:
                ser1.write('MEDIUM'.encode())
                #print('FAN MEDIUM SPEED!', end='\n\n')
            elif potentiometerValue > 750:
                ser1.write('HIGH'.encode())
                #print('FAN HIGH SPEED!', end='\n\n')
        else:
            ser1.write('OFF'.encode())
            print('TEMPERATURE OR LIGHT UNDER LIMIT, FAN IS SET TO OFF..', end='\n\n')

        time.sleep(1)

def calcThermistorTemp(thermistorValue):
    # Resistor value
    R1 = 10000;
    # Steinhart–Hart coefficients
    c1, c2, c3 = 1.009249522e-03, 2.378405444e-04, 2.019202697e-07

    # thermistorValue == Vin * (R2 / (R1 + R2))
    # R2 == R1 * (Vin / thermistorValue - 1)
    # 5V == Vin == 1023

    R2 = R1 * (1023 / thermistorValue - 1)
    logR2 = math.log(R2)

    # Steinhart–Hart equation
    T = 1 / (c1 + c2 * logR2 + c3 * logR2 * logR2 * logR2)

    # From Kelvin to Celsius degrees
    return round(float(T - 273.15), 2)

if __name__ == '__main__':
    main()
