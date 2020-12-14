import threading as th
import time
import keyboard

keep_going = True
def key_capture_thread():
    global keep_going
    a = keyboard.read_key()
    if a == "esc":
        keep_going = False


def do_stuff():
    th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()
    i=0
    while keep_going:
        print('still going...')
        time.sleep(1)
        i=i+1
        print (i)
    print ("Schleife beendet")


do_stuff()