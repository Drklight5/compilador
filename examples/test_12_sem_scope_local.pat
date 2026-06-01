programa scope_local;

vars x : entero;

nula foo(x : entero)
{
    {
        escribe(x);
    }
};

inicio
{
    x = 100;
    foo(42);
    escribe(x);
}
fin
