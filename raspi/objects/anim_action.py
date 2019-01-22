
class AnimAction:
    def __init__(self, time_str, time_sec, device_i2c_addr, device_type, device_id, setting):
        self.time_str = time_str
        self.time_sec = time_sec
        self.device_i2c_addr = device_i2c_addr
        self.device_type = device_type
        self.device_id = device_id
        self.setting = setting

    def __str__(self):
        return str(self.time_str) + '-' + str(self.device_i2c_addr) + '-' + str(self.device_type) + '-' + str(self.device_id) + '-' + str(self.setting)
    