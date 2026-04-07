from structures.hash_table import HashTable

def test_hash_table():
    print("===== TESTS HASH TABLE =====")

    h = HashTable()

    # Test 1: put y get
    h.put("x", 10)
    result = h.get("x")
    print("Test 1: put/get\t\t", "PASS" if result == 10 else "FAIL")

    # Test 2: overwrite
    h.put("x", 20)
    result = h.get("x")
    print("Test 2: overwrite \t", "PASS" if result == 20 else "FAIL")

    # Test 3: key inexistente
    result = h.get("y")
    print("Test 3: key inexistente ", "PASS" if result is None else "FAIL")

    # Test 4: remove
    h.put("z", 50)
    h.remove("z")
    result = h.get("z")
    print("Test 4: remove \t\t", "PASS" if result is None else "FAIL")

    # Test 5: contains
    h.put("a", 1)
    result = h.contains("a")
    print("Test 5: contains \t", "PASS" if result is True else "FAIL")

    # Test 6: size
    result = h.size()
    print("Test 6: size \t\t", "PASS" if result == 2 else "FAIL")

    # Test 7: is_empty
    h = HashTable()
    result = h.is_empty()
    print("Test 7: is_empty \t", "PASS" if result is True else "FAIL")

    print()