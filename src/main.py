import random, time, datetime

# Interface class defines the method signature
class MachineInterface:
    def generate_data(self):
        pass
    
    def set_status(self, status):
        pass

    def get_status(self):
        pass
    
    def __str__(self):
        machine = self.machine_attributes
        return f"Machine ID:    {machine["machine_id"]} \nMachine Type:  {machine["machine_type"]}"
    
# Base class defines default class config
class Machine(MachineInterface):
    status_modes = {
        "off": "off",
        "idle": "idle",
        "active": "active",
        "maintenance": "maintenance",
        "error": "error"
    }
    machine_types = {
        "jet_printer": "jet_printer"
    }

    machine_attributes = {"machine_id": "", "machine_type": ""}
    machine_data = {"timestamp": "", "status": ""}

    def __init__(self, machine_id: str, machine_type: str):
        self.machine_attributes["machine_id"] = machine_id
        self.machine_attributes["machine_type"] = machine_type
        
    def generate_data(self):
        # Create timestamp
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        self.machine_data["timestamp"] = timestamp
        
        # Combine machine_attributes dict and machine_data dict
        generated_data = self.machine_attributes.copy()
        generated_data.update(self.machine_data)

        return generated_data
    
    def set_status(self, status):
        if status in self.status_modes:
            self.status = status
        else:
            print(f"Status mode doesn't exist, choose avaiable mode {self.status_modes}")

    def get_status(self):
        return self.status

# Sub-class modifies base class
class JetPrinter(Machine):
    machine_data = {"temperature": ""}

    def generate_data(self):
        base_data = super().generate_data()
        #base_data.update(self.machine_data)
        generated_data = base_data

        return generated_data 

    def set_temperature(self, temp):
        self.machine_data["temperature"] = temp

# Factory class creates subclasses
class MachineFactory:
    def create_machine(type: str):
        if type in Machine.machine_types:
            if type == "jet_printer":
                return JetPrinter("A1", Machine.machine_types[type])
        else:
            return f"Machine type not found \n Available Types: {Machine.machine_types}"
        
if __name__ == "__main__":
    # Test machine factory logic
    machine1 = MachineFactory.create_machine("jet_printer")
    machine1.set_status("idle")
    machine1.set_temperature("105")

    print(machine1.generate_data())


