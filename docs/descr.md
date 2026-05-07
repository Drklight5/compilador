Descripción del lenguaje 

<> -> Modulo
'' -> palabra reservada
id -> identificador alfanumérico libre para el usuario 
fin -> fin del programa (palabra reservada)
(salida) -> se termina el modulo
epsilon -> vacio


Se describe el diagrama de cómo funciona el lenguaje PATITO
En formato <MODULO> y a continuacion 
id de elemento . origen -> id de elemento. objetivo
Existen bucles y bypass

<PROGRAMA>

1. 'programa' -> 2. id
2. id → 3. ;
3. ; → 4. <VARS>
3. ; → 5. <FUNCS> 
3. ; -> 6. 'inicio'
4. <VARS> → 5. <FUNCS>
5. <FUNCS> → 6. inicio
5. <FUNCS> → 5. <FUNCS>
6. 'inicio' → 7. <CUERPO>
7. <CUERPO> → 8. fin

<VARS>
1. 'vars' → 2. id
2. id → 3. ,  
2. id → 4. :
3. , → 2. id
4. : → 5. <TIPO>
5. <TIPO> → 6. ;
6. ; → 2. id 
6. ; → (salida) 

<TIPO>
0. epsilon -> 1. 'entero'
0. epsilon -> 2. 'flotante'
1. 'entero' -> (salida)
2. 'flotante' -> (salida)

<CUERPO>
1. { -> 2. <ESTATUTO> 
1. { -> 3. }
2. <ESTATUTO>  -> 2. <ESTATUTO>
2. <ESTATUTO>  -> 3. }
3. } -> (salida)

<ESTATUTO>
0. epsilon -> 1. <ASIGNA>
0. epsilon -> 2. <CONDICION>
0. epsilon -> 3. <CICLO>
0. epsilon -> 4. <LLAMADA>
0. epsilon -> 6. <IMPRIME>
0. epsilon -> 7. [
1. <ASIGNA> -> (salida)
2. <CONDICION> -> (salida)
3. <CICLO> -> (salida)
4. <LLAMADA> ->  5. ;
5. ; -> (salida)
6.  <IMPRIME> -> (salida)
7. [ -> 8. <ESTATUTO>
7. [ -> 9. ]
8. <ESTATUTO> -> 9. ]
9. ] -> (salida)

<ASIGNA>
1. id   -> 2. =
2. = -> 3. <EXPRESION>
3. <EXPRESION> -> 4. ;
4. ;  ->  (salida)

<EXPRESION>
1. <EXP> -> (salida)
1. <EXP> -> 2. >
1. <EXP> -> 3. <
1. <EXP> -> 4. !=
1. <EXP> -> 5. ==
2. > -> 6. <EXP>
3. < -> 6. <EXP>
4. != -> 6. <EXP>
5. == -> 6. <EXP>
6. <EXP> -> (salida)

<IMPRIME>
1. 'escribe' -> 2. (
2. ( -> 3. <EXPRESION>
2. ( -> 4. 'letrero'
3. <EXPRESION> -> 5. ,
3. <EXPRESION> -> 6. )
4. 'letrero' -> 6. )
5. , -> 3. <EXPRESION>
6. ) -> 7. ;
7. ; -> (salida)

<CICLO>
1. 'mientras' -> 2. (
2. ( -> 3. <EXPRESION>
3. <EXPRESION> -> 4. )
4. ) -> 5. 'haz'
5. 'haz' -> 6. <CUERPO> 
6. <CUERPO> -> 7. ;
7. ; -> (salida)

<CONDICION>
1. 'si' -> 2. ( 
2. ( -> 3. <EXPRESION>
3. <EXPRESION> -> 4. ) 
4. ) -> 5. <CUERPO>
5. <CUERPO> -> 8. ;
5. <CUERPO> -> 6. 'sino'
6. 'sino' -> 7. <CUERPO>
7. <CUERPO> -> 8. ;
8. ; -> (salida)


<FACTOR>
0. epsilon -> 1. (
0. epsilon -> 2. +
0. epsilon -> 3. - 
0. epsilon -> 7. id
0. epsilon -> 8. <CTE>
0. epsilon -> 4. <LLAMADA>
1. ( -> 5. <EXPRESION>
2. + -> 7. id
2. + -> 8. <CTE>
3. -  -> 7. id
3. -  -> 8. <CTE>
4. <LLAMADA> -> (salida)
5. <EXPRESION> -> 6. )
6. ) -> (salida)
7. id -> (salida)
8. <CTE> -> (salida)

<TERMINO> 
1. <FACTOR> -> (salida)
1. <FACTOR> -> 2. *
1. <FACTOR> -> 3. /
2. * -> 1. <FACTOR>
3. /  -> 1. <FACTOR>


<LLAMADA>
1. id -> 2. (
2. ( -> 3. <EXPRESION>
2. ( -> 5. )
3. <EXPRESION> -> 4. ,
3. <EXPRESION> -> 5. )
4. , -> 3. <EXPRESION>
5. ) -> (salida)

<EXP>
1. <TERMINO> -> (salida)
1. <TERMINO> -> 2. +
1. <TERMINO> -> 2. -
2. + -> 1. <TERMINO> 
2. - -> 1. <TERMINO> 

<CTE>
Notas, es cualquier constante numérica
0. epsilon -> 1. cte_ent
0. epsilon -> 2. cte_flot
1. cte_ent -> (salida)
1. cte_flot -> (salida)

<FUNCS>
0. epsilon -> 1. 'nula'
0. epsilon -> 2. <TIPO>
1. 'nula' -> 3. id
2. <TIPO> -> 3. id
3. id -> 4. (
4. ( -> 5. )
4. ( -> 6. id
6. id -> 7. :
7. : -> 8. <TIPO>
8. <TIPO> -> 9. ,
8. <TIPO> -> 5. )
9. , -> 6. id
5. ) -> 10. {
10. { -> 11. <VARS>
11. <VARS>  -> 12. <CUERPO>
12. <CUERPO> -> 13. }
13. } -> 14. ;
14. ; -> (salida)

<LLAMADA>
1. id -> 2. (
2. ( -> 3. <EXPRESION
2. ( -> 5. )
3. <EXPRESION> -> 4. ,
3. <EXPRESION> -> 5. )
4. , -> 3. <EXPRESION>
5. ) -> (salida)