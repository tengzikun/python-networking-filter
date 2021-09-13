# tengzikun
# A0199547H
from socket import*
import sys
#FINAL COPY


port = int(sys.argv[1])
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', port))
## ready for message
serverSocket.listen(1)
keyMap ={"123" : b''} # value is b
counterMap ={"123":''} #value is a string
#check if double space is reached
def scanTillDoubleSpacing():
    spacing = 0
    nextWord = ''
    answer = ''
    while spacing < 2:
        nextWord = connectionSocket.recv(1).decode()
        if nextWord == ' ':
            spacing += 1
        else :
            answer += nextWord
            spacing = 0
    return answer

def scanTillDoubleSpacingLEE():
    spacing = 0
    nextWord = ''
    answer = ''
    while spacing < 2:
        nextWord = connectionSocket.recv(1).decode()
        if nextWord == ' ':
            spacing += 1
            answer += nextWord
        else :
            answer += nextWord
            spacing = 0
    return answer
#check if single space is reached
def scanTillSingleSpacing():
    spacing = 0
    nextWord =''
    answer = ''
    while spacing < 1:
        nextWord = connectionSocket.recv(1).decode()
        if nextWord == ' ':
            spacing += 1
            break #double insurance
        else :
            answer += nextWord
    return answer

    




while True:
    connectionSocket,IPAddress = serverSocket.accept()
   # counter = 0
    canRead = True
    message = ''
    storage = ''
    Rmessage = ''
    answer = ''
    while canRead:
        message =''
        message = connectionSocket.recv(1).decode().upper()
        if not message :
            canRead = False
            
        
        #GET
        if message == 'G':
            storage = ''
            for x in range(5):
                storage += connectionSocket.recv(1).decode()
            garbage = ''

            if storage.find('k') >= 0 : # its key
                garbage1=''
                for x in range(3):
                    garbage1 = connectionSocket.recv(1).decode() #ey/
                    garbage +=  garbage1
                
                key = scanTillDoubleSpacing()

                if key in keyMap and key in counterMap: #keymap exist but counter value is positive
                    Rmessage = ("200 OK Content-Length " + str(len(keyMap.get(key))) + "  ").encode() + keyMap.get(key)
                    number = counterMap.get(key)
                    num = 0
                    num = int(number)
                    num = num - 1 
                    if num == 0: #if number of retrieval in counter map is 0, delete key from both stores
                        counterMap.pop(key)
                        keyMap.pop(key)
                        connectionSocket.send(Rmessage)
                        #continue
                    else:
                        counterMap.update({key : str(num)}) #decrease the value of the counter by 1
                        connectionSocket.send(Rmessage)
                        storage = '' #clean it
                       # continue
                elif key not in keyMap: # not found in keymap
                    Rmessage = "404 NotFound  "
                    connectionSocket.send(Rmessage.encode())
                    #continue
                 
                elif key in keyMap and key not in counterMap: # in keymap but not in countermap
                    Rmessage =( "200 OK Content-Length " + str(len(keyMap.get(key))) + "  ").encode() + keyMap.get(key)
                    connectionSocket.send(Rmessage)
                    #continue

            elif storage.find('c') >= 0: # counter
                storage = '' # clean it
                #remove the next 7
                garbage = ""
                for i in range(7):
                    garbage += connectionSocket.recv(1).decode()
                key = scanTillDoubleSpacing()
                if key not in keyMap:
                    Rmessage = "404 NotFound  " # not found in both maps
                    connectionSocket.send(Rmessage.encode())
                   #continue

                elif key not in counterMap and key in keyMap:  # exist in counter map but not keymap
                    Rmessage = "200 OK Content-Length 8  Infinity"
                    connectionSocket.send(Rmessage.encode())
                   # continue

                elif key in counterMap and key in keyMap: # key exists in both maps
                    Rmessage = "200 OK Content-Length " + str(len(str(counterMap.get(key)))) + "  " + str(counterMap.get(key))
                    connectionSocket.send(Rmessage.encode())
                   # continue

        #POST
        elif message == "P":
            storage = ""
            for x in range(6):
                storage += connectionSocket.recv(1).decode().lower()
            if storage.find('k')>= 0: #its key
                garbage = ''
                for i in range(3): #remove the next 3   
                    garbage1 = connectionSocket.recv(1).decode()
                    garbage += garbage1
                key = scanTillSingleSpacing()
                if key in keyMap and key in counterMap: #keymap exist and counter value >0
                    Rmessage = '405 MethodNotAllowed  '
                    connectionSocket.send(Rmessage.encode())
                    jiajun = scanTillDoubleSpacingLEE()
                    jiajun1 = jiajun.split()
                    num3 = jiajun1[1]
                    for i in range(int(num3)):
                        connectionSocket.recv(1)
                else:
                    garbageLEE = ''
                    value = ''.encode()
                    garbageLEE = scanTillDoubleSpacingLEE()
                    jiajun1 = garbageLEE.split()
                    i = 0
                    num4 = 0 
                    while True:
                        if jiajun1[i].upper() == "CONTENT-LENGTH" and jiajun1[i+1].isdigit():
                            num4 = int(jiajun1[i+1])
                            
                            break
                        else:
                            i+=1

                    num6 = num4
                    while num6 > 0:
                        value += connectionSocket.recv(num6)
                        num6 = num4 - len(value)


                    if key not in keyMap: ##insertion
                        keyMap.update({key : value}) 
                    else :
                        keyMap[key] = value
                    Rmessage = '200 OK  '
                    connectionSocket.send(Rmessage.encode())

            elif storage.find('c') >= 0: # counter
                garbage = ''
                for i in range(7): # remove the next 7
                    garbage += connectionSocket.recv(1).decode()
                key = scanTillSingleSpacing()
                if key not in keyMap: # want to post in countermap but key dont even exist in keymap
                    Rmessage = '405 MethodNotAllowed  '
                    connectionSocket.send(Rmessage.encode())
                    jiajun = scanTillDoubleSpacingLEE()
                    jiajun1 = jiajun.split()
                    num3 = jiajun1[1]
                    for i in range(int(num3)):
                        connectionSocket.recv(1)
                    continue
                else: #update the countermap
                    garbage = scanTillSingleSpacing()
                    temp = scanTillDoubleSpacing()
                    lengthNumber =''
                    for i in temp.split():
                        if i.isdigit():
                            lengthNumber += str(i)
                    int(lengthNumber) # find length
                    actualLength = ''
                    for i in range(int(lengthNumber)):
                        actualLength += connectionSocket.recv(1).decode() #value of the counter\

                    if key not in counterMap:
                        counterMap[key] = actualLength #add new counter
                    else:
                        number = counterMap.get(key) #update the counter
                        num = 0
                        num = int(actualLength) + int(number)
                        str(num)
                        counterMap[key] = num

                    Rmessage = '200 OK  '
                    connectionSocket.send(Rmessage.encode())
        
        elif message == 'D':  # deletion
            storage = ''
            for i in range(8):
                storage += connectionSocket.recv(1).decode()
            
            if storage.find('k') >= 0: #key
                garbage=''
                for i in range(3):
                    garbage += connectionSocket.recv(1).decode()
            
                key = scanTillDoubleSpacing()
                if key in counterMap:   #countermap has positive count
                    Rmessage = "405 MethodNotAllowed  "
                    connectionSocket.send(Rmessage.encode())
                    #continue
                elif key not in keyMap: #key does not exist
                    Rmessage = '404 NotFound  '
                    connectionSocket.send(Rmessage.encode())
                   # continue
                elif key in keyMap: #delete from keymap
                    Rmessage = ('200 OK Content-Length '+ str(len(keyMap.get(key))) + "  " ).encode()+ keyMap.get(key)
                    Rmessage
                    keyMap.pop(key) #remove from keymap
                    counterMap.pop(key,None)
                    connectionSocket.send(Rmessage)
                    #continue
                
            elif storage.find('c') >= 0: #counter
                garbage = ''
                for i in range(7):
                    garbage += connectionSocket.recv(1).decode()
                
                key = scanTillDoubleSpacing()
                #HERE IM ASSUMING THE MOMENT I WANT TO DELETE COUNTER, I CAN JUST DELETE
                if key not in counterMap: # no such value in counterMap
                    Rmessage = '404 NotFound  '
                    connectionSocket.send(Rmessage.encode())
                    #continue
                else:
                    value = counterMap.get(key)
                    Rmessage = '200 OK Content-Length ' + str(len(str(value))) + "  " + str(counterMap.get(key))
                    counterMap.pop(key)
                    connectionSocket.send(Rmessage.encode())

connectionSocket.close()