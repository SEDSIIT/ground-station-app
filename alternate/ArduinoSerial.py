import time

class ArduinoSerial:
    def __init__(self):
        # this will be the reference to the ground station object
        self.gsa_obj = None
        pass

    def set_gsa_ref(self, gsa_obj):
        self.gsa_obj = gsa_obj
    
    def run(self):
        print("Input 1")
        
        time.sleep(2)
        print("Input 2")
        self.gsa_obj.nova_light['style'] = 'Green.TFrame'
        self.gsa_obj.mda.set("Abc")
        self.gsa_obj.call_sign.set(5)
        time.sleep(3)
        self.gsa_obj.call_sign.set("Blah")
        self.gsa_obj.nova_light['style'] = 'Red.TFrame'
        self.gsa_obj.mda.set("def")
        print("Final input test")
        pass

    def update(self):
        pass