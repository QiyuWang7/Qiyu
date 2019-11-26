import os
from dynamixel_sdk import *
import time

# Control table address
ADDR_AX_TORQUE_ENABLE      = 24
ADDR_AX_GOAL_POSITION      = 30
ADDR_AX_PRESENT_POSITION   = 36
ADDR_AX_MOVING_SPEED       = 32
ADDR_AX_PRESENT_LOAD       = 40
ADDR_AX_CW_ANGLE_LIMIT     = 6
ADDR_AX_CCW_ANGLE_LIMIT    = 8

# Protocol version
PROTOCOL_VERSION            = 1.0                           # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID_1                    = 1                             # Dynamixel ID : 1
DXL_ID_2                    = 2                             # Dynamixel ID : 2

DXL_IDs                     = (DXL_ID_1,DXL_ID_2)
BAUDRATE                    = 1000000                       # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'                        # Check which port is being used on your controller
                                                            # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                             # Value for enabling the torque
TORQUE_DISABLE              = 0                             # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 10                            # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 1000                          # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20                            # Dynamixel moving status threshold

angleLimit_r                = 0
angleLimit_l                = 1023
WHEEL_ENABLE                = 1
WHEEL_DISABLE               = 0
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)


def portOpen():
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        quit()
    setBaud()

def setBaud():
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        quit()

def portClose():
    portHandler.closePort()

def torqueEnable(id, value):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, id, ADDR_AX_TORQUE_ENABLE, value)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


def servoRead(id):
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, id, ADDR_AX_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    print("[ID:%03d]  PresPos:%03d" % (id, dxl_present_position))
    return dxl_present_position

def servoSpeed(id,value):
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, id, ADDR_AX_MOVING_SPEED, value)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

def wheelMode(id, boolean):
    if boolean == WHEEL_ENABLE:
        angleLimit_r = 0
        angleLimit_l = 0
    elif boolean == WHEEL_DISABLE :
        angleLimit_r = 0
        angleLimit_l = 1023

    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, id, ADDR_AX_CW_ANGLE_LIMIT,angleLimit_r)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, id, ADDR_AX_CCW_ANGLE_LIMIT,angleLimit_l)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

def servoWrite(id,value):
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, id, ADDR_AX_GOAL_POSITION, value)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

if __name__ == "__main__":
    portOpen()
    torqueEnable(DXL_IDs[0],TORQUE_ENABLE)
    wheelMode(DXL_IDs[0],WHEEL_DISABLE)
    servoSpeed(DXL_IDs[0],350)
    servoWrite(DXL_IDs[0],256)
    time.sleep(2)
    servoWrite(DXL_IDs[0],768)
    servoRead(DXL_IDs[0])

    torqueEnable(DXL_IDs[1],TORQUE_ENABLE)
    wheelMode(DXL_IDs[1],WHEEL_DISABLE)
    servoSpeed(DXL_IDs[1],100)
    servoWrite(DXL_IDs[1],256)
    time.sleep(2)
    servoWrite(DXL_IDs[1],768)
    servoRead(DXL_IDs[1])


# a = true
    #while 1:
        #if servoRead(DXL_IDs[0])>1000:
        #if time == 6:
            #servoWrite(DXL_IDs[0],1)
            #break
        #if servoRead(DXL_IDs[1])>1000:
        #if time == 6:
            #servoWrite(DXL_IDs[1],1)
            #break

    #while 1:
        #if time:
            #servoSpeed(DXL_IDs[0],0)
            #break
        #if time:
            #servoSpeed(DXL_IDs[1],0)
            #break


    #sleep (500)
