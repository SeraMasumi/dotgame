import queue
import subprocess
import threading
import shutil
import io


class AD_reader(threading.Thread):
    def __init__(self, AD_tablet_queue, AD_joystick_x_queue, AD_joystick_y_queue):
        threading.Thread.__init__(self)
        # self.AD_tablet_value = -1
        self.AD_tablet_queue = AD_tablet_queue
        self.AD_joystick_x_queue = AD_joystick_x_queue
        self.AD_joystick_y_queue = AD_joystick_y_queue

    def run(self):
        err_buf = io.BytesIO()

        cmd = ["sudo ./ads1256_test"]
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err_thread = threading.Thread(target=shutil.copyfileobj, args=(proc.stderr, err_buf))
        err_thread.start()
        for line in proc.stdout:
            lineEntry = line.decode('utf-8')
            if lineEntry[0] == '2' or lineEntry[0] == '3' or lineEntry[0] == '4':
                number, code, bigNumber, voltage, smallNumber = AD_reader.WorkWithValues(self, lineEntry)
                if lineEntry[0] == '2':
                    AD_reader.myPut_size1(self, self.AD_tablet_queue, bigNumber)
                    # print("in AD_reader, AD_tablet_value = ", self.AD_tablet_value)
                elif lineEntry[0] == '3':
                    self.AD_joystick_x_queue.put(bigNumber)
                    AD_reader.myPut(self, self.AD_joystick_x_queue, bigNumber)
                    # print("in AD_reader, AD_joystick_x_queue size = ", self.AD_joystick_x_queue.qsize())
                elif lineEntry[0] == '4':
                    AD_reader.myPut(self, self.AD_joystick_y_queue, bigNumber)
                    # print("in AD_reader, AD_joystick_y_queue size = ", self.AD_joystick_y_queue.qsize())
                # erg = number * bigNumber
                # print(str(erg), end='\n')
                # print(time.time() - t0,end='\n')
        retval = proc.wait()
        err_thread.join()
        print('error:', err_buf.getvalue())

    # Funktion, welche den String einer Zeile aufteilt und die Werte zurück gibt
    def WorkWithValues(self, lineEntry):
        numStr = ''
        bigNumStr = ''
        voltStr = ''
        smallNumStr = ''
        code = ''
        state = 0
        numBlancs = 0
        for letter in lineEntry:
            if letter == ' ' and state < 3:
                continue
            elif letter == ' ':
                numBlancs += 1
                if numBlancs == 2:
                    state = 4
                continue

            if letter == '=':
                state = 1
                continue
            elif letter == ',':
                state = 2
                continue
            elif letter == '(':
                state = 3
                continue
            elif letter == 'V':
                state = 5
                continue

            if state == 0:
                numStr += letter
            elif state == 1:
                code += letter
            elif state == 2:
                bigNumStr += letter
            elif state == 3:
                voltStr += letter
            elif state == 4:
                smallNumStr += letter

        number = int(numStr)
        bigNumber = int(bigNumStr)
        voltage = float(voltStr)
        smallNumber = int(smallNumStr)
        # print(str(number) + "=" + code + ",   " + str(bigNumber) + " ( " + str(voltage) + " " + str(smallNumber) + " V) \n")
        return number, code, bigNumber, voltage, smallNumber

    def myPut(self, queue, element):
        QSIZE = 2
        if(queue.qsize() >= QSIZE):
            queue.queue.clear()
        queue.put(element)

    def myPut_size1(self, queue, element):
        QSIZE = 1
        if(queue.qsize() >= QSIZE):
            queue.queue.clear()
        queue.put(element)