from structures.stack import Stack
def test_stack():
    print("===== TESTS STACK =====")

    # Test 1: push y pop
    s = Stack()
    s.push(10)
    s.push(20)
    result = s.pop()
    print("Test 1: push y pop \t", "PASS" if result == 20 else "FAIL")

    # Test 2: peek
    s.push(5)
    result = s.peek()
    print("Test 2: peek \t\t", "PASS" if result == 5 else "FAIL")

    # Test 3: pop en vacío
    s = Stack()
    result = s.pop()
    print("Test 3: pop en vacío \t", "PASS" if result is None else "FAIL")

    # Test 4: size
    s.push(1)
    s.push(2)
    result = s.size()
    print("Test 4: size \t\t", "PASS" if result == 2 else "FAIL")

    # Test 5: is_empty
    s = Stack()
    result = s.is_empty()
    print("Test 5: is_empty \t", "PASS" if result is True else "FAIL")

    print()