import pyautogui
import serial
import argparse
import time
import logging

class MyControllerMap:
    def __init__(self):
        self.buttonskip = {'A': 'nexttrack'} # Pular a música
        self.buttonprev = {'B': 'prevtrack'} # Música anterior
        self.buttonpause = {'C': 'playpause'} # Pause/Play
        self.buttonup = {'D': 'volumeup'} # Aumentar volume
        self.buttondown = {'E': 'volumedown'} # Diminuir volume

class SerialControllerInterface:
    # Protocolo
    # byte 1 -> Botão 1 (estado - Apertado 1 ou não 0)
    # byte 2 -> EOP - End of Packet -> valor reservado 'X'

    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate=baudrate)
        self.mapping = MyControllerMap()
        self.incoming = '0'
        pyautogui.PAUSE = 0  ## remove delay
    
    def update(self):
        ## Sync protocol
        while self.incoming != b'X':
            self.incoming = self.ser.read()
            logging.debug("Received INCOMING: {}".format(self.incoming))

        data = self.ser.read()
        logging.debug("Received DATA: {}".format(data))

        if data == b'1':
            logging.info("KEYDOWN A")
            pyautogui.keyDown(self.mapping.buttonskip['A'])
        elif data == b'0':
            logging.info("KEYUP A")
            pyautogui.keyUp(self.mapping.buttonskip['A'])
        elif data == b'2':
            logging.info("KEYDOWN A")
            pyautogui.keyDown(self.mapping.buttonprev['B'])
        elif data == b'3':
            logging.info("KEYUP A")
            pyautogui.keyUp(self.mapping.buttonprev['B'])
        elif data == b'4':
            logging.info("KEYDOWN A")
            pyautogui.keyDown(self.mapping.buttonpause['C'])
        elif data == b'5':
            logging.info("KEYUP A")
            pyautogui.keyUp(self.mapping.buttonpause['C'])
        elif data == b'6':
            logging.info("KEYDOWN A")
            pyautogui.keyDown(self.mapping.buttonup['D'])
        elif data == b'7':
            logging.info("KEYUP A")
            pyautogui.keyUp(self.mapping.buttonup['D'])
        elif data == b'8':
            logging.info("KEYDOWN A")
            pyautogui.keyDown(self.mapping.buttondown['E'])
        elif data == b'9':
            logging.info("KEYUP A")
            pyautogui.keyUp(self.mapping.buttondown['E'])

        self.incoming = self.ser.read()


class DummyControllerInterface:
    def __init__(self):
        self.mapping = MyControllerMap()

    def update(self):
        pyautogui.keyDown(self.mapping.buttonup['D'])
        time.sleep(1)
        pyautogui.keyUp(self.mapping.buttonup['D'])
        logging.info("[Dummy] Pressed A button")
        time.sleep(10)
        pyautogui.keyDown(self.mapping.buttondown['E'])
        time.sleep(1)
        pyautogui.keyUp(self.mapping.buttondown['E'])
        logging.info("[Dummy] Pressed A button")
        time.sleep(10)


if __name__ == '__main__':
    interfaces = ['dummy', 'serial']
    argparse = argparse.ArgumentParser()
    argparse.add_argument('serial_port', type=str)
    argparse.add_argument('-b', '--baudrate', type=int, default=9600)
    argparse.add_argument('-c', '--controller_interface', type=str, default='serial', choices=interfaces)
    argparse.add_argument('-d', '--debug', default=False, action='store_true')
    args = argparse.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    print("Connection to {} using {} interface ({})".format(args.serial_port, args.controller_interface, args.baudrate))
    if args.controller_interface == 'dummy':
        controller = DummyControllerInterface()
    else:
        controller = SerialControllerInterface(port=args.serial_port, baudrate=args.baudrate)

    while True:
        controller.update()
