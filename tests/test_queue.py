from structures.queue import Queue

def test_queue():
    print("===== TESTS QUEUE =====")

    # Test 1: enqueue y dequeue
    q = Queue()
    q.enqueue(10)
    q.enqueue(20)
    result = q.dequeue()
    print("Test 1: enqueue/dequeue ", "PASS" if result == 10 else "FAIL")

    # Test 2: front
    result = q.front()
    print("Test 2: front \t\t", "PASS" if result == 20 else "FAIL")

    # Test 3: dequeue en vacío
    q = Queue()
    result = q.dequeue()
    print("Test 3: dequeue en vacío", "PASS" if result is None else "FAIL")

    # Test 4: front en vacío
    result = q.front()
    print("Test 4: front en vacío \t", "PASS" if result is None else "FAIL")

    # Test 5: size
    q.enqueue(1)
    q.enqueue(2)
    result = q.size()
    print("Test 5: size \t\t", "PASS" if result == 2 else "FAIL")

    # Test 6: is_empty
    q = Queue()
    result = q.is_empty()
    print("Test 6: is_empty \t", "PASS" if result is True else "FAIL")

    # Test 7: orden FIFO correcto
    q.enqueue(100)
    q.enqueue(200)
    q.enqueue(300)
    first = q.dequeue()
    second = q.dequeue()
    print("Test 7: FIFO \t\t", "PASS" if first == 100 and second == 200 else "FAIL")

    print()