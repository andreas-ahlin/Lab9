# Syntaxkontroll

from LinkedQFileLab8 import LinkedQ
from StackCHATGPT import Stack


class Syntaxfel(Exception):
    pass


def readFormel(q):
    syntax_stack = Stack()
    readMol(q, syntax_stack)
    if q.peek() == "\n":
        if not syntax_stack.is_empty():
            raise Syntaxfel("Saknad högerparentes vid radslutet")
        q.dequeue()


def readMol(q, s):
    readGroup(q, s)
    if q.peek() != '\n':
        readMol(q, s)


def readGroup(q, s):

    if q.peek() == "\n":
        return
    elif q.peek() == '(':
        s.push(q.dequeue())
        readMol(q, s)

    elif q.peek() == ')':
        if s.is_empty():
            raise Syntaxfel("Felaktig gruppstart vid radslutet ")
        else:
            s.pop()
            q.dequeue()
            if q.peek() in '123456789':
                readNum(q)
            else:
                raise Syntaxfel("Saknad siffra vid radslutet ")

    elif q.peek() in '0123456789':
        raise Syntaxfel("Felaktig gruppstart vid radslutet ")

    else:
        readAtom(q)
        if q.peek() in '0123456789':
            readNum(q)


def readAtom(q):
    atom = readBLetter(q)
    char = q.peek()
    if char not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        atom = atom+readSLetter(q)
    lista = "H  He  Li  Be  B  C  N  O  F  Ne  Na  Mg  Al  Si  P  S  Cl  Ar  K  Ca  Sc  Ti  V  Cr  Mn  Fe  Co  Ni  Cu  Zn  Ga  Ge  As  Se  Br  Kr  Rb  Sr  Y  Zr  Nb  Mo  Tc  Ru  Rh  Pd  Ag  Cd  In  Sn  Sb  Te  I  Xe  Cs  Ba  La  Ce  Pr  Nd  Pm  Sm  Eu  Gd  Tb  Dy  Ho  Er  Tm  Yb  Lu  Hf  Ta  W  Re  Os  Ir  Pt  Au  Hg  Tl  Pb  Bi  Po  At  Rn  Fr  Ra  Ac  Th  Pa  U  Np  Pu  Am  Cm  Bk  Cf  Es  Fm  Md  No  Lr  Rf  Db  Sg  Bh  Hs  Mt  Ds  Rg  Cn  Fl  Lv"
    lista = lista.split('  ')

    if atom not in lista:
        raise Syntaxfel("Okänd atom vid radslutet ")


def readBLetter(q):
    char = q.dequeue()
    if char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        return char
    raise Syntaxfel("Saknad stor bokstav vid radslutet " + char)


def readSLetter(q):
    if not q.peek() in '0123456789()\n':
        char = q.dequeue()  # Skippar ifall det bara matas in stor bokstav
        return char
    return ''
    # if char in 'abcdefghijklmnopqrstuvwxyz':
    #     return
    # raise Syntaxfel("Saknad liten bokstav vid radslutet " + char)


def readNum(q):
    char = q.peek()
    if char in '123456789':  # kollar om det kommer en nolla
        q.dequeue()
        # Om det första siffran är 1 måste den följas av något annat
        if char == '1' and not q.peek() in '0123456789':
            raise Syntaxfel("För litet tal vid radslutet ")

        while q.peek() in '0123456789':
            q.dequeue()
        return
    elif char == '\n':
        return
    q.dequeue()
    raise Syntaxfel("För litet tal vid radslutet ")


def printQueue(q):
    while not q.isEmpty():
        char = q.dequeue()
        print(char, end=" ")
    print()


def storeMolekyl(molekyl):
    q = LinkedQ()
    molekyl = [*molekyl]
    for char in molekyl:
        q.enqueue(char)
    q.enqueue("\n")
    return q


def kollaMolekyl(Molekyl):
    q = storeMolekyl(Molekyl)

    try:
        readFormel(q)
        return "Formeln är syntaktiskt korrekt"
    except Syntaxfel as fel:
        resMol = ''
        while q.peek() != '\n':
            resMol = resMol+q.dequeue()
        return str(fel) + str(resMol)


def main():
    molekyl = str(input(""))
    while molekyl != '#':
        resultat = kollaMolekyl(molekyl)
        print(resultat)
        molekyl = str(input(""))


if __name__ == "__main__":
    main()
