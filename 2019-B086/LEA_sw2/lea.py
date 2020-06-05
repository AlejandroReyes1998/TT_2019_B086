import random

KeyL = 256
blockSize = 128
minimumBlockLength = 32
numberOfKeyPartitions = int(KeyL/minimumBlockLength)
r =  24 if KeyL == 128 else 28 if KeyL == 192 else 32 

strToBits = lambda str  : ''.join(list(bits(str)))
BitsToStr = lambda binN : ''.join(from_bits(binN))
intToBits = lambda myInt: "{0:b}".format(myInt)
ROL       = lambda i,x  : x[i:] + x[:i]
ROR       = lambda i,x  : x[-i:] + x[:-i]
XOR       = lambda x,y  : format((int(x, 2) ^ int(y, 2)), 'b').zfill(minimumBlockLength)
mod_add   = lambda x,y  : format((int(x,2)+int(y,2)) % 2**minimumBlockLength, 'b').zfill(minimumBlockLength)
mod_sub   = lambda x,y  : format((int(x,2)-int(y,2)) % 2**minimumBlockLength, 'b').zfill(minimumBlockLength)
divideKey = lambda K    : list(divide_chunks(K,minimumBlockLength))
BitsToStr = lambda b    : ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(b)]*8))

deltaConstants = ['11000011111011111110100111011011', #0xc3efe9db
                  '01000100011000100110101100000010', #0x79e27c8a
                  '01111001111000100111110010001010', #0x715ea49e
                  '01111000110111110011000011101100', #0xe04ef22a
                  '01110001010111101010010010011110', #0x44626b02
                  '11000111100001011101101000001010', #0x78df30ec
                  '11100000010011101111001000101010', #0xc785da04
                  '11100101110001000000100101010111'  #0xe5c40957
                 ]

  
def initializeCipherProcessValues(PlainText):
  P_s = []
  paddingBlockLenght = 0
  aux = (len(PlainText)/blockSize)
  s,i = int(aux),0
  nBlocks = s if aux % 1 == 0 else s+1
  while(i<nBlocks):
    block = PlainText[blockSize*i:blockSize*(i+1)]
    blockl = len(block)
    if(blockl < blockSize):
      paddingBlockLenght = blockSize-blockl
      block+=getPaddingBlock(paddingBlockLenght)
    P_s.append(block)

    i+=1
  P_s = [list(divide_chunks(i,minimumBlockLength)) for i in P_s]
  return P_s,nBlocks,paddingBlockLenght

def intializeDecipherProcessValues(CipherText):

  cipherTextLenght = len(CipherText)
  pbbegin = cipherTextLenght-7
  pbend   = cipherTextLenght
  paddingBlockLenght = int(CipherText[pbbegin:pbend],2)
  CipherText = CipherText[0:pbbegin]
  C_s = []
  s = list(divide_chunks(CipherText,blockSize))
  for i in s:
    C_s.append(list(divide_chunks(i,minimumBlockLength)))
  nBlocks = int(len(CipherText)/blockSize)
  return C_s,nBlocks,paddingBlockLenght

def getPaddingBlock(lenght):
  paddedMesage = random.getrandbits(lenght)
  paddedMesage = intToBits(paddedMesage).zfill(lenght)
  return paddedMesage


def getRoundKey(T,i,r):
    if r == 24:
      T[0] = ROL(1 ,mod_add(T[0],ROL(i+0,deltaConstants[i%4])))
      T[1] = ROL(3 ,mod_add(T[1],ROL(i+1,deltaConstants[i%4])))
      T[2] = ROL(6 ,mod_add(T[2],ROL(i+2,deltaConstants[i%4])))
      T[3] = ROL(11,mod_add(T[3],ROL(i+3,deltaConstants[i%4])))

      return [T[0],T[1],T[2],T[1],T[3],T[1]]

    elif r == 28:
      T[0] = ROL(1, mod_add(T[0],ROL(i+0,deltaConstants[i%6])))
      T[1] = ROL(3, mod_add(T[1],ROL(i+1,deltaConstants[i%6])))
      T[2] = ROL(6, mod_add(T[2],ROL(i+2,deltaConstants[i%6])))
      T[3] = ROL(11,mod_add(T[3],ROL(i+3,deltaConstants[i%6])))
      T[4] = ROL(13,mod_add(T[4],ROL(i+4,deltaConstants[i%6])))
      T[5] = ROL(17,mod_add(T[5],ROL(i+5,deltaConstants[i%6])))

      return [T[0],T[1],T[2],T[3],T[4],T[5]]

    else:
      T[(6*i+0) % 8] = ROL(1 ,mod_add(T[(6*i+0) % 8],ROL(i+0,deltaConstants[i%8])))
      T[(6*i+1) % 8] = ROL(3 ,mod_add(T[(6*i+1) % 8],ROL(i+1,deltaConstants[i%8])))
      T[(6*i+2) % 8] = ROL(6 ,mod_add(T[(6*i+2) % 8],ROL(i+2,deltaConstants[i%8])))
      T[(6*i+3) % 8] = ROL(11,mod_add(T[(6*i+3) % 8],ROL(i+3,deltaConstants[i%8])))
      T[(6*i+4) % 8] = ROL(13,mod_add(T[(6*i+4) % 8],ROL(i+4,deltaConstants[i%8])))
      T[(6*i+5) % 8] = ROL(17,mod_add(T[(6*i+5) % 8],ROL(i+5,deltaConstants[i%8])))

      return [T[(6*i+0) % 8],T[(6*i+1) % 8],T[(6*i+2) % 8],T[(6*i+3) % 8],T[(6*i+4) % 8],T[(6*i+5) % 8]]

def runKeySchedule(T):
  RK = []
  i = 0
  while(i<r):
    RK.append(getRoundKey(T,i,r))
    i+=1
  return RK

def divide_chunks(l, n):  
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def cipherPlainText(P_s,RK,nBlocks,pms):
  X,C = [],[]
  for i in range(nBlocks):
    X.append(P_s[i])
    for j in range(r):
      S = []
      S.append(ROL(9,mod_add(XOR(X[j][0],RK[j][0]),XOR(X[j][1],RK[j][1]))))
      S.append(ROR(5,mod_add(XOR(X[j][1],RK[j][2]),XOR(X[j][2],RK[j][3]))))
      S.append(ROR(3,mod_add(XOR(X[j][2],RK[j][4]),XOR(X[j][3],RK[j][5]))))
      S.append(X[j][0])
      X.append(S)
    C.append(''.join(X[-1]))
    X.clear()
  #print((str(pms) if pms > 99 else "0"+str(pms) if pms > 9 else "00"+str(pms)))
  return str(''.join(C))+(intToBits(pms).zfill(7))

def decipherText(C_s,RK,nBlocks,pms):
  X,D = [],[]
  for i in range(nBlocks):
    X.append(C_s[i])
    for j in range(r):
      S=[]
      k = len(RK)-1-j
      S.append(X[j][3])
      S.append(XOR(mod_sub(ROR(9,X[j][0]),XOR(X[j][3],RK[k][0])), RK[k][1]))
      S.append(XOR(mod_sub(ROL(5,X[j][1]),XOR(S[1]   ,RK[k][2])), RK[k][3]))
      S.append(XOR(mod_sub(ROL(3,X[j][2]),XOR(S[2]   ,RK[k][4])), RK[k][5]))
      X.append(S)
    D.append(''.join(X[-1]))
    X.clear()
  return str(''.join(D))[0:len(D)-pms]

def bits(s):
    for c in s:
        yield from (str(int(bit)) for bit in bin(ord(c))[2:].zfill(8))

def from_bits(b):
    for i in range(0, len(b), 8): 
        yield chr(int(''.join(str(bit) for bit in b[i:i + 8]), 2)) 

def runApp():

  #CipherProcess
  plainText = "Loremipsumdolorsitamet,consecteturadipiscingelit.Maecenasacloremimperdiet"
  P = strToBits(plainText)
  Key = random.getrandbits(KeyL)
  K = intToBits(Key).zfill(KeyL)
  P_s,nBlocks,pms1 = initializeCipherProcessValues(P)
  K_s = divideKey(K)
  T = K_s
  RK = runKeySchedule(T)
  C = cipherPlainText(P_s,RK,nBlocks,pms1)
  #EndCipherProcess

  #BeginCipherInstructions
  print("Cipher Process")
  print("Pt= "+BitsToStr(P))
  print("Ct= "+BitsToStr(C))
  #EndCipherInstructions

  #BeginDecipherProcess
  C = C
  K = intToBits(Key).zfill(KeyL)
  C_s,nBlocks,pms2  = intializeDecipherProcessValues(C)
  K_s = divideKey(K)
  T = K_s
  RK = runKeySchedule(T)
  D = decipherText(C_s,RK,nBlocks,pms2)
  #EndDecipherProcess

  #BeginDecipherInstructions  
  print("Decipher Process")
  print("Dt= "+BitsToStr(D))
  print("Ct= "+BitsToStr(C))
  #EndDecipherInstructions

  
runApp()