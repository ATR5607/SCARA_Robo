from dynamixel_sdk import *
import math

ADDR_PRO_TORQUE_ENABLE      = 64               # Control table address is different in Dynamixel model
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132

PROTOCOL_VERSION            = 2.0

DXL_ID                      = 1   
DXL2_ID                      = 2              # Dynamixel ID : 1
BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
DEVICENAME                  = "COM6"    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 2048   
DXL2_MINIMUM_POSITION_VALUE  = 2048        # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 0            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL2_MAXIMUM_POSITION_VALUE  = 0      
DXL_MOVING_STATUS_THRESHOLD = 100                # Dynamixel moving status threshold

                                              # IK Example - Two link Manipulater 

L1 = 92.5 
L2 = 92.5


response = 1

index = 0
while(response != 0):
     while 1:
          ivKX  = float(input("Pick a X point: "))
          ivKY = float(input("Pick a Y point: "))
          root = -1
          r = ((math.pow(ivKX,2) + math.pow(ivKY, 2) - math.pow(L1,2) - math.pow(L2,2))) / (2 * L1 * L2) 
          print(r)
          Theta2 = (math.atan2(root * math.sqrt(1 - math.pow(r,2)), r)) 
          print(Theta2 * (180 / math.pi))
          print(math.atan2(1,0))
          Theta1 = (math.atan2(ivKY,ivKX) - math.atan2(L2* math.sin(Theta2),L1+ L2 * math.cos(Theta2)))
          print(Theta1 * (180 / math.pi))

          #test = int(input("Pick a end point: "))
          #test2 = int(input("Pick a end point for id2: "))
          DXL_MINIMUM_POSITION_VALUE = 2048
          #DXL_MAXIMUM_POSITION_VALUE = int((4096/360)*test+ 2048) 
          DXL_MAXIMUM_POSITION_VALUE = int((4096/6.28) * Theta1 + 2048)
          DXL2_MINIMUM_POSITION_VALUE = 2048
          #DXL2_MAXIMUM_POSITION_VALUE = int((4096/360)*test2 + 2048)
          DXL2_MAXIMUM_POSITION_VALUE = int((4096/6.28) * Theta2 + 2048)
          finalPos = (DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE)
          finalPos2 = (DXL2_MINIMUM_POSITION_VALUE, DXL2_MAXIMUM_POSITION_VALUE)
          print("Feast your eyes on this!", finalPos[0])
         # print(test, test2)
          portHandler  = PortHandler(DEVICENAME)

          packetHandler = PacketHandler(PROTOCOL_VERSION)

          portHandler.openPort()
          portHandler.setBaudRate(BAUDRATE)

          packetHandler.write1ByteTxRx(portHandler,DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
          packetHandler.write1ByteTxRx(portHandler,DXL2_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)

          packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_POSITION, finalPos[index])
          packetHandler.write4ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_GOAL_POSITION, finalPos2[index])

          currentPos = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_PRESENT_POSITION) 
          currentPos2 = packetHandler.read4ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_PRESENT_POSITION)
          index =0
          index = 1
          
          Yp = 92.5 * math.cos(math.radians(Theta1))
          Xp = 92.5 * math.sin(math.radians(Theta1))
          Yp2 = 92.5 * math.cos(math.radians(Theta1+Theta2))
          Xp2 =  92.5 * math.sin(math.radians(Theta1+Theta2))  
          ansY = Xp + Xp2
          ansX = Yp + Yp2
          print(ansY, ansX)
          print(Theta2,Theta1)


          response = int(input("Type 1 if you want to continue if no type 0: "))
          if(response == 0):
               packetHandler.write1ByteTxRx(portHandler,DXL_ID, ADDR_PRO_TORQUE_ENABLE,TORQUE_DISABLE)
               packetHandler.write1ByteTxRx(portHandler,DXL2_ID, ADDR_PRO_TORQUE_ENABLE,TORQUE_DISABLE)
               break
               
          

          

          print(DXL_ID, currentPos)
          print(DXL2_ID, currentPos2)
          
          
          
          
     packetHandler.write1ByteTxRx(portHandler,DXL_ID, ADDR_PRO_TORQUE_ENABLE,TORQUE_DISABLE)
     packetHandler.write1ByteTxRx(portHandler,DXL2_ID, ADDR_PRO_TORQUE_ENABLE,TORQUE_DISABLE)








portHandler.closePort()