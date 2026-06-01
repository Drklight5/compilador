import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from semantic.semantic_cube import TYPES


# ── Rangos de segmentos ───────────────────────────────────────────────────
#
#  Segmento          Tipo       Rango
#  -----------------+-----------+-----------
#  Global            entero     1000 - 1999
#  Global            flotante   2000 - 2999
#  Local             entero     3000 - 3999
#  Local             flotante   4000 - 4999
#  Temporal          entero     5000 - 5999
#  Temporal          flotante   6000 - 6999
#  Temporal          bool       7000 - 7999
#  Constante         entero     8000 - 8999
#  Constante         flotante   9000 - 9999
#  Constante         string     10000 - 10999
#  Retorno func.     entero     11000 - 11499
#  Retorno func.     flotante   11500 - 11999
# ─────────────────────────────────────────────────────────────────────────

GLOBAL_INT_BASE    = 1000
GLOBAL_FLOAT_BASE  = 2000
LOCAL_INT_BASE     = 3000
LOCAL_FLOAT_BASE   = 4000
TEMP_INT_BASE      = 5000
TEMP_FLOAT_BASE    = 6000
TEMP_BOOL_BASE     = 7000
CONST_INT_BASE     = 8000
CONST_FLOAT_BASE   = 9000
CONST_STR_BASE     = 10000
RETURN_INT_BASE    = 11000
RETURN_FLOAT_BASE  = 11500


class VirtualMemory:
    def __init__(self):
        self._counters = {
            ('global', TYPES.INT):   GLOBAL_INT_BASE,
            ('global', TYPES.FLOAT): GLOBAL_FLOAT_BASE,
            ('local',  TYPES.INT):   LOCAL_INT_BASE,
            ('local',  TYPES.FLOAT): LOCAL_FLOAT_BASE,
            ('temp',   TYPES.INT):   TEMP_INT_BASE,
            ('temp',   TYPES.FLOAT): TEMP_FLOAT_BASE,
            ('temp',   TYPES.BOOL):  TEMP_BOOL_BASE,
            ('return', TYPES.INT):   RETURN_INT_BASE,
            ('return', TYPES.FLOAT): RETURN_FLOAT_BASE,
        }

        # Tablas de constantes: valor → dirección
        self._const_int   = {}
        self._const_float = {}
        self._const_str   = {}
        self._const_int_ctr   = CONST_INT_BASE
        self._const_float_ctr = CONST_FLOAT_BASE
        self._const_str_ctr   = CONST_STR_BASE

        # Mapa inverso: dirección → (símbolo, tipo, valor)
        self._addr_info = {}

    # ── Asignación de dirección ──────────────────────────────────────

    def next_address(self, segment, var_type, name=None):
        """
        Asigna la siguiente dirección disponible en (segment, var_type).
        segment: 'global' | 'local' | 'temp' | 'return'
        """
        key = (segment, var_type)
        if key not in self._counters:
            raise Exception(f'Segmento desconocido: {segment}, {var_type}')
        addr = self._counters[key]
        self._counters[key] += 1
        if name:
            self._addr_info[addr] = (name, var_type)
        return addr

    # ── Constantes ───────────────────────────────────────────────────

    def get_constant(self, value, const_type):
        """Regresa la dirección de una constante (crea si no existe)."""
        if const_type == TYPES.INT:
            if value not in self._const_int:
                addr = self._const_int_ctr
                self._const_int[value] = addr
                self._const_int_ctr += 1
                self._addr_info[addr] = (str(value), const_type)
            return self._const_int[value]

        elif const_type == TYPES.FLOAT:
            if value not in self._const_float:
                addr = self._const_float_ctr
                self._const_float[value] = addr
                self._const_float_ctr += 1
                self._addr_info[addr] = (str(value), const_type)
            return self._const_float[value]

        elif const_type == TYPES.STRING:
            if value not in self._const_str:
                addr = self._const_str_ctr
                self._const_str[value] = addr
                self._const_str_ctr += 1
                self._addr_info[addr] = (value, const_type)
            return self._const_str[value]

        raise Exception(f'Tipo de constante desconocido: {const_type}')

    # ── Reset de segmentos ───────────────────────────────────────────

    def reset_local(self):
        """Reinicia contadores locales para una nueva función."""
        self._counters[('local', TYPES.INT)]   = LOCAL_INT_BASE
        self._counters[('local', TYPES.FLOAT)] = LOCAL_FLOAT_BASE

    def reset_temps(self):
        """Reinicia contadores de temporales para un nuevo scope."""
        self._counters[('temp', TYPES.INT)]   = TEMP_INT_BASE
        self._counters[('temp', TYPES.FLOAT)] = TEMP_FLOAT_BASE
        self._counters[('temp', TYPES.BOOL)]  = TEMP_BOOL_BASE

    # ── Consultas ────────────────────────────────────────────────────

    def get_name(self, addr):
        info = self._addr_info.get(addr)
        return info[0] if info else str(addr)

    def get_constants_table(self):
        """Lista de (dirección, tipo, valor) para todas las constantes."""
        rows = []
        for val, addr in self._const_int.items():
            rows.append((addr, 'entero', val))
        for val, addr in self._const_float.items():
            rows.append((addr, 'flotante', val))
        for val, addr in self._const_str.items():
            rows.append((addr, 'string', val))
        return sorted(rows)

    def segment_of(self, addr):
        """Regresa el nombre del segmento al que pertenece una dirección."""
        if GLOBAL_INT_BASE   <= addr < GLOBAL_FLOAT_BASE:  return 'global int'
        if GLOBAL_FLOAT_BASE <= addr < LOCAL_INT_BASE:     return 'global float'
        if LOCAL_INT_BASE    <= addr < LOCAL_FLOAT_BASE:   return 'local int'
        if LOCAL_FLOAT_BASE  <= addr < TEMP_INT_BASE:      return 'local float'
        if TEMP_INT_BASE     <= addr < TEMP_FLOAT_BASE:    return 'temp int'
        if TEMP_FLOAT_BASE   <= addr < TEMP_BOOL_BASE:     return 'temp float'
        if TEMP_BOOL_BASE    <= addr < CONST_INT_BASE:     return 'temp bool'
        if CONST_INT_BASE    <= addr < CONST_FLOAT_BASE:   return 'const int'
        if CONST_FLOAT_BASE  <= addr < CONST_STR_BASE:     return 'const float'
        if CONST_STR_BASE    <= addr < RETURN_INT_BASE:    return 'const string'
        if RETURN_INT_BASE   <= addr < RETURN_FLOAT_BASE:  return 'return int'
        if RETURN_FLOAT_BASE <= addr < 12000:              return 'return float'
        return 'unknown'
