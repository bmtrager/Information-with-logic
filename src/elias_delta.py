import math
from math import floor
from math import log

# np.random.choice([0, 1], size=(10,), p=[1./3, 2./3])

def Binary_Representation_Without_MSB(x):
    # binary = "{0:b}".format(int(x))
    # binary_without_MSB = binary[1:]
    return format(x, 'b')[1:]
 
def EliasGammaEncode(k):
    if (k == 0):
        return '0'
    N = 1 + floor(log(k, 2))
    Unary = (N-1)*'0'+'1'
    return Unary + Binary_Representation_Without_MSB(k)
 
def EliasDeltaEncode(k):
    Gamma = EliasGammaEncode(1 + floor(log(k, 2)))
    binary_without_MSB = Binary_Representation_Without_MSB(k)
    return Gamma+binary_without_MSB

def  EliasDeltaDecode(x):
    x = list(x)
    L=0
    while True:
        if not x[L] == '0':
            break
        L= L + 1
    
    # Reading L more bits and dropping ALL
    x=x[2*L+1:] 
      
    # Prepending with 1 in MSB
    x.insert(0,'1') 
    x.reverse()
    n=0
      
    # Converting binary to integer
    for i in range(len(x)): 
        if x[i]=='1':
            n=n+math.pow(2,i)
    return int(n)
  
def  EliasDeltaDecode2(x):
    x = list(x)
    L = x.index('1')
    # Reading L more bits and dropping ALL
    x=x[2*L+1:] 
      
    # Prepending with 1 in MSB
    x.insert(0,'1') 
    x.reverse()
    n=0
      
    # Converting binary to integer
    for i in range(len(x)): 
        if x[i]=='1':
            n=n+math.pow(2,i)
    return int(n)

def  EliasDeltaDecode3(x):
    L = x.index("1")
    # Reading L more bits and dropping ALL
    x=x[2*L+1:] 
    return int("1" + x,2)


#k = 137
#st = EliasDeltaEncode(k)
#print(st)
#print(EliasDeltaDecode(st))
#print(EliasDeltaDecode3(st))



