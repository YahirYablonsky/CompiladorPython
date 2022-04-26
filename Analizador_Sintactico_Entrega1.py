# Para ejecutar
# [.....]\tp\venv\Scripts> python ..\..\src\Analizador_Sintactico_TP2.py
import ply.yacc as yacc
import os
from Analizador_Lexico_TP import tokens
from Analizador_Lexico_TP import analizador
PATH_PRUEBAS = os.path.dirname(os.path.abspath(__file__)) + '\Pruebas'

#PASO 1. DEFINO LA PRECEDENCIA DE LOS OPERADORES
precedence = (
    ('right','ASSIGN'),
    ('left','NE','EQUAL'),
    ('left','LT','LTE','GT','GTE'),
    ('left','PLUS','MINUS'),
    ('left','MULT','DIVIDE','REST'),
    ('left','LBRA','RBRA'),
    ('left','COMMA')
    )
#PASO 2. DEFINO LA LISTA DE VARIABLES Y EL RESULTADO DE LA GRAMÁTICA
variables = {}
resultado_gramatica = []
reglas_aplicadas = []
tabla_simbolos = {}

def armar_tabla(nombre, tipo, valor):
    tipo='-'
    valor = valor if(valor) else '-'
    tabla_simbolos[nombre]={'tipo':tipo, 'valor':valor}

#PASO 3. DEFINO LA GRAMÁTICA

#START VA A SER "PROGRAM"
def p_program(p):
    ''' program : bloque'''
    reglas_aplicadas.append('Entro en Regla 01: P->B')

#UN BLOQUE ES UN CONJUNTO DE SENTENCIAS O UNA SENTENCIA
def p_bloque(p):
    ''' bloque : lista_sentencias'''
    reglas_aplicadas.append('Entro en Regla 02: B-> LS')
   
def p_lista_sentencias_1(p):
    ''' lista_sentencias : lista_sentencias  sentencia ENDL'''
    reglas_aplicadas.append("Entro en Regla 03: LS -> LS S ;")

def p_lista_sentencias_2(p):
    ''' lista_sentencias : sentencia ENDL'''
    reglas_aplicadas.append("Entro en Regla 04: LS -> S ;")

#UNA SENTENCIA ES: UNA SENT_WHILE, SENT_ASIG, SENT_COND, SENT_DECL, SENT_WRITE, SENT_READ
def p_sentencia_1(p):
    ''' sentencia : sentencia_asig
    |               sentencia_cond         
    |               sentencia_while
    |               sentencia_decl
    |               sentencia_write
    |               sentencia_read
    ''' 
    reglas_aplicadas.append("Entro en Regla 05-10: S -> SW SC SD SA")

#GRAMATICA DE ASIGNACION
def p_setencia_asig(p):
    ''' sentencia_asig : ID ASSIGN expresion'''
    reglas_aplicadas.append("Entro en Regla 11: SA -> ID := E")
    armar_tabla(p[1], '', '') #################<-------------#################

def p_expresion(p):
    ''' expresion : expresion op_arit termino'''
    reglas_aplicadas.append("Entro en Regla 12: E -> E OP T")

def p_expresion_ter(p):
    ''' expresion : termino'''
    reglas_aplicadas.append("Entro en Regla 13: E -> T")

def p_op_arit(p):
    ''' op_arit : PLUS 
    |             MINUS 
    |             MULT 
    |             DIVIDE 
    |             REST
    '''
    reglas_aplicadas.append("Entro en Regla 14-18: OP -> + |- | / | * | %")

def p_termino_id(p):
    ''' termino : ID '''
    reglas_aplicadas.append("Entro en Regla 19: T-> ID")
    armar_tabla(p[1], '', '') #################<-------------#################

def p_termino_const(p):
    ''' termino : INTEGER 
    |             FLOATD
              '''
    reglas_aplicadas.append("Entro en Regla 20-21: T-> ID")
    armar_tabla('_'+str(p[1]), '', p[1]) #################<-------------#################

def p_termino_expr(p):
    ''' termino : LBRA expresion RBRA '''
    reglas_aplicadas.append("Entro en Regla 22: T-> (E)")    

#GRAMATICA DE CONDICIÓN
def p_setencia_cond(p):
    ''' sentencia_cond : IF condicion OP_BRA lista_sentencias CL_BRA'''
    reglas_aplicadas.append('''Entro en Regla 23: SC -> IF C { LS }''' )

def p_setencia_cond_else(p):
    ''' sentencia_cond : IF condicion OP_BRA lista_sentencias CL_BRA ELSE OP_BRA lista_sentencias CL_BRA'''
    reglas_aplicadas.append('''Entro en Regla 24: SC -> IF C { LS }  ELSE { LS }''' )

def p_condicion(p): 
    ''' condicion : expresion op_logico termino'''
    reglas_aplicadas.append('''Entro en Regla 25: C -> E OP_L T''' )

def p_condicion_par(p): 
    ''' condicion : LBRA condicion RBRA'''
    reglas_aplicadas.append('''Entro en Regla 26: C -> (E OP_L T)''' )

def p_condicion_par_and(p): 
    ''' condicion : condicion AND condicion'''
    reglas_aplicadas.append('''Entro en Regla 27: C -> C AND C''' )

def p_condicion_par_or(p): 
    ''' condicion : condicion OR condicion'''
    reglas_aplicadas.append('''Entro en Regla 28: C -> C OR C''' )

def p_op_logico(p):
    ''' op_logico : NE 
    | LT 
    | LTE
    | GT 
    | GTE 
    | EQUAL
    '''
    reglas_aplicadas.append('''Entro en Regla 29-34: OP_L -> NE | LT | LTE | GT | GTE | EQUAL''' )

#GRAMATICA DE WHILE
def p_sentencia_while(p):
    ''' sentencia_while : WHILE condicion OP_BRA lista_sentencias CL_BRA'''
    reglas_aplicadas.append('Entro en Regla 35: SW -> WHILE C { LS } ' )

#GRAMATICA DE DECLARACION
def p_sentencia_declaracion(p):
    ''' sentencia_decl : DECVAR lista_declaraciones ENDDEC'''
    reglas_aplicadas.append('''Entro en Regla 36: SD -> DECVAR LD ENDDEC ''' )

def p_lista_declaraciones_1(p):
    ''' lista_declaraciones : lista_declaraciones  declaracion'''
    reglas_aplicadas.append('''Entro en Regla 37: LD -> LD ; D ''' )

def p_lista_declaraciones_2(p):
    ''' lista_declaraciones : declaracion  '''
    reglas_aplicadas.append('''Entro en Regla 38: LD -> D ''' )


def p_declaracion(p):
    ''' declaracion : lista_id COLON tipo_dato ENDL'''
    reglas_aplicadas.append('''Entro en Regla 39: D -> LI COLON TIPO ENDL''' )


def p_lista_id1(p):
    ''' lista_id : lista_id COMMA ID '''
    reglas_aplicadas.append('''Entro en Regla 40: LI -> LI , ID ''' )
    armar_tabla(p[3], '', '') #################<-------------#################

def p_lista_id2(p):
    ''' lista_id : ID '''
    reglas_aplicadas.append('''Entro en Regla 41: LI -> ID ''' )
    armar_tabla(p[1], '', '') #################<-------------#################


def p_tipo_dato(p):
    ''' tipo_dato : FLOAT 
    | STRING 
    | INT 
    '''
    reglas_aplicadas.append('''Entro en Regla 42-44: tipo_dato -> FLOAT | STRING | INT''' )

#GRAMATICAS DE LECTURA Y ESCRITURA

def p_sentencia_write1 (p):
    ''' sentencia_write : WRITE cte '''
    reglas_aplicadas.append('''Entro en Regla 45: SWRT -> WRITE cte ''' )

def p_sentencia_write2 (p):
    ''' sentencia_write : WRITE ID '''
    reglas_aplicadas.append('''Entro en Regla 46: SWRT -> WRITE ID ''' )

def p_sentencia_read (p):
    ''' sentencia_read : READ ID '''
    reglas_aplicadas.append('''Entro en Regla 47: SRD -> READ ID ''' )

def p_cte (p):
    ''' cte : FLOATD
    |         INTEGER
    |         STRINGD'''
    reglas_aplicadas.append('''Entro en Regla 48-50: CTE -> INTEGER | FLOATD | STRINGD''' )
    armar_tabla('_'+str(p[1]), '', p[1]) #################<-------------#################

    
#GRAMATICAS FUNCIONES TAKE Y BETWEEN
def p_condicion_between1(p):
    ''' condicion_between : BETWEEN LBRA ID COMMA tupla RBRA '''
    reglas_aplicadas.append('''Entro en Regla 51: CD_BTW -> BETWEEN ( tupla ) ''' )

def p_tupla(p):
    ''' tupla :  OP_BRC expresion ENDL expresion CL_BRC '''
    reglas_aplicadas.append('''Entro en Regla 52: tupla -> [E;E] ''' )

def p_condicion_between2(p):
    ''' condicion : condicion_between '''
    reglas_aplicadas.append('''Entro en Regla 53: E -> EX_BTW''' )

def p_expresion_take1(p):
    ''' expresion : expresion_take '''
    reglas_aplicadas.append('''Entro en Regla 54: E -> EX_TK''' )

def p_expresion_take2(p):
    ''' expresion_take : TAKE LBRA op_arit ENDL INTEGER ENDL OP_BRC lista_take CL_BRC RBRA '''
    reglas_aplicadas.append('''Entro en Regla 55: EX_TK -> TAKE (op_arit ; INTEGER ; [LS_TK])''' )

def p_lista_take1(p):
    ''' lista_take : lista_take ENDL cte_take  '''
    reglas_aplicadas.append('''Entro en Regla 56: LS_TK -> LS_TK ; CTE_TK''' )

def p_lista_take2(p):
    ''' lista_take : cte_take  '''
    reglas_aplicadas.append('''Entro en Regla 57: LS_TK -> CTE_TK''' )


def p_cte_take2(p):
    ''' cte_take : INTEGER
    |              FLOATD  '''
    reglas_aplicadas.append('''Entro en Regla 58-59: CTE_TK -> INTEGER | FLOATD''' )
    armar_tabla('_'+str(p[1]), '', p[1]) #################<-------------#################




def p_error(t):
    global resultado_gramatica
    if t:
        resultado = "Error sintactico:\n Token: {}\n Valor: {}\n linea:{}".format(  str(t.type),str(t.value), str(t.lexer.lineno))
        print(resultado)
    else:
        resultado = "Error sintactico {}".format(t)
        print('Inesperado cierre de sentencia')
    resultado_gramatica.append(resultado)


# instanciamos el analizador sistactico
parser = yacc.yacc()

def prueba_sintactica(data):
    global resultado_gramatica
    resultado_gramatica.clear()
    if data:
        gram = parser.parse(data)
        if gram:
            resultado_gramatica.append(str(gram))
    else: print("data vacia")

    return resultado_gramatica

if __name__ == '__main__':
    
    inputFile = open(PATH_PRUEBAS + '\Prueba.in','r')
    outputFile = open(PATH_PRUEBAS + '\Prueba.out','w')
    file = ''
    while True:
        linea = inputFile.read() 
        if not linea:
            break   
        file = file + linea
        prueba_sintactica(file)
        for regla in reglas_aplicadas:
            print (regla)
            outputFile.write(regla + "\n")

    outputFile.close()       
    inputFile.close()

    table_file = open(PATH_PRUEBAS + '\_ts.txt','w')
    line = 'NOMBRE,TIPO,VALOR'
    table_file.write(line + "\n")
    for i in tabla_simbolos:
        line = str(i)+','+str(tabla_simbolos[i]['tipo'])+','+str(tabla_simbolos[i]['valor'])
        table_file.write(line + "\n")
    table_file.close()   
    