#!/usr/bin/python3
from tkinter import *
import threading
import queue

import multiple 


def __simulation_thread__(__queue):

    sim = None
    timeout = 200

    while True:

        try:
            msg = __queue.get(False, timeout)

        except queue.Empty:
            msg = None

        if msg:
            print(msg)
            if msg['cmd'] == 'quit':
                print('quit!')
                return

            elif msg['cmd'] == 'start':
                print('start simulation!')
                sim = multiple.simulation(True, None, msg['speed_up'].get())
                timeout = 0

            elif msg['cmd'] == 'stop': 
                print('stop simulation!')
                sim = None
                timeout = 200

        if sim:
            next(sim)


class Gui(object):

    
    def __init__(self, master):

        self.__master = master
        frame = Frame(master)
        frame.pack()

        self.__queue = queue.Queue(maxsize=1)

        label = Label(frame, text="Velocidad:")
        label.grid(row=0, column=1)

        self.__speed_up = IntVar(master)
        self.__speed_up.set(1)

        speed_menu = OptionMenu(frame, self.__speed_up, 1, 2, 3, 4, 5, 6)
        speed_menu.grid(row=0, column=2)

        button = Button(frame,
                        text="Empezar simulación",
                        command=self.__start)
        button.grid(row=1, column=0)

        button = Button(frame,
                        text="Terminar simulación",
                        command=self.__stop)
        button.grid(row=1, column=1)

        button = Button(frame,
                        text="Salir",
                        command=self.__quit)
        button.grid(row=1, column=2)

        threading.Thread(target=__simulation_thread__, args=(self.__queue,)).start()


    def __start(self):
        self.__queue.put({'cmd': 'start', 'speed_up': self.__speed_up})


    def __stop(self):
        self.__queue.put({'cmd': 'stop'})


    def __quit(self):
        self.__queue.put({'cmd': 'quit'})
        self.__master.destroy() 


if __name__ == '__main__':
    root = Tk()
    app = Gui(root)

    mainloop()
