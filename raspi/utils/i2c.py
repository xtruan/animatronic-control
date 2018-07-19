from smbus import SMBus

from objects.anim_action import AnimAction

I2C_ADDR = 0x8      # bus address
I2C_BUS = SMBus(1)  # indicates /dev/ic2-1



def write_anim_i2c(action):
    data = [action.device_type.encode()[0], action.device_id, action.setting]
    I2C_BUS.write_i2c_block_data(I2C_ADDR, 0x0, data)
    #I2C_BUS.write_byte(I2C_ADDR, action.device_type.encode()[0])
    #I2C_BUS.write_byte(I2C_ADDR, action.device_id)
    #I2C_BUS.write_byte(I2C_ADDR, action.setting)