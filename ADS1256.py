# #****************************************************************************
# * | File        :	  ads1256.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2019-03-13
# * | Info        :
# ******************************************************************************/
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import config
import RPi.GPIO as GPIO

# gain channel
ADS1256_GAIN_E = {'ADS1256_GAIN_1': 0,  # GAIN   1
                  'ADS1256_GAIN_2': 1,  # GAIN   2
                  'ADS1256_GAIN_4': 2,  # GAIN   4
                  'ADS1256_GAIN_8': 3,  # GAIN   8
                  'ADS1256_GAIN_16': 4,  # GAIN  16
                  'ADS1256_GAIN_32': 5,  # GAIN  32
                  'ADS1256_GAIN_64': 6,  # GAIN  64
                  }

# data rate
ADS1256_DRATE_E = {'ADS1256_30000SPS': 0xF0,  # reset the default values
                   'ADS1256_15000SPS': 0xE0,
                   'ADS1256_7500SPS': 0xD0,
                   'ADS1256_3750SPS': 0xC0,
                   'ADS1256_2000SPS': 0xB0,
                   'ADS1256_1000SPS': 0xA1,
                   'ADS1256_500SPS': 0x92,
                   'ADS1256_100SPS': 0x82,
                   'ADS1256_60SPS': 0x72,
                   'ADS1256_50SPS': 0x63,
                   'ADS1256_30SPS': 0x53,
                   'ADS1256_25SPS': 0x43,
                   'ADS1256_15SPS': 0x33,
                   'ADS1256_10SPS': 0x20,
                   'ADS1256_5SPS': 0x13,
                   'ADS1256_2d5SPS': 0x03
                   }

# registration definition
REG_E = {'REG_STATUS': 0,  # x1H
         'REG_MUX': 1,  # 01H
         'REG_ADCON': 2,  # 20H
         'REG_DRATE': 3,  # F0H
         'REG_IO': 4,  # E0H
         'REG_OFC0': 5,  # xxH
         'REG_OFC1': 6,  # xxH
         'REG_OFC2': 7,  # xxH
         'REG_FSC0': 8,  # xxH
         'REG_FSC1': 9,  # xxH
         'REG_FSC2': 10,  # xxH
         }

# command definition
CMD = {'CMD_WAKEUP': 0x00,  # Completes SYNC and Exits Standby Mode 0000  0000 (00h)
       'CMD_RDATA': 0x01,  # Read Data 0000  0001 (01h)
       'CMD_RDATAC': 0x03,  # Read Data Continuously 0000   0011 (03h)
       'CMD_SDATAC': 0x0F,  # Stop Read Data Continuously 0000   1111 (0Fh)
       'CMD_RREG': 0x10,  # Read from REG rrr 0001 rrrr (1xh)
       'CMD_WREG': 0x50,  # Write to REG rrr 0101 rrrr (5xh)
       'CMD_SELFCAL': 0xF0,  # Offset and Gain Self-Calibration 1111    0000 (F0h)
       'CMD_SELFOCAL': 0xF1,  # Offset Self-Calibration 1111    0001 (F1h)
       'CMD_SELFGCAL': 0xF2,  # Gain Self-Calibration 1111    0010 (F2h)
       'CMD_SYSOCAL': 0xF3,  # System Offset Calibration 1111   0011 (F3h)
       'CMD_SYSGCAL': 0xF4,  # System Gain Calibration 1111    0100 (F4h)
       'CMD_SYNC': 0xFC,  # Synchronize the A/D Conversion 1111   1100 (FCh)
       'CMD_STANDBY': 0xFD,  # Begin Standby Mode 1111   1101 (FDh)
       'CMD_RESET': 0xFE,  # Reset to Power-Up Values 1111   1110 (FEh)
       }


class ADS1256:
    def __init__(self):
        self.rst_pin = config.RST_PIN
        self.cs_pin = config.CS_PIN
        self.drdy_pin = config.DRDY_PIN

        self.AdcNow = [0, 0, 0, 0, 0, 0, 0, 0]  # ADC  Conversion value
        self.Channel = 0  # The current channel
        self.ScanMode = 0  # Scanning mode_ 0 : Single-ended input  8 channel; 1 : Differential input  4 channel

    # Hardware reset
    def ADS1256_Reset(self):
        config.digital_write(self.rst_pin, GPIO.HIGH)
        config.delay_ms(200)
        config.digital_write(self.rst_pin, GPIO.LOW)
        config.delay_ms(200)
        config.digital_write(self.rst_pin, GPIO.HIGH)

    def ADS1256_DelayUs(self, us):
        i = 0
        for i in range(0, us):
            i = i + 1

    def ADS1256_SendData(self, data):
        config.spi_writebyte([data])

    def ADS1256_ReadData(self):
        read_data = 0

        config.digital_write(self.cs_pin, GPIO.LOW)

        self.ADS1256_SendData(CMD['CMD_RDATA'])
        self.ADS1256_DelayUs(10)

        buf = config.spi_readbytes(0xff)
        # print(buf
        config.digital_write(self.cs_pin, GPIO.HIGH)

        read_data = buf[0] << 16
        read_data |= buf[1] << 8
        read_data |= buf[0]

        if (read_data & 0x800000):
            read_data |= 0xFF000000
        return read_data

    def ADS1256_WriteReg(self, _RegID, _RegValue):
        '''Write the corresponding register'''
        config.digital_write(self.cs_pin, GPIO.LOW)
        self.ADS1256_SendData(CMD['CMD_WREG'] | _RegID)
        self.ADS1256_SendData(0x00)

        self.ADS1256_SendData(_RegValue)
        config.digital_write(self.cs_pin, GPIO.HIGH)

    def ADS1256_ReadReg(self, _RegID):
        '''Read  the corresponding register'''
        config.digital_write(self.cs_pin, GPIO.LOW)
        self.ADS1256_SendData(CMD['CMD_RREG'] | _RegID)
        self.ADS1256_SendData(0x00)

        config.delay_ms(1)

        read_data = config.spi_readbytes(0xff)

        config.digital_write(self.cs_pin, GPIO.HIGH)
        return read_data[0]

    def ADS1256_WaitDRDY(self):
        for i in range(0, 400000, 1):
            if (config.digital_read(self.drdy_pin) == 0):
                break
        if (i >= 400000):
            print("Time Out ...\r\n")

    def ADS1256_ReadChipID(self):
        self.ADS1256_WaitDRDY()
        id = self.ADS1256_ReadReg(REG_E['REG_STATUS'])
        id = id >> 4
        print("id = ", id)
        if (id != 3):
            print("read ID error!!")
            exit()
        else:
            print("read ID success!!")

    def ADS1256_WriteCmd(self, _cmd):
        '''Sending a single byte order'''
        config.digital_write(self.cs_pin, GPIO.LOW)  # cs  0
        self.ADS1256_SendData(_cmd)
        config.digital_write(self.cs_pin, GPIO.HIGH)  # cs  0

    def ADS1256_CfgADC(self, _gain, _drate):
        '''The configuration parameters of ADC, gain and data rate'''
        self.Gain = _gain
        self.DataRate = _drate

        self.ADS1256_WaitDRDY()

        # Storage ads1256 register configuration parameters
        buf = [0x00, 0x00, 0x00, 0x00];

        '''Status register define
        			Bits 7-4 ID3, ID2, ID1, ID0  Factory Programmed Identification Bits (Read Only)

        			Bit 3 ORDER: Data Output Bit Order
        				0 = Most Significant Bit First (default)
        				1 = Least Significant Bit First
        			Input data  is always shifted in most significant byte and bit first. Output data is always shifted out most significant
        			byte first. The ORDER bit only controls the bit order of the output data within the byte.

        			Bit 2 ACAL : Auto-Calibration
        				0 = Auto-Calibration Disabled (default)
        				1 = Auto-Calibration Enabled
        			When Auto-Calibration is enabled, self-calibration begins at the completion of the WREG command that changes
        			the PGA (bits 0-2 of ADCON register), DR (bits 7-0 in the DRATE register) or BUFEN (bit 1 in the STATUS register)
        			values.

        			Bit 1 BUFEN: Analog Input Buffer Enable
        				0 = Buffer Disabled (default)
        				1 = Buffer Enabled

        			Bit 0 DRDY :  Data Ready (Read Only)
        				This bit duplicates the state of the DRDY pin.

        			ACAL=1  enable  calibration
        '''
        # //buf[0] = (0 << 3) | (1 << 2) | (1 << 1);//enable the internal buffer
        buf[0] = (0 << 3) | (1 << 2) | (0 << 1);  # 0000 0100: MSBF, Auto-cal, Buffer disabled, Data Ready

        # MUX: Input multiplexer Control register (Address 01h)
        # Bits 7-4: Positive Input Channel (0-7 = AIN0-7, 1xxx = AINCOM)
        # Bits 3-0: Negative Input Channel (0-7 = AIN0-7, 1xxx = AINCOM)
        buf[1] = 0x08  # Positive Input Channel: AIN0, Negative Input Channel: AINCOM

        '''
            ADCON: A/D Control Register (Address 02h)
        			Bit 7 Reserved, always 0 (Read Only)
        			Bits 6-5 CLK1, CLK0 : D0/CLKOUT Clock Out Rate Setting
        				00 = Clock Out OFF
        				01 = Clock Out Frequency = fCLKIN (default)
        				10 = Clock Out Frequency = fCLKIN/2
        				11 = Clock Out Frequency = fCLKIN/4
        				When not using CLKOUT, it is recommended that it be turned off. These bits can only be reset using the RESET pin.

        			Bits 4-3 SDCS1, SCDS0: Sensor Detect Current Sources
        				00 = Sensor Detect OFF (default)
        				01 = Sensor Detect Current = 0.5 A
        				10 = Sensor Detect Current = 2 A
        				11 = Sensor Detect Current = 10 A
        				The Sensor Detect Current Sources can be activated to verify  the integrity of an external sensor supplying a signal to the
        				ADS1255/6. A shorted sensor produces a very small signal while an open-circuit sensor produces a very large signal.

        			Bits 2-0 PGA2, PGA1, PGA0: Programmable Gain Amplifier Setting
        				000 = 1 (default)
        				001 = 2
        				010 = 4
        				011 = 8
        				100 = 16
        				101 = 32
        				110 = 64
        				111 = 64
        '''
        buf[2] = (0 << 5) | (0 << 3) | (_gain << 0)  # Clock out off, Sensor detect off, gain = 1
        # //ADS1256_WriteReg(REG_ADCON, (0 << 5) | (0 << 2) | (GAIN_1 << 1));	/*choose 1: gain 1 ;input 5V/
        buf[3] = self.DataRate  # ADS1256_DRATE_E[_drate]

        config.digital_write(self.cs_pin, GPIO.LOW)
        self.ADS1256_SendData(CMD['CMD_WREG'] | 0)  # Write register, starting with register address 0
        self.ADS1256_SendData(0x03);  # number of bytes to be sent: 4 (writing 4 registers), set the number = 4 - 1

        self.ADS1256_SendData(buf[0])  # Set the status register
        self.ADS1256_SendData(buf[1])  # Set the input channel parameters
        self.ADS1256_SendData(buf[2])  # Set the ADCON control register,gain
        self.ADS1256_SendData(buf[3])  # Set the output rate

        print("send data  = ", buf[0], buf[1], buf[2], buf[3])
        config.digital_write(self.cs_pin, GPIO.HIGH)

    def ADS1256_SetChannel(self, _ch):
        '''Configuration channel number
        	Bits 7-4 PSEL3, PSEL2, PSEL1, PSEL0: Positive Input Channel (AINP) Select
        		0000 = AIN0 (default)
        		0001 = AIN1
        		0010 = AIN2 (ADS1256 only)
        		0011 = AIN3 (ADS1256 only)
        		0100 = AIN4 (ADS1256 only)
        		0101 = AIN5 (ADS1256 only)
        		0110 = AIN6 (ADS1256 only)
        		0111 = AIN7 (ADS1256 only)
        		1xxx = AINCOM (when PSEL3 = 1, PSEL2, PSEL1, PSEL0 are dont care)

        		NOTE: When using an ADS1255 make sure to only select the available inputs.

        	Bits 3-0 NSEL3, NSEL2, NSEL1, NSEL0: Negative Input Channel (AINN)Select
        		0000 = AIN0
        		0001 = AIN1 (default)
        		0010 = AIN2 (ADS1256 only)
        		0011 = AIN3 (ADS1256 only)
        		0100 = AIN4 (ADS1256 only)
        		0101 = AIN5 (ADS1256 only)
        		0110 = AIN6 (ADS1256 only)
        		0111 = AIN7 (ADS1256 only)
        		1xxx = AINCOM (when NSEL3 = 1, NSEL2, NSEL1, NSEL0 are dont care)
        '''
        if (_ch > 7):
            return
        self.ADS1256_WriteReg(REG_E['REG_MUX'], (_ch << 4) | (1 << 3))  # Bit3 = 1, AINN connection AINCOM
        # self.Channel = _ch

    def ADS1256_StartScan(self, _ucScanMode, _chnum):
        '''Configuration DRDY PIN for external interrupt is triggered'''
        self.ScanMode = _ucScanMode
        self.Channel = _chnum
        self.ADS1256_SetChannel(self.Channel)
        self.AdcNow = [0, 0, 0, 0, 0, 0, 0, 0]  # reset

    def ADS1256_ISR(self):
        '''Collection procedures'''
        if (self.ScanMode == 0):  # 0  Single-ended input  8 channel
            # print("ScanMode = 0,Single-ended input  8 channel"
            self.ADS1256_SetChannel(self.Channel)  # Switch channel mode
            self.ADS1256_DelayUs(5)

            self.ADS1256_WriteCmd(CMD['CMD_SYNC'])
            self.ADS1256_DelayUs(5)

            self.ADS1256_WriteCmd(CMD['CMD_WAKEUP']);
            self.ADS1256_DelayUs(25)

            if (self.Channel == 0):
                # self.AdcNow[self.Channel] = self.ADS1256_ReadData()
                self.AdcNow[7] = self.ADS1256_ReadData()
            else:
                self.AdcNow[self.Channel - 1] = self.ADS1256_ReadData()

            self.Channel = self.Channel + 1
            if (self.Channel >= 8):
                self.Channel = 0

        else:  # 1 Differential input  4 channel
            print("ScanMode = 1,Differential input  4 channel")
            self.ADS1256_SetDiffChannel(self.Channel)  # change DiffChannel
            self.ADS1256_DelayUs(5)

            self.ADS1256_WriteCmd(CMD['CMD_SYNC'])
            self.ADS1256_DelayUs(5)

            self.ADS1256_WriteCmd(CMD['CMD_WAKEUP'])
            self.ADS1256_DelayUs(25)

            if (self.Channel == 0):
                self.AdcNow[3] = self.ADS1256_ReadData()
            else:
                self.AdcNow[self.Channel - 1] = self.ADS1256_ReadData()

            self.Channel = self.Channel + 1
            if (self.Channel >= 4):
                self.Channel = 0

    def ADS1256_GetAdc(self, _ch):
        '''read stored ADC value'''
        if (_ch > 7):
            return 0
        return self.AdcNow[_ch]

    def ADS1256_Scan(self):
        '''Scan function'''
        if (config.digital_read(self.drdy_pin) == 0):
            # print("goto ADS1256_ISR"
            self.ADS1256_ISR()
            return 1
        return 0

    def ADS1256_Init(self):
        print("ADS1256 Init")
        if (config.module_init() != 0):
            return -1
        self.ADS1256_Reset()
        self.ADS1256_ReadChipID()

        # print("goto ADS1256_CfgADC"
        self.ADS1256_CfgADC(ADS1256_GAIN_E['ADS1256_GAIN_1'], ADS1256_DRATE_E['ADS1256_15SPS'])
        # print("goto ADS1256_StartScan"
        self.ADS1256_StartScan(0, 0)

    def ADS1256_GetAll(self):
        print(" ADS1256_GetAll")
        adc = [0, 0, 0, 0, 0, 0, 0, 0]  # -1.0
        volt = [0, 0, 0, 0, 0, 0, 0, 0]  # -2.0
        while True:
            if (self.ADS1256_Scan() == 1):
                for i in range(0, 8):
                    adc[i] = self.ADS1256_GetAdc(i)
                    volt[i] = (adc[i] * 100) / 167 / 100000.0
                    print("i = ", i, "adc= ", adc[i], "volt = ", volt[i])
            else:
                print("NO scan performed!")
            config.delay_ms(100)

    # def ADS1256_GetoneChannel(self, Channel):
    #     print(" ADS1256_GetAll")
    #     adc = [0, 0, 0, 0, 0, 0, 0, 0]  # -1.0
    #     volt = [0, 0, 0, 0, 0, 0, 0, 0]  # -2.0
    #     while True:
    #         if (self.ADS1256_Scan() == 1):
    #             adc[Channel] = self.ADS1256_GetAdc(Channel)
    #             volt[Channel] = (adc[Channel] * 100) / 167 / 100000.0
    #             print("i = ", Channel, "adc= ", adc[Channel], "volt = ", volt[Channel])
    #         else:
    #             print("NO scan performed!")
    #         config.delay_ms(100)

    def ADS1256_GetoneChannel(self, Channel):
        print(" ADS1256_GetAll")
        adc = [0, 0, 0, 0, 0, 0, 0, 0]  # -1.0
        volt = [0, 0, 0, 0, 0, 0, 0, 0]  # -2.0
        while True:
            if (self.ADS1256_Scan() == 1):
                adc[Channel] = self.ADS1256_GetAdc(Channel)
                volt[Channel] = (adc[Channel] * 100) / 167 / 100000.0
                # print("i = ", Channel, "adc= ", adc[Channel], "volt = ", volt[Channel])
                return adc[Channel]
            else:
                # print("NO scan performed!")
                pass
            config.delay_ms(100)