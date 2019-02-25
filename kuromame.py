import broadlink
import time
from tinydb import TinyDB, Query
from tinydb.operations import set


class kuromame:
    def __init__(self):
        self.devices = broadlink.discover(timeout=5)
        
        if len(self.devices) == 0 :
            print("device is not found.")
            print("connect same network with broadlink.")
            print("run kuromame().setting()")
            self.devices = None
        else:
            self.device = self.devices[0]
            self.device.auth()
    
    def setting(self,SSID,password,security=3):
        broadlink.setup(SSID,password,security)
        return broadlink.discover(timeout=5) #if not found return empty list []

    def learning(self):
        self.device.enter_learning()
        ir_packet = self.device.check_data()
        starttime = time.time()
        while ir_packet == None:
            ir_packet = self.device.check_data()
            if time.time() - starttime > 20:
                    print("signal not found")
                    break
        return ir_packet # if not found return None
    
    def send_packet(self,ir_packet):
        return self.device.send_data(ir_packet)

    def hexadecimal_to_bytes(self,hexa):
        return bytes.fromhex(hexa)

    def learning_mode(self):
        db = TinyDB("ir_packet.json")
        que = Query()
        flag = 0
        name = input("input learning device name:")
        db.insert({"name":name})
        while flag == 0:
            input_item_name = input("input your button name: ")
            print("send your button")
            packet = self.learning()
            packet = packet.hex() #bytes to hexadecimal
            if not packet == None:print(f"packet recieved  {packet}")
            db.update(set(input_item_name,packet),que.name == name)
            flag = int(input("[0]:continue, [1]:exit : "))

        print("end learning mode")

if __name__ == "__main__":
    cls = kuromame()
    if cls.devices == None:
        cls.setting()
    else:
        cls.learning_mode()

"""
db.update でpacketで受け取ったバイト列を登録できない
"""