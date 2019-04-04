import threading, time


def _start_thread(f, *args):
    t = threading.Thread(target=f, args=args)
    t.start()
    return t


lock = threading.Lock()


def client(num):
    with lock:
        print(num)
        time.sleep(2)


def task4_1():
    threads = []
    
    for num in range(3):
        threads.append(_start_thread(client, num))
    
    for thread in threads:
        thread.join()


border_open = threading.Event()
border_gate = threading.Condition()


def tourist(num):
    border_open.set()
    with border_gate:
        print(num)
    border_open.clear()


def border_guard():
    border_open.set()

    for _ in range(3):
        border_gate.notify()
        time.sleep(1)

    border_gate.notify_all()


def task4_2():
    threads = []
    
    for num in range(6):
        threads.append(_start_thread(tourist, num))
    time.sleep(3)
    threads.append(_start_thread(border_guard))
    
    for thread in threads:
        thread.join()


_client = threading.Semaphore(3)


def client_2(num):
    with _client:
        print(num)
        time.sleep(num * .5)


def task4_3():
    threads = []

    for num in range(9):
        threads.append(_start_thread(client_2, num))
    
    for thread in threads:
        thread.join()


def border_guard_2():
    time.sleep(4)
    border_open.set()
    time.sleep(2)
    border_open.clear()
    time.sleep(4)
    border_open.set()


def task4_4():
    threads = []

    threads.append(_start_thread(border_guard))
    
    for num in range(9):
        threads.append(_start_thread(tourist, num))
        time.sleep(1)
    
    
    for thread in threads:
        thread.join()


ride = threading.BoundedSemaphore(5)


def roller_coaster(num):
    ride.acquire(timeout=4)
    print(num)
    ride.release()


def task4_5():
    threads = []
    for num in range(20):
        threads.append(_start_thread(roller_coaster, num))
        time.sleep(.5)

    for num in range(20, 30):
        threads.append(_start_thread(roller_coaster, num))
        time.sleep(1)

    for num in range(30, 35):
        threads.append(_start_thread(roller_coaster, num))
        time.sleep(2)

    for thread in threads:
        thread.join()
