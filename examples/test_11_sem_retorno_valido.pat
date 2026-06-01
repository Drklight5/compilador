programa retorno_valido;

vars resultado : entero;

entero doble(x : entero)
{
    vars r : entero;
    {
        r = x + x;
        regresa r;
    }
};

inicio
{
    resultado = doble(5);
    escribe(resultado);
}
fin
