import time

def serial_poll():
        # print("Polling serial device for status...")
        pass


class ArduinoSerial:
    def __init__(self):
        # this will be the reference to the ground station object
        self.gsa_obj = None
        pass

    def set_gsa_ref(self, gsa_obj):
        self.gsa_obj = gsa_obj

    def run(self, pyroChanConf, updatePyroChan):

        print("Arduino Serial still in developement")

        # Main loop
        while(True):
            time.sleep(1)

            serial_poll()

            if(updatePyroChan.is_set()): 
                print(f"Received data {pyroChanConf.get_attr('a_tsll_e').get()} in serial thread")
                updatePyroChan.clear()
            


        # print("Input 1")
        
        # time.sleep(2)
        # print("Input 2")
        # self.gsa_obj.nova_light['style'] = 'Green.TFrame'
        # self.gsa_obj.mda.set("Abc")
        # self.gsa_obj.call_sign.set(5)
        # time.sleep(3)
        # self.gsa_obj.call_sign.set("Blah")
        # self.gsa_obj.nova_light['style'] = 'Red.TFrame'
        # self.gsa_obj.mda.set("def")
        # print("Final input test")
 
        # Dummy data setup
        # self.gsa_obj.nova_light['style'] = 'Green.TFrame'
        # self.gsa_obj.arduino_light['style'] = 'Green.TFrame'
 
        # self.gsa_obj.connection_status.set("BABABOOEY")
        # self.gsa_obj.connection_status_lb['style'] = 'HeaderGreen.TLabel'
        # self.gsa_obj.call_sign.set("KO4WVK")
        # self.gsa_obj.serial   .set(11051)
        # self.gsa_obj.flight   .set(1)
        # self.gsa_obj.state    .set("drogue")
        # self.gsa_obj.rssi     .set(-33)
        # self.gsa_obj.age      .set(0)
 
        # self.gsa_obj.mda              .set(3040)
        # self.gsa_obj.apg_delay        .set(5.25)
        # self.gsa_obj.apg_lockout      .set(10.68)
        # self.gsa_obj.bf               .set(4000)


        
        

    