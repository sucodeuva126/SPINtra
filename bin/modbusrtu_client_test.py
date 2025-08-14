from pymodbus.client.sync import ModbusSerialClient
from pymodbus.transaction import ModbusRtuFramer
import logging

FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)  

rtu_framer = ModbusRtuFramer
serial_port = "COM6"
client = ModbusSerialClient( method='rtu', port=serial_port, timeout = 1, baudrate = 9600)
UNIT = 0x1

log.debug("Write to a holding register and read back")
rq = client.write_register(717, 500  , unit=UNIT)
rr = client.read_holding_registers(717, 1, unit=UNIT)

client.close()





