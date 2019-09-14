from smbus import SMBus

from objects.anim_action import AnimAction

#I2C_ADDR = 0x8      # bus address
I2C_BUS = SMBus(1)  # indicates /dev/ic2-1



def write_anim_i2c(action):
    # data struct == device type, device_id, setting (3 bytes)
    data = [action.device_type.encode()[0], action.device_id, action.setting]
    I2C_BUS.write_i2c_block_data(action.device_i2c_addr, 0x0, data)
    #I2C_BUS.write_byte(I2C_ADDR, action.device_type.encode()[0])
    #I2C_BUS.write_byte(I2C_ADDR, action.device_id)
    #I2C_BUS.write_byte(I2C_ADDR, action.setting)

def read_mecca_i2c(i2c_addr):
    # this is designed to read 6 MeccaBrain modules when they are in LIM mode

    # data struct == device id, setting, device id, setting, device id, setting, 
    # device id, setting, device id, setting, device id, setting, status (12 bytes)
    data = I2C_BUS.read_i2c_block_data(i2c_addr, 0x0, 13)
    return data