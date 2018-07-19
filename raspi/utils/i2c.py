from smbus2 import SMBus

from objects.anim_action import AnimAction

I2C_ADDR = 0x8      # bus address
I2C_BUS = SMBus(1)  # indicates /dev/ic2-1

def write_anim_i2c(action):
    I2C_BUS.write_byte(I2C_ADDR, action.encode().device_type[0])
    I2C_BUS.write_byte(I2C_ADDR, action.device_id)
    I2C_BUS.write_byte(I2C_ADDR, action.setting)