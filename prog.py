import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from test1 import Ui_Dialog
from list_ports import serial_ports
import serial
import re
import threading
import io

cr = True
lf = True
timestamp = False

replchars = re.compile(r'[\n\r]')
def replchars_to_hex(match):
	return r'\0x{0:02x}'.format(ord(match.group()))

def reading():
	while True:
		# reading = ser.readline().decode('ascii')
		reading = sio.readline()
		if reading != '':
			prog.addToConsoleText(reading)
			# text = replchars.sub(replchars_to_hex, reading)
			# prog.infoLabel.setText('Bytes RX: '+ text)


class MyFirstGuiProgram(Ui_Dialog):
	def __init__(self, dialog):
		Ui_Dialog.__init__(self)
		self.setupUi(dialog)

		# Connect "add" button with a custom function (addInputTextToListbox)
		# self.addBtn.clicked.connect(self.addInputTextToListbox)
		# Connect "add" button with a custom function (addInputTextToListbox)
		self.refreshPortsButton.clicked.connect(self.readPorts)
		self.portsList.currentIndexChanged.connect(self.portSelected)
		self.dataWidthList.currentIndexChanged.connect(self.dataWidthChanged)
		self.baudrateList.currentIndexChanged.connect(self.baudrateChanged)
		self.stopBitsList.currentIndexChanged.connect(self.stopBitsChanged)
		self.parityList.currentIndexChanged.connect(self.parityChanged)
		self.flowControlList.currentIndexChanged.connect(self.flowControlChanged)
		self.openCloseButton.clicked.connect(self.openClosePort)
		self.crCheckBox.stateChanged.connect(self.crChanged)
		self.lfCheckBox.stateChanged.connect(self.lfChanged)
		self.timestampCheckBox.stateChanged.connect(self.timestampChanged)
		self.sendButton.clicked.connect(self.sendBytes)
		self.consoleTextEdit.ensureCursorVisible()

	def sendBytes(self):
		text = self.textToSend.text()
		self.infoLabel.setText('Original text: ' + text)
		if cr == True:
			text = text + '\r'
		if lf == True:
			text = text + '\n'
		if ser.is_open == True:
			print('Text being sent: ' + replchars.sub(replchars_to_hex, text))
			# ser.write(text.encode('utf-8'))
			sio.write(text)
		else:
			self.infoLabel.setText('Port is not open!')

		self.consoleTextEdit.setTextColor(QtGui.QColor(255,0,0))
		self.consoleTextEdit.append(text)
		self.consoleTextEdit.moveCursor(QtGui.QTextCursor.End)

		text = replchars.sub(replchars_to_hex, text)
		self.infoLabel.setText('Bytes to send: ' + text)




	def addInputTextToListbox(self):
		txt = self.myTextInput.text()
		self.listWidget.addItem(txt)

	def openClosePort(self):
		# check if port has already been open and then close it if necessary, or open
		if self.openCloseButton.text() == 'Open':
			try:
				ser.open()
				self.openCloseButton.setText('Close')
				self.currentPortLabel.setText(self.portsList.currentText() + ' open')
				reading_thread.start()
				# self.consoleTextEdit.setText('')
			except:
				self.currentPortLabel.setText('No ports available to open!')
		elif self.openCloseButton.text() == 'Close':
			ser.close()
			self.openCloseButton.setText('Open')
			self.currentPortLabel.setText(self.portsList.currentText() + ' closed')
		# self.infoLabel.setText('Open/close button clicked!')

	def readPorts(self):
		self.infoLabel.setText('Now reading ports')

		ser.close()
		self.openCloseButton.setText('Open')

		self.portsList.clear()
		ports = serial_ports()
		# ports.remove('COM1')
		for port in range(len(ports)):
			self.portsList.addItem(str(ports[port]))

	def portSelected(self):
		if self.portsList.currentText() == '':
			self.currentPortLabel.setText('No ports available')
		else:
			self.currentPortLabel.setText(self.portsList.currentText() + ' selected')
		ser.port = self.portsList.currentText()
		# self.infoLabel.setText('New port selected: ' + self.portsList.currentText())

	def dataWidthChanged(self):
		if self.dataWidthList.currentText() == '8 bits':
			ser.bytesize = serial.EIGHTBITS
		elif self.dataWidthList.currentText() == '7 bits':
			ser.bytesize = serial.SEVENBITS
		elif self.dataWidthList.currentText() == '6 bits':
			ser.bytesize = serial.SIXBITS
		elif self.dataWidthList.currentText() == '5 bits':
			ser.bytesize = serial.FIVEBITS
		else:
			ser.bytesize = serial.EIGHTBITS
		# self.infoLabel.setText('New datawidth selected: ' + self.dataWidthList.currentText())

	def baudrateChanged(self):
		ser.baudrate = int(self.baudrateList.currentText())
		# self.infoLabel.setText('New baudrate selected: ' + self.baudrateList.currentText())

	def stopBitsChanged(self):
		if self.stopBitsList.currentText() == '1 bit':
			ser.stopbits = serial.STOPBITS_ONE
		elif self.stopBitsList.currentText() == '1.5 bits':
			ser.stopbits = serial.STOPBITS_ONE_POINT_FIVE
		elif self.stopBitsList.currentText() == '2 bits':
			ser.stopbits = serial.STOPBITS_TWO
		else:
			ser.stopbits = serial.STOPBITS_ONE
		# self.infoLabel.setText('New stop bits selected: ' + self.stopBitsList.currentText())

	def parityChanged(self):
		if self.stopBitsList.currentText() == 'None':
			ser.parity = serial.PARITY_NONE
		elif self.stopBitsList.currentText() == 'Even':
			ser.parity = serial.PARITY_EVEN
		elif self.stopBitsList.currentText() == 'Odd':
			ser.parity = serial.PARITY_ODD
		elif self.stopBitsList.currentText() == 'Mark':
			ser.parity = serial.PARITY_MARK
		elif self.stopBitsList.currentText() == 'Space':
			ser.parity = serial.PARITY_SPACE
		else:
			ser.parity = serial.PARITY_NONE
		# self.infoLabel.setText('New parity selected: ' + self.parityList.currentText())

	def flowControlChanged(self):
		if self.flowControlList.currentText() == 'None':
			ser.xonxoff = False
			ser.dsrdtr = False
			ser.rtscts = False
		elif self.flowControlList.currentText() == 'Xon/Xoff':
			ser.xonxoff = True
			ser.dsrdtr = False
			ser.rtscts = False
		elif self.flowControlList.currentText() == 'DSR/DTR':
			ser.xonxoff = False
			ser.dsrdtr = True
			ser.rtscts = False
		elif self.flowControlList.currentText() == 'RTS/CTS':
			ser.xonxoff = False
			ser.dsrdtr = False
			ser.rtscts = True
		else:
			ser.xonxoff = False
			ser.dsrdtr = False
			ser.rtscts = False
		# self.infoLabel.setText('New flow control selected: ' + self.flowControlList.currentText())

	def crChanged(self):
		if self.crCheckBox.isChecked() == True:
			cr = True
		else:
			cr = False
		self.infoLabel.setText('New CR setting: ' + str(cr))

	def lfChanged(self):
		if self.lfCheckBox.isChecked() == True:
			lf = True
		else:
			lf = False
		self.infoLabel.setText('New LF setting: ' + str(lf))

	def timestampChanged(self):
		if self.timestampCheckBox.isChecked() == True:
			timestamp = True
		else:
			timestamp = False
		self.infoLabel.setText('New timestamp setting: ' + str(timestamp))

	def addToConsoleText(self,string):
		self.consoleTextEdit.setTextColor(QtGui.QColor(0,255,0))
		self.consoleTextEdit.append(string)
		self.consoleTextEdit.moveCursor(QtGui.QTextCursor.End)


if __name__ == '__main__':
	reading_thread = threading.Thread(target=reading, daemon=True)
	# reading_event = reading_thread.Event()

	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QDialog()
	prog = MyFirstGuiProgram(dialog)

	# prog.infoLabel.setText(prog.parityList.currentText())

	ports = serial_ports()
	# ports.remove('COM1')
	# prog.infoLabel.setText('Ports list:' + str(ports))
	ser = serial.Serial(baudrate = 115200, parity = serial.PARITY_NONE, xonxoff = False, dsrdtr = False, rtscts = False, stopbits = serial.STOPBITS_ONE, timeout = 1.0, bytesize = serial.EIGHTBITS)
	sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser), newline='\n')

	for port in range(len(ports)):
		prog.portsList.addItem(str(ports[port]))

	dialog.show()
	sys.exit(app.exec_())
	ser.close()             # close port

