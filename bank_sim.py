import threading
import time
import random
from collections import deque
#Global variables
num_tellers = 3
num_customers = 50

bank_open = threading.Event()          # bank opens when all tellers are ready
door_sem = threading.Semaphore(2)      # only two customers can enter at once
safe_sem = threading.Semaphore(2)      # only two tellers can be in the safe
manager_sem = threading.Semaphore(1)   # only one teller can talk to manager

queue_lock = threading.Lock()
customer_available = threading.Condition(lock=queue_lock)
waiting_queue = deque()

served_count = 0
served_count_lock = threading.Lock()

# per-customer semaphores
assigned_sem = {}
introduced_sem = {}
teller_ask_sem = {}
told_sem = {}
transaction_done_sem = {}
customer_left_sem = {}

# thread-safe print
print_lock = threading.Lock()
def write_log(msg):
    with print_lock:
        print(msg)

# store customer transaction type and assigned teller
assigned_teller = {}
customer_transaction = {}

# initialize per-customer semaphores
for i in range(num_customers):
    assigned_sem[i] = threading.Semaphore(0)
    introduced_sem[i] = threading.Semaphore(0)
    teller_ask_sem[i] = threading.Semaphore(0)
    told_sem[i] = threading.Semaphore(0)
    transaction_done_sem[i] = threading.Semaphore(0)
    customer_left_sem[i] = threading.Semaphore(0)

# track how many tellers are ready
teller_ready_count = 0
teller_ready_lock = threading.Lock()

#  Teller Thread method
def teller_thread(tid):
    global teller_ready_count, served_count

    write_log(f"Teller {tid} []: ready to serve")
    write_log(f"Teller {tid} []: waiting for a customer")

    # increment ready count and possibly open bank
    with teller_ready_lock:
        teller_ready_count += 1
        if teller_ready_count == num_tellers:
            bank_open.set()

    # teller loop (queues and handles customers)
    while True:
        with customer_available:
            while len(waiting_queue) == 0:
                with served_count_lock:
                    if served_count >= num_customers:
                        write_log(f"Teller {tid} []: leaving for the day")
                        return
                customer_available.wait(timeout=0.1)

            cid = waiting_queue.popleft()
            assigned_teller[cid] = tid
            assigned_sem[cid].release()

        # start handling customer
        write_log(f"Teller {tid} [Customer {cid}]: serving a customer")
        write_log(f"Teller {tid} [Customer {cid}]: asks for transaction")

        introduced_sem[cid].acquire()
        teller_ask_sem[cid].release()
        told_sem[cid].acquire()

        trans = customer_transaction[cid]

        # withdrawal
        if trans == "withdrawal":
            write_log(f"Teller {tid} [Customer {cid}]: handling withdrawal transaction")

            write_log(f"Teller {tid} [Customer {cid}]: going to the manager")
            manager_sem.acquire()

            ms = random.randint(5, 30)
            write_log(f"Teller {tid} [Customer {cid}]: getting manager's permission")
            write_log(f"Teller {tid} [Customer {cid}]: manager interaction starts ({ms} ms)")
            time.sleep(ms / 1000)
            write_log(f"Teller {tid} [Customer {cid}]: got manager's permission")

            manager_sem.release()

            write_log(f"Teller {tid} [Customer {cid}]: going to safe")
            safe_sem.acquire()
            write_log(f"Teller {tid} [Customer {cid}]: enter safe")

            ms2 = random.randint(10, 50)
            write_log(f"Teller {tid} [Customer {cid}]: performing transaction in safe ({ms2} ms)")
            time.sleep(ms2 / 1000)

            write_log(f"Teller {tid} [Customer {cid}]: leaving safe")
            safe_sem.release()

            write_log(f"Teller {tid} [Customer {cid}]: finishes withdrawal transaction.")
            write_log(f"Teller {tid} [Customer {cid}]: wait for customer to leave.")

        # deposit
        else:
            write_log(f"Teller {tid} [Customer {cid}]: handling deposit transaction")

            write_log(f"Teller {tid} [Customer {cid}]: going to safe")
            safe_sem.acquire()
            write_log(f"Teller {tid} [Customer {cid}]: enter safe")

            ms2 = random.randint(10, 50)
            write_log(f"Teller {tid} [Customer {cid}]: performing transaction in safe ({ms2} ms)")
            time.sleep(ms2 / 1000)

            write_log(f"Teller {tid} [Customer {cid}]: leaving safe")
            safe_sem.release()

            write_log(f"Teller {tid} [Customer {cid}]: finishes deposit transaction.")
            write_log(f"Teller {tid} [Customer {cid}]: wait for customer to leave.")

        # notify customer transaction is finished
        transaction_done_sem[cid].release()
        # wait for customer to leave teller
        customer_left_sem[cid].acquire()

        # teller is ready again
        with served_count_lock:
            served_count += 1
            write_log(f"Teller {tid} []: ready to serve")
            write_log(f"Teller {tid} []: waiting for a customer")

            if served_count >= num_customers:
                with customer_available:
                    customer_available.notify_all()

# Customer Thread method
def customer_thread(cid):
    # randomly choose transaction type
    trans = random.choice(["deposit", "withdrawal"])
    customer_transaction[cid] = trans
    write_log(f"Customer {cid} []: wants to perform a {trans} transaction")

    # arrival delay 0–100 ms
    time.sleep(random.randint(0, 100) / 1000)

    bank_open.wait()

    write_log(f"Customer {cid} []: going to bank.")
    write_log(f"Customer {cid} []: entering bank.")
    door_sem.acquire()

    write_log(f"Customer {cid} []: getting in line.")
    write_log(f"Customer {cid} []: selecting a teller.")

    with customer_available:
        waiting_queue.append(cid)
        customer_available.notify()

    assigned_sem[cid].acquire()
    tid = assigned_teller[cid]

    write_log(f"Customer {cid} [Teller {tid}]: selects teller")
    write_log(f"Customer {cid} [Teller {tid}] introduces itself")

    introduced_sem[cid].release()

    teller_ask_sem[cid].acquire()
    write_log(f"Customer {cid} [Teller {tid}]: asks for {trans} transaction")
    told_sem[cid].release()

    transaction_done_sem[cid].acquire()
    write_log(f"Customer {cid} [Teller {tid}]: leaves teller")

    write_log(f"Customer {cid} []: goes to door")
    write_log(f"Customer {cid} []: leaves the bank")

    customer_left_sem[cid].release()
    door_sem.release()

# main method
def main():

    #Threads created
    tellers = []
    for t in range(num_tellers):
        th = threading.Thread(target=teller_thread, args=(t,))
        th.start()
        tellers.append(th)

    customers = []
    for c in range(num_customers):
        th = threading.Thread(target=customer_thread, args=(c,))
        th.start()
        customers.append(th)

    # waits for threads to finish
    for th in customers:
        th.join()

    for th in tellers:
        th.join()

    write_log("The bank closes for the day.")

if __name__ == "__main__":
    main()

