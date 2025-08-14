from pymodbus.server.sync import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.transaction import ModbusRtuFramer
serial_port = "COM7"


def run_sync_server():
    n = 780
    store = ModbusSlaveContext(di=ModbusSequentialDataBlock(0, [17]*n),
        co=ModbusSequentialDataBlock(0, [17]*n),
        hr=ModbusSequentialDataBlock(0, [17]*n),
        ir=ModbusSequentialDataBlock(0, [17]*n))
    context = ModbusServerContext(slaves=store, single= True)
    StartSerialServer(context=context, identity=None, framer= ModbusRtuFramer, port = serial_port, baudrate = 9600, stopbits = 1, bytesize = 8)
    return None #ERROR ON PARITY, BYTESIZE values

