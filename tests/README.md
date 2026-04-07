# Test Cases
## Stack
1. push(10), push(20), pop() = 20
2. push(5), peek() = 5
3. pop() en vacío = None
4. size() después de insertar = correcto
5. is_empty() en pila nueva =  True

## Queue
1. enqueue(10), enqueue(20), dequeue() = 10
2. front() = 20 (siguiente elemento en la cola)
3. dequeue() en cola vacía = None
4. front() en cola vacía = None
5. enqueue(1), enqueue(2), size() = 2
6. is_empty() en cola vacía = True
7. enqueue(100), enqueue(200), enqueue(300), dequeue(), dequeue() = 100, 200 (orden FIFO correcto)

## Hash Table
1. put("x",10), get("x") = 10  
2. put("x",20), get("x") = 20 (sobrescritura correcta)  
3. get("y") (clave inexistente) = None  
4. put("z",50), remove("z"), get("z") = None  
5. put("a",1), contains("a") = True  
6. size() = número correcto de elementos  
7. is_empty() en tabla vacía = True  