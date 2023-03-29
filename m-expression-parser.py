# parses by reds per m-espressioni:
# F[x;y;...]
# [ e0; e1; ...]

''' grammatica (da parser combinator di Matt Might, estesa per le liste

exp ::= app | ID | '[' exp arg* ']'       (nota: con id qui accetto non liste tra [ e ]
app ::= ID '[' exp arg* ']'
arg ::= ';' exp

nota che sia app che ID iniziano per ID;
distinguo i due casi cosi:

se il token corrente e' un ID (non e' una [ o ; o ]),
se il token successivo e' [, allora chiamo la procedura
app altrimenti consumo ID  (dovrebbe essere quindi LL(2) )

output:

dato che P[ x; y; ... ] significa che P e' applicato a y, y, ...,
l'output e' una s-espressione, ovvero (P x y ...)

'''

#import re
#  id = re.compile(r'

ti = -1

_id = 0
_app = 1


def flat(t):
  r = []
  if type(t) != type([]):
     return t
  if len(t) == 1:
    return t[0]
  for e in t:
   if type(e) == type([]):
     s = flat(e)
     r += s
   else:
     r.append(e)
  return r

def arg(tt):
  global ti
  # salta ;
  if tt[ti] != ';':
    print('ERRORE, atteso ;, trovato', tt[ti])
    raise RuntimeError('errore di parsing')
  ti += 1
  res = []
  #while tt[ti] != Eot and tt[ti] != ']':
  return expr(tt) #  res.append(expr(tt))
  #return res   

Eot = -1
       
def app(tt):
  global ti
  head = tt[ti]
  ti += 2
  e0 = expr(tt)
  ris = [head, e0]
  while tt[ti] != ']' :
     a = arg(tt)
     ris.append(flat(a))
  ti += 1 # salta la ]    
  return ris     
  
def lista(tt):
  global ti
  ti += 1 # salta la [
  e0 = expr(tt)
  ris = [e0]
  while tt[ti] != ']' :
     a = arg(tt)
     # ris.append(flat(a))
     ris.append(a)
  return ris     
  
  
def expr(tt):
  global ti
  #print('ocio', len(tt), ti)
  if tt[ti] == '[':
     return lista(tt)
  if tt[ti+1].startswith('['):
     return app(tt)
  h = tt[ti]
  ti += 1
  return h
  
def test(p):
  global ti
  #print('input',p)
  # il "Lexer" : pro
  p = p.replace('[', ' [ ').replace(']', ' ] ').replace(';',' ; ').replace(',', ' , ').split() #.append(-1)
  print('input:',' '.join(p))
  p.append(-1)
  #print(p)
  ti = 0
  r = expr(p)
  print('outp ', r)
  print('-----------------')
       
p0 = [ 'F', '[', 'x', ';', 'y', ']', -1]
p1 = [ 'F', '[', 'x', ';', 'G', '[', 'y', ']', ']', -1]
p2 = [ 'F', '[', 'x', ';', 'G', '[', 'y', ';', 'j', ']', ']', -1]
p3 = [ '[', 'x', ';', 'y', ']' ]
''' ti = 0
r = expr(p0)
print(r)'''

#test(''.join(p3))

test( 'F[x;y]')
test( 'F[x;G[y]]')
test( 'F[x;G[y;j]]')
test('F[G[x]]')
test('F[G[x;y]]')
test( 'F[G[x;y;z]]')
test( '[F[x;y];u]')
test( '[F[x;K[y;m;o]];u]')
test( '[F[x;K[y;m;o]];O[t;v;oi]]')
test( 'P[F[x;K[y;m;o]];O[t;v;oi]]')
test( 'P[F[x;K[y;m]];O[t;v]]')
test( 'P[F[x;K[y]];O[t]]')
# test( '[ P[Q[s;t] ; M[G[u;v]]')
# test( '[x,y]')

test( '[ P[Q[s;t]] ; M[G[u;v]] ]')
test( '[M[G[u;v]]]')

test( '[x;M[G[u;v]]]')

''' OUTPUT:
input: F [ x ; y ]
outp  ['F', 'x', 'y']
-----------------
input: F [ x ; G [ y ] ]
outp  ['F', 'x', ['G', 'y']]
-----------------
input: F [ x ; G [ y ; j ] ]
outp  ['F', 'x', ['G', 'y', 'j']]
-----------------
input: F [ G [ x ] ]
outp  ['F', ['G', 'x']]
-----------------
input: F [ G [ x ; y ] ]
outp  ['F', ['G', 'x', 'y']]
-----------------
input: F [ G [ x ; y ; z ] ]
outp  ['F', ['G', 'x', 'y', 'z']]
-----------------
input: [ F [ x ; y ] ; u ]
outp  [['F', 'x', 'y'], 'u']
-----------------
input: [ F [ x ; K [ y ; m ; o ] ] ; u ]
outp  [['F', 'x', ['K', 'y', 'm', 'o']], 'u']
-----------------
input: [ F [ x ; K [ y ; m ; o ] ] ; O [ t ; v ; oi ] ]
outp  [['F', 'x', ['K', 'y', 'm', 'o']], ['O', 't', 'v', 'oi']]
-----------------
input: P [ F [ x ; K [ y ; m ; o ] ] ; O [ t ; v ; oi ] ]
outp  ['P', ['F', 'x', ['K', 'y', 'm', 'o']], ['O', 't', 'v', 'oi']]
-----------------
input: P [ F [ x ; K [ y ; m ] ] ; O [ t ; v ] ]
outp  ['P', ['F', 'x', ['K', 'y', 'm']], ['O', 't', 'v']]
-----------------
input: P [ F [ x ; K [ y ] ] ; O [ t ] ]
outp  ['P', ['F', 'x', ['K', 'y']], ['O', 't']]
-----------------
input: [ P [ Q [ s ; t ] ] ; M [ G [ u ; v ] ] ]
outp  [['P', ['Q', 's', 't']], ['M', ['G', 'u', 'v']]]
-----------------
input: [ M [ G [ u ; v ] ] ]
outp  [['M', ['G', 'u', 'v']]]
-----------------
input: [ x ; M [ G [ u ; v ] ] ]
outp  ['x', ['M', ['G', 'u', 'v']]]
-----------------
'''
