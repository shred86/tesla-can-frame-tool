"""
tesla-can-frame-tool by shred86

CAN frame deciphering was based on Jason Hugh's
Tesla Model S CAN Bus Deciphering guide.

amund7's Scan My Tesla & apach3guy's CAN3 for helping guide me.

Raw CAN frame examples from TM-Spy:

382F96248218500A0180007
302D0E61A00019EE000
"""
# Constants
KWH = ' kWh'
MILES = ' miles'
PCT = ' %'
VOLTS = ' volts'
AMPS = ' amps'

# Get full CAN frame from user
canFrameInput = input('Enter the full CAN frame: ')

# Remove first 3-digits (CAN ID)
canID = canFrameInput[0:3]

# Check if CAN frame is from TM-Spy recording
if len(canFrameInput) == 23:
    canFrame = canFrameInput[3:19]
# Check if CAN frame is from Trace log
elif len(canFrameInput) == 19:
    canFrame = canFrameInput[3:]
else:
    print("Error: CAN frame length is invalid")
    exit()

print("\nCAN ID: " + canID)
print("CAN Frame: " + canFrame + "\n")

# Convert each byte from hex to decimal
b0 = int(canFrame[0:2], 16)
b1 = int(canFrame[2:4], 16)
b2 = int(canFrame[4:6], 16)
b3 = int(canFrame[6:8], 16)
b4 = int(canFrame[8:10], 16)
b5 = int(canFrame[10:12], 16)
b6 = int(canFrame[12:14], 16)
b7 = int(canFrame[14:16], 16)


# Convert 0x382 data to human readable format
def nominalFullPackEnergy():
    return (b0 + ((b1 & 0x03) << 8)) * 0.1


def nominalEnergyRemaining():
    return ((b1 >> 2) + ((b2 & 0x0F) * 64)) * 0.1


def expectedEnergyRemaining():
    return ((b2 >> 4) + ((b3 & 0x3F) * 16)) * 0.1


def idealEnergyRemaining():
    return ((b3 >> 6) + ((b4 & 0xFF) * 4)) * 0.1


def energyToChargeComplete():
    return (b5 + ((b6 & 0x03) << 8)) * 0.1


def energyBuffer():
    return ((b6 >> 2) + ((b7 & 0x03) * 64)) * 0.1


# Not reported by BMS obviously, but it should match the car display
def socDisplayed():
    return (nominalEnergyRemaining() - energyBuffer()) / (nominalFullPackEnergy() - energyBuffer()) * 100


# Not reported on CAN bus, just calculated - should match socUI
def socNominal():
    return (nominalEnergyRemaining() / nominalFullPackEnergy()) * 100


# Convert 0x338 data to human readable format
def ratedRange():
    return b0 + (b1 << 8)


def typicalRange():
    return b2 + (b3 << 8)


# Convert 0x302 data to human readable format
def socMin():
    return (b0 + ((b1 & 0x3) << 8)) / 10.0


def socUI():
    return ((b1 >> 2) + ((b2 & 0xF) << 6)) / 10.0


# Convert 0x232 data to human readable format
def odometer():
    return (b0 + (b1 << 8) + (b2 << 16) + (b3 << 24)) / 1000


# Convert 0x102 data to human readable format
def battVoltage():
    return (b0 | b1 << 8) / 100.0


def battCurrent():
    return (((b2 + ((b3 & 0x3F) << 8)) - ((b3 & 0x40) << 8)) - 10000) / 10.0


# Print results based on canID
if canID == '382':
    print("Nominal Full Pack Energy: " + str(nominalFullPackEnergy()) + KWH)
    print("Nominal Energy Remaining: " + str(nominalEnergyRemaining()) + KWH)
    print("Expected Energy Remaining: " + str(expectedEnergyRemaining()) + KWH)
    print("Ideal Energy Remaining: " + str(idealEnergyRemaining()) + KWH)
    print("Energy to Charge Complete: " + str(energyToChargeComplete()) + KWH)
    print("Energy Buffer: " + str(energyBuffer()) + KWH)
    print("*Displayed SOC: " + str(socDisplayed()) + PCT)
    print("*Nominal SOC: " + str(socNominal()) + PCT)
    print("*Calculated values (not reported on CAN bus).\n")
elif canID == '338':
    print("Rated range: " + str(ratedRange()) + MILES)
    print("Typical range: " + str(typicalRange()) + MILES + "\n")
elif canID == '302':
    print("SOC Min: " + str(socMin()) + PCT)
    print("SOC UI: " + str(socUI()) + PCT + "\n")
elif canID == '232':
    print("Odometer: " + str(odometer()))
elif canID == '102':
    print("Battery Voltage: " + str(battVoltage()) + VOLTS)
    print("Battery Current: " + str(battCurrent()) + AMPS)
else:
    print("CAN ID not yet supported" + "\n")
