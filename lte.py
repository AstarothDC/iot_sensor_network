from machine import UART
import time
import ujson

class SIM800L:
    def __init__(self, tx=27, rx=26, baudrate=9600):
        self.uart = UART(2, tx=tx, rx=rx, baudrate=baudrate)
        self._flush()

    def _flush(self):
        while self.uart.any():
            self.uart.read()

    def send_cmd(self, cmd, delay=1):
        self.uart.write((cmd + '\r\n').encode())
        time.sleep(delay)
        return self.uart.read()

    def send_json(self, url, data):
        data_str = ujson.dumps(data)
        self.send_cmd('AT')
        self.send_cmd('AT+SAPBR=3,1,"CONTYPE","GPRS"')
        self.send_cmd('AT+SAPBR=3,1,"APN","internet.claro.com.co"')  # Cambia el APN según tu operador
        self.send_cmd('AT+SAPBR=1,1', 3)
        self.send_cmd('AT+HTTPINIT')
        self.send_cmd(f'AT+HTTPPARA="URL","{url}"')
        self.send_cmd('AT+HTTPPARA="CONTENT","application/json"')
        self.send_cmd(f'AT+HTTPDATA={len(data_str)},10000')
        time.sleep(0.5)
        self.uart.write(data_str.encode())
        time.sleep(1)
        self.send_cmd('AT+HTTPACTION=1', 3)
        self.send_cmd('AT+HTTPTERM')
        self.send_cmd('AT+SAPBR=0,1')

    def test_connection(self):
        self.send_cmd('AT')
        self.send_cmd('AT+CSQ')
        self.send_cmd('AT+CREG?')
        self.send_cmd('AT+CGATT?')