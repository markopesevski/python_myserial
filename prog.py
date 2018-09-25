import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from test1 import Ui_Dialog
from list_ports import serial_ports
import serial
import re
import threading
import io
import time
import datetime
from PyCRC.CRC16 import CRC16
import binascii

cr = True
lf = True
timestamp = False
crc16 = True

replchars = re.compile(r'[\n\r]')
def replchars_to_hex(match):
	return r'\0x{0:02x}'.format(ord(match.group()))

def reading():
	while True:
		try:
			reading = ser.readline().decode('ascii')
			# reading = sio.readline()
			if reading != '':
				prog.addToConsoleText(reading)
				# text = replchars.sub(replchars_to_hex, reading)
				# prog.infoLabel.setText('Bytes RX: '+ text)
		except Exception as e:
			print(e)

class MyFirstGuiProgram(Ui_Dialog):
	def __init__(self, dialog):
		Ui_Dialog.__init__(self)
		self.setupUi(dialog)

		# Connect "add" button with a custom function (addInputTextToListbox)
		# self.addBtn.clicked.connect(self.addInputTextToListbox)
		# Connect "add" button with a custom function (addInputTextToListbox)
		self.refreshPortsButton.clicked.connect(self.readPorts)
		self.clearButton.clicked.connect(self.clearConsole)
		self.portsList.currentIndexChanged.connect(self.portSelected)
		self.dataWidthList.currentIndexChanged.connect(self.dataWidthChanged)
		self.baudrateList.currentIndexChanged.connect(self.baudrateChanged)
		self.stopBitsList.currentIndexChanged.connect(self.stopBitsChanged)
		self.parityList.currentIndexChanged.connect(self.parityChanged)
		self.flowControlList.currentIndexChanged.connect(self.flowControlChanged)
		self.openCloseButton.clicked.connect(self.openClosePort)
		self.crCheckBox.stateChanged.connect(self.crChanged)
		self.lfCheckBox.stateChanged.connect(self.lfChanged)
		self.crc16CheckBox.stateChanged.connect(self.crc16Changed)
		self.timestampCheckBox.stateChanged.connect(self.timestampChanged)
		self.sendButton.clicked.connect(self.sendBytesButton)
		self.consoleTextEdit.ensureCursorVisible()

		self.LTAON_Button.clicked.connect(self.LTAON_Button_cb)
		self.LTAOFF_Button.clicked.connect(self.LTAOFF_Button_cb)
		self.LTBON_Button.clicked.connect(self.LTBON_Button_cb)
		self.LTBOFF_Button.clicked.connect(self.LTBOFF_Button_cb)
		self.LTCON_Button.clicked.connect(self.LTCON_Button_cb)
		self.LTCOFF_Button.clicked.connect(self.LTCOFF_Button_cb)
		self.LTDON_Button.clicked.connect(self.LTDON_Button_cb)
		self.LTDOFF_Button.clicked.connect(self.LTDOFF_Button_cb)
		self.LTEON_Button.clicked.connect(self.LTEON_Button_cb)
		self.LTEOFF_Button.clicked.connect(self.LTEOFF_Button_cb)
		self.LTFON_Button.clicked.connect(self.LTFON_Button_cb)
		self.LTFOFF_Button.clicked.connect(self.LTFOFF_Button_cb)
		self.ALLLTON_Button.clicked.connect(self.ALLLTON_Button_cb)
		self.ALLLTOFF_Button.clicked.connect(self.ALLLTOFF_Button_cb)

		self.SHTAON_Button.clicked.connect(self.SHTAON_Button_cb)
		self.SHTAOFF_Button.clicked.connect(self.SHTAOFF_Button_cb)
		self.SHTBON_Button.clicked.connect(self.SHTBON_Button_cb)
		self.SHTBOFF_Button.clicked.connect(self.SHTBOFF_Button_cb)
		self.SHTCON_Button.clicked.connect(self.SHTCON_Button_cb)
		self.SHTCOFF_Button.clicked.connect(self.SHTCOFF_Button_cb)
		self.SHTDON_Button.clicked.connect(self.SHTDON_Button_cb)
		self.SHTDOFF_Button.clicked.connect(self.SHTDOFF_Button_cb)
		self.SHTEON_Button.clicked.connect(self.SHTEON_Button_cb)
		self.SHTEOFF_Button.clicked.connect(self.SHTEOFF_Button_cb)
		self.SHTFON_Button.clicked.connect(self.SHTFON_Button_cb)
		self.SHTFOFF_Button.clicked.connect(self.SHTFOFF_Button_cb)
		self.ALLSHTON_Button.clicked.connect(self.ALLSHTON_Button_cb)
		self.ALLSHTOFF_Button.clicked.connect(self.ALLSHTOFF_Button_cb)

		self.OUTAON_Button.clicked.connect(self.OUTAON_Button_cb)
		self.OUTAOFF_Button.clicked.connect(self.OUTAOFF_Button_cb)
		self.OUTBON_Button.clicked.connect(self.OUTBON_Button_cb)
		self.OUTBOFF_Button.clicked.connect(self.OUTBOFF_Button_cb)
		self.OUTCON_Button.clicked.connect(self.OUTCON_Button_cb)
		self.OUTCOFF_Button.clicked.connect(self.OUTCOFF_Button_cb)
		self.OUTDON_Button.clicked.connect(self.OUTDON_Button_cb)
		self.OUTDOFF_Button.clicked.connect(self.OUTDOFF_Button_cb)
		self.OUTEON_Button.clicked.connect(self.OUTEON_Button_cb)
		self.OUTEOFF_Button.clicked.connect(self.OUTEOFF_Button_cb)
		self.OUTFON_Button.clicked.connect(self.OUTFON_Button_cb)
		self.OUTFOFF_Button.clicked.connect(self.OUTFOFF_Button_cb)
		self.ALLOUTON_Button.clicked.connect(self.ALLOUTON_Button_cb)
		self.ALLOUTOFF_Button.clicked.connect(self.ALLOUTOFF_Button_cb)

		self.STARTSIGNALING_Button.clicked.connect(self.STARTSIGNALING_Button_cb)
		self.STOPSIGNALING_Button.clicked.connect(self.STOPSIGNALING_Button_cb)

		self.SENDAPOWER_Button.clicked.connect(self.SENDAPOWER_Button_cb)
		self.SENDBPOWER_Button.clicked.connect(self.SENDBPOWER_Button_cb)
		self.SENDCPOWER_Button.clicked.connect(self.SENDCPOWER_Button_cb)
		self.SENDDPOWER_Button.clicked.connect(self.SENDDPOWER_Button_cb)
		self.SENDEPOWER_Button.clicked.connect(self.SENDEPOWER_Button_cb)
		self.SENDFPOWER_Button.clicked.connect(self.SENDFPOWER_Button_cb)
		self.SENDALLPOWER_Button.clicked.connect(self.SENDALLPOWER_Button_cb)

		self.FREQUENCY_Button.clicked.connect(self.FREQUENCY_Button_cb)

		self.DAC2A_Button.clicked.connect(self.DAC2A_Button_cb)
		self.DAC2B_Button.clicked.connect(self.DAC2B_Button_cb)

		self.HEATERENABLE_Button.clicked.connect(self.HEATERENABLE_Button_cb)
		self.HEATERDISABLE_Button.clicked.connect(self.HEATERDISABLE_Button_cb)
		self.HEATERPOWER1_Button.clicked.connect(self.HEATERPOWER1_Button_cb)
		self.HEATERPOWER2_Button.clicked.connect(self.HEATERPOWER2_Button_cb)
		self.HEATERPOWER3_Button.clicked.connect(self.HEATERPOWER3_Button_cb)
		self.HEATERPOWER4_Button.clicked.connect(self.HEATERPOWER4_Button_cb)
		self.HEATERPOWER5_Button.clicked.connect(self.HEATERPOWER5_Button_cb)
		self.HEATERPOWER6_Button.clicked.connect(self.HEATERPOWER6_Button_cb)

		self.programsList.currentIndexChanged.connect(self.programChanged)

	def sendBytesButton(self):
		text = self.textToSend.text()
		self.infoLabel.setText('Original text: ' + text)
		# if crc16 == True:
		# 	crc = CRC16().calculate(text)
		# 	print('CRC16 int: ' + str(crc))
		# 	crc = format(crc, 'x')
		# 	print('CRC16 hex: ' + str(crc))
		# 	text = text + str(crc)
		if cr == True:
			text = text + '\r'
		if lf == True:
			text = text + '\n'
		if ser.is_open == True:
			print('Text being sent: ' + replchars.sub(replchars_to_hex, text))
			try:
				ser.write(text.encode('utf-8'))
				# sio.write(text)
			except Exception as e:
				print(e)
		else:
			self.infoLabel.setText('Port is not open!')

		ts = time.time()
		# st = datetime.datetime.fromtimestamp(ts).strftime('[%Y-%m-%d %H:%M:%S]')
		st = datetime.datetime.fromtimestamp(ts).strftime('[%H:%M:%S]')
		# print(st)

		self.consoleTextEdit.setTextColor(QtGui.QColor(0,255,0))
		self.consoleTextEdit.append(st + ' ')
		self.consoleTextEdit.setTextColor(QtGui.QColor(255,0,0))
		self.consoleTextEdit.append(text)
		self.consoleTextEdit.moveCursor(QtGui.QTextCursor.End)

		text = replchars.sub(replchars_to_hex, text)
		self.infoLabel.setText('Bytes to send: ' + text)

	def sendBytes(self,texttosend):
		if texttosend == '':
			text = self.textToSend.text()
		else:
			text = texttosend
		self.infoLabel.setText('Original text: ' + text)
		# if crc16 == True:
		# 	crc = CRC16().calculate(text)
		# 	print('CRC16 int: ' + str(crc))
		# 	crc = format(crc, 'x')
		# 	print('CRC16 hex: ' + str(crc))
		# 	text = text + str(crc)
		if cr == True:
			text = text + '\r'
		if lf == True:
			text = text + '\n'
		if ser.is_open == True:
			print('Text being sent: ' + replchars.sub(replchars_to_hex, text))
			try:
				ser.write(text.encode('utf-8'))
				# sio.write(text)
			except Exception as e:
				print(e)
		else:
			self.infoLabel.setText('Port is not open!')

		ts = time.time()
		# st = datetime.datetime.fromtimestamp(ts).strftime('[%Y-%m-%d %H:%M:%S]')
		st = datetime.datetime.fromtimestamp(ts).strftime('[%H:%M:%S]')
		# print(st)

		self.consoleTextEdit.setTextColor(QtGui.QColor(0,255,0))
		self.consoleTextEdit.append(st + ' ')
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

	def crc16Changed(self):
		if self.crc16CheckBox.isChecked() == True:
			crc16 = True
		else:
			crc16 = False
		self.infoLabel.setText('New CRC16 setting: ' + str(crc16))

	def addToConsoleText(self,string):
		ts = time.time()
		# st = datetime.datetime.fromtimestamp(ts).strftime('[%Y-%m-%d %H:%M:%S]')
		st = datetime.datetime.fromtimestamp(ts).strftime('[%H:%M:%S]')
		# print(st)

		self.consoleTextEdit.setTextColor(QtGui.QColor(0,255,0))
		self.consoleTextEdit.append(st + ' ')
		self.consoleTextEdit.setTextColor(QtGui.QColor(0,255,0))
		self.consoleTextEdit.append(string)
		self.consoleTextEdit.moveCursor(QtGui.QTextCursor.End)

	def clearConsole(self):
		self.consoleTextEdit.clear()

















	def LTAON_Button_cb(self):
		self.sendBytes("tla1")

	def LTAOFF_Button_cb(self):
		self.sendBytes("tla0")

	def LTBON_Button_cb(self):
		self.sendBytes("tlb1")

	def LTBOFF_Button_cb(self):
		self.sendBytes("tlb0")

	def LTCON_Button_cb(self):
		self.sendBytes("tlc1")

	def LTCOFF_Button_cb(self):
		self.sendBytes("tlc0")

	def LTDON_Button_cb(self):
		self.sendBytes("tld1")

	def LTDOFF_Button_cb(self):
		self.sendBytes("tld0")

	def LTEON_Button_cb(self):
		self.sendBytes("tle1")

	def LTEOFF_Button_cb(self):
		self.sendBytes("tle0")

	def LTFON_Button_cb(self):
		self.sendBytes("tlf1")

	def LTFOFF_Button_cb(self):
		self.sendBytes("tlf0")

	def SHTAON_Button_cb(self):
		self.sendBytes("tsa1")

	def SHTAOFF_Button_cb(self):
		self.sendBytes("tsa0")

	def SHTBON_Button_cb(self):
		self.sendBytes("tsb1")

	def SHTBOFF_Button_cb(self):
		self.sendBytes("tsb0")

	def SHTCON_Button_cb(self):
		self.sendBytes("tsc1")

	def SHTCOFF_Button_cb(self):
		self.sendBytes("tsc0")

	def SHTDON_Button_cb(self):
		self.sendBytes("tsd1")

	def SHTDOFF_Button_cb(self):
		self.sendBytes("tsd0")

	def SHTEON_Button_cb(self):
		self.sendBytes("tse1")

	def SHTEOFF_Button_cb(self):
		self.sendBytes("tse0")

	def SHTFON_Button_cb(self):
		self.sendBytes("tsf1")

	def SHTFOFF_Button_cb(self):
		self.sendBytes("tsf0")

	def OUTAON_Button_cb(self):
		self.sendBytes("toa1")

	def OUTAOFF_Button_cb(self):
		self.sendBytes("toa0")

	def OUTBON_Button_cb(self):
		self.sendBytes("tob1")

	def OUTBOFF_Button_cb(self):
		self.sendBytes("tob0")

	def OUTCON_Button_cb(self):
		self.sendBytes("toc1")

	def OUTCOFF_Button_cb(self):
		self.sendBytes("toc0")

	def OUTDON_Button_cb(self):
		self.sendBytes("tod1")

	def OUTDOFF_Button_cb(self):
		self.sendBytes("tod0")

	def OUTEON_Button_cb(self):
		self.sendBytes("toe1")

	def OUTEOFF_Button_cb(self):
		self.sendBytes("toe0")

	def OUTFON_Button_cb(self):
		self.sendBytes("tof1")

	def OUTFOFF_Button_cb(self):
		self.sendBytes("tof0")

	def STARTSIGNALING_Button_cb(self):
		self.sendBytes("ss1")

	def STOPSIGNALING_Button_cb(self):
		self.sendBytes("ss0")

	def SENDAPOWER_Button_cb(self):
		self.sendBytes("prfa" + self.APOWER_Text.text())

	def SENDBPOWER_Button_cb(self):
		self.sendBytes("prfb" + self.BPOWER_Text.text())

	def SENDCPOWER_Button_cb(self):
		self.sendBytes("prfc" + self.CPOWER_Text.text())

	def SENDDPOWER_Button_cb(self):
		self.sendBytes("prfd" + self.DPOWER_Text.text())

	def SENDEPOWER_Button_cb(self):
		self.sendBytes("prfe" + self.EPOWER_Text.text())

	def SENDFPOWER_Button_cb(self):
		self.sendBytes("prff" + self.FPOWER_Text.text())

	def FREQUENCY_Button_cb(self):
		self.sendBytes("pf" + self.FREQUENCY_Text.text())

	def DAC2A_Button_cb(self):
		self.sendBytes("prf2a" + self.DAC2A_Text.text())

	def DAC2B_Button_cb(self):
		self.sendBytes("prf2b" + self.DAC2B_Text.text())

	def ALLLTON_Button_cb(self):
		self.sendBytes("tla1")
		self.sendBytes("tlb1")
		self.sendBytes("tlc1")
		self.sendBytes("tld1")
		self.sendBytes("tle1")
		self.sendBytes("tlf1")

	def ALLLTOFF_Button_cb(self):
		self.sendBytes("tla0")
		self.sendBytes("tlb0")
		self.sendBytes("tlc0")
		self.sendBytes("tld0")
		self.sendBytes("tle0")
		self.sendBytes("tlf0")

	def ALLSHTON_Button_cb(self):
		self.sendBytes("tsa1")
		self.sendBytes("tsb1")
		self.sendBytes("tsc1")
		self.sendBytes("tsd1")
		self.sendBytes("tse1")
		self.sendBytes("tsf1")

	def ALLSHTOFF_Button_cb(self):
		self.sendBytes("tsa0")
		self.sendBytes("tsb0")
		self.sendBytes("tsc0")
		self.sendBytes("tsd0")
		self.sendBytes("tse0")
		self.sendBytes("tsf0")

	def ALLOUTON_Button_cb(self):
		self.sendBytes("toa1")
		self.sendBytes("tob1")
		self.sendBytes("toc1")
		self.sendBytes("tod1")
		self.sendBytes("toe1")
		self.sendBytes("tof1")

	def ALLOUTOFF_Button_cb(self):
		self.sendBytes("toa0")
		self.sendBytes("tob0")
		self.sendBytes("toc0")
		self.sendBytes("tod0")
		self.sendBytes("toe0")
		self.sendBytes("tof0")

	def SENDALLPOWER_Button_cb(self):
		self.sendBytes("prfa" + self.APOWER_Text.text())
		self.sendBytes("prfb" + self.BPOWER_Text.text())
		self.sendBytes("prfc" + self.CPOWER_Text.text())
		self.sendBytes("prfd" + self.DPOWER_Text.text())
		self.sendBytes("prfe" + self.EPOWER_Text.text())
		self.sendBytes("prff" + self.FPOWER_Text.text())


	def HEATERENABLE_Button_cb(self):
		self.sendBytes("he")

	def HEATERDISABLE_Button_cb(self):
		self.sendBytes("hd")

	def HEATERPOWER1_Button_cb(self):
		self.sendBytes("h0" + self.HEATERPOWER1_Text.text())

	def HEATERPOWER2_Button_cb(self):
		self.sendBytes("h1" + self.HEATERPOWER2_Text.text())

	def HEATERPOWER3_Button_cb(self):
		self.sendBytes("h2" + self.HEATERPOWER3_Text.text())

	def HEATERPOWER4_Button_cb(self):
		self.sendBytes("h3" + self.HEATERPOWER4_Text.text())

	def HEATERPOWER5_Button_cb(self):
		self.sendBytes("h4" + self.HEATERPOWER5_Text.text())

	def HEATERPOWER6_Button_cb(self):
		self.sendBytes("h5" + self.HEATERPOWER6_Text.text())

	def programChanged(self):
		self.sendBytes("ps" + str(self.programsList.currentIndex()))

































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
	# sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser), newline='\n')

	for port in range(len(ports)):
		prog.portsList.addItem(str(ports[port]))

	dialog.show()
	sys.exit(app.exec_())
	ser.close()             # close port

