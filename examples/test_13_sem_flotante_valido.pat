programa flotante_valido;

vars resultado : flotante;

flotante suma_float(a : flotante, b : flotante)
{
    vars r : flotante;
    {
        r = a + b;
        regresa r;
    }
};

inicio
{
    resultado = suma_float(3.0, 7.0);
    escribe(resultado);
}
fin
