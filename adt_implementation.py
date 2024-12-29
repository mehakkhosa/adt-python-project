"""fp2"""

""" 2.1.1 - TAD gerador"""
# •Construtores


def cria_gerador(b, s):
    if s <= 0 or not isinstance(s, int) or type(b) != int or (b != 32 and b != 64):
        raise ValueError('cria gerador: argumentos invalidos')
    return [b, s]


def cria_copia_gerador(g):
    g_copy = g
    return g_copy


def obtem_estado(g):                          # •Seletores
    return g[1]


# •Modificadores


def define_estado(g, s):
    g[1] = s
    return s


def atualiza_estado(g):
    if g[0] == 32:
        g[1] ^= (g[1] << 13) & 0xFFFFFFFF
        g[1] ^= (g[1] >> 17) & 0xFFFFFFFF
        g[1] ^= (g[1] << 5) & 0xFFFFFFFF
        return g[1]
    if g[0] == 64:
        g[1] ^= (g[1] << 13) & 0xFFFFFFFFFFFFFFFF
        g[1] ^= (g[1] >> 7) & 0xFFFFFFFFFFFFFFFF
        g[1] ^= (g[1] << 17) & 0xFFFFFFFFFFFFFFFF
        return g[1]


def eh_gerador(g):                     # •Reconhecedor
    if type(g) != list:
        return False
    if len(g) != 2 or obtem_estado(g) <= 0 or not isinstance(obtem_estado(g), int) or type(g[0]) != int or (g[0] != 32 and g[0] != 64):
        return False
    return True


def geradores_iguais(g1, g2):               # •Teste
    if eh_gerador(g1) == False or eh_gerador(g2) == False:
        return False
    if g1[0] != g2[0] or obtem_estado(g1) != obtem_estado(g2):
        return False
    return True


def gerador_para_str(g):                    # •Transformador
    f = 'xorshift' + str(g[0]) + '(s=' + str(g[1]) + ')'
    return f


# funcoes de alto nivel


def gera_numero_aleatorio(g, n):
    atualiza_estado(g)
    def mod():
        return obtem_estado(g) % n
    return 1 + mod()


def  gera_carater_aleatorio(g, cad):
    atualiza_estado(g)
    l = ''
    for i in range(ord('A'),(ord(cad)+1)):
        l += chr(i)
    def mod():
        return obtem_estado(g) % len(l)
    return chr(mod() + ord('A'))

"""2.1.2 TAD coordenada"""


def cria_coordenada(col, lin):                              # •Construtor
    if not isinstance(col, str) or not isinstance(lin, int):
        raise ValueError(' cria_coordenada: argumentos invalidos')
    if 'A' > col or col > 'Z' or 1 > lin or lin > 99:
        raise ValueError(' cria_coordenada: argumentos invalidos')
    return (col,lin)


# •Seletores


def obtem_coluna(c):
    return c[0]


def obtem_linha(c):
    return c[1]


def eh_coordenada(arg):                                 # •Reconhecedor
    if type(arg) != tuple:
        return False
    if len(arg) != 2 or 'A' > obtem_coluna(arg) or obtem_coluna(arg) > 'Z' or 1 > obtem_linha(arg) or obtem_linha(arg) > 99\
            or not isinstance(obtem_linha(arg), int) or type(obtem_coluna(arg)) != str:
                return False
    return True


def coordenadas_iguais(c1, c2):                           # •Teste
    if eh_coordenada(c1) == False or eh_coordenada(c2) == False:
        return False
    if obtem_coluna(c1) != obtem_coluna(c2) or obtem_linha(c1) != obtem_linha(c2):
        return False
    return True


# transformadores


def coordenada_para_str(c):
    if obtem_linha(c) < 10:
        return str(obtem_coluna(c)) + '0' + str(obtem_linha(c))
    return str(obtem_coluna(c)) + str(obtem_linha(c))


def str_para_coordenada(s):
    if s[1] == '0':
        return (s[0]),int(s[2])
    return (s[0]), int(s[1]+s[2])


# funcoes de alto nivel


def obtem_coordenadas_vizinhas(c):
    t = ()
    col_diagonal = ord(obtem_coluna(c)) - 1     # para obter as coordenadas vizinhas de linha de cima
    for i in range(3):
        linha_cima = chr(col_diagonal + i)
        if 'A' > linha_cima or linha_cima > 'Z' or 1 > (obtem_linha(c)-1) or (obtem_linha(c)-1) > 99:
            pass
        else:
            t += (cria_coordenada(linha_cima, obtem_linha(c)-1),)
    if 'A' > chr(ord(obtem_coluna(c)) + 1) or chr(ord(obtem_coluna(c)) + 1) > 'Z':   # coordenada vizinha do lado direito
        pass
    else:
        t += (cria_coordenada(chr(ord(obtem_coluna(c)) + 1), obtem_linha(c)),)
    col_diagonal_b = ord(obtem_coluna(c)) + 1
    for i in range(3):                             # para obter as coordenadas vizinhas de linha de baixo
        linha_cima = chr(col_diagonal_b - i)
        if 'A' > linha_cima or linha_cima > 'Z' or 1 > (obtem_linha(c)+1) or (obtem_linha(c)+1) > 99:
            pass
        else:
            t += (cria_coordenada(linha_cima, obtem_linha(c)+1),)
    if 'A' > chr(ord(obtem_coluna(c)) - 1) or chr(ord(obtem_coluna(c)) - 1) > 'Z': # coordenada vizinha do lado direito
        pass
    else:
        t += (cria_coordenada(chr(ord(obtem_coluna(c)) - 1), obtem_linha(c)),)
    return t


def obtem_coordenada_aleatoria(c, g):
    return cria_coordenada(gera_carater_aleatorio(g, obtem_coluna(c)), gera_numero_aleatorio(g, obtem_linha(c)))


"""2.1.3 TAD parcela"""

# construtores
# 'pt' --> parcela tapada
# 'pl' --> parcela limpa
# 'pm' --> parcela marcada
# 'mina' --> parcela que esconde mina

def cria_parcela():
    return ['pt']


def cria_copia_parcela(p):
    copy_p = p
    return copy_p


#• Modificadores


def limpa_parcela(p):
    p[0] = 'pl'
    return p


def marca_parcela(p):
    p = ['pm']
    return p


def desmarca_parcela(p):
    p = ['pt']
    return p


def esconde_mina(p):
     p = ['mina']
     return p


# reconhecedor

def eh_parcela(arg):
    if arg == ['pt'] or arg == ['pl'] or arg == ['pm'] or arg == ['mina']:
        return True
    else:
        return False


def eh_parcela_tapada(p):
    if p == ['pt']:
        return True
    else:
        return False


def eh_parcela_marcada(p):
    if p == ['pm']:
        return True
    else:
        return False


def eh_parcela_limpa(p):
    if p == ['pl']:
        return True
    else:
        return False


def eh_parcela_minada(p):
    if p == ['mina']:
        return True
    else:
        return False


def parcelas_iguais(p1, p2):      # teste
    if p1[0] == p2[0] :
        return True
    else:
        return False


def parcela_para_str(p):                       # Transformadores
    if eh_parcela_limpa(p):
        return '?'
    if eh_parcela_minada(p):
        return 'X'
    if eh_parcela_tapada(p):
        return '#'
    if eh_parcela_marcada(p):
        return '@'

p1 = cria_parcela()
print(p1)
p2 = cria_copia_parcela(p1)
print(p2)
print(parcela_para_str(p1))
print(parcela_para_str(limpa_parcela(p1)))
limpa_parcela(p1)
print(p1)
print(p2)
print(parcelas_iguais(p1, p2)) 
