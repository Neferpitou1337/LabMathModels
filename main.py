from sympy.logic.boolalg import to_dnf
from collections import deque
import re

# NOT(A) OR NOT(B) = A NAND B
# A AND B = NOT(A NAND B)
# NOT(A) = A NAND A
#Input:
# ~ is NOT
# & is AND
# | is OR
# divide one expr in several

def partsOf(DNFBoolExp):
    return DNFBoolExp.split("|")


def remove_character(string, index):
    s = list(string)
    del s[index]
    return "".join(s)


# transformations of the conjunction parts
def conjParts(conjList):
    counter = 0
    stack = []
    some_bul = False
    halfCompl = []
    for i in conjList:
        for sym in i:
            #if we have some ~value we convert it to NOT value
            if some_bul:
                some_bul = False
                stack.append('NOT '+ sym)
                counter+=1
                continue
            if sym == '(' or sym == ')' or sym == ' ' or sym == '&':
                continue
            elif sym == "~":
                some_bul = True
            else:
                stack.append(sym)
                counter += 1
        #if stack contain only 1 elem prgm return this value
        if len(stack) == 1:
            halfCompl.append(stack[-1])
            stack.pop()
        else:
            for i in range(0, counter):
                A = 'NOT ( ' + stack[-1] + ' NAND ' + stack[-2] + ' )'
                stack.pop()
                stack.pop()
                if len(stack) == 0: break

                stack.append(A)
                #A = ''
            halfCompl.append(A)
    return halfCompl


# transformations of the disjunction parts
def disjParts(disjList):
    END = []
    #if this list has only 1 value prgm will return it
    if len(disjList)==1:
        return "".join(disjList)

    for i in disjList:
        A = 'NOT ( ' + disjList[-1] + ' ) NAND NOT ( '+  disjList[-2] + ' )'
        disjList.pop()
        disjList.pop()

        if len(disjList) == 0:
            return A
        disjList.append(A)
# doesn't work correctly

def bracketsDestination(str):
    stack = []
    ltinlt = []
    for i in range(len(str)):
        if str[i] =='(':
            stack.append(i)
        if str[i] ==')':
            ltinlt.append([stack[-1], i])
            stack.pop()
    return ltinlt

def delExtraNOT(str):
    coord = bracketsDestination(str)
    letterList = []
    for i in coord:
        letterList.append("".join(re.findall(" [A-Z] ", str[i[0] : i[1]] )))
    print(letterList)
    tmp = 1
    for j in range(0, len(letterList)-1):
        if letterList[j] == letterList[j+1]:
            letterList[j] = letterList[j+1] = ''
            #TODO: delete brackets here
            str = remove_character(str, coord[j][0])
            str = remove_character(str, coord[j][1])

            str = remove_character(str, coord[j+1][0])
            str = remove_character(str, coord[j+1][1])
    print(str)


# Simplification and calling the functions aka main
boolExpr = input("print some boolean expressions: ")
SimpleDNF = to_dnf(boolExpr, True).__str__()
print("Simplification is ",SimpleDNF)
print("Expression using NAND and NOT gates is ",disjParts(conjParts(partsOf(SimpleDNF))))
print(bracketsDestination('NOT ( NOT ( NOT ( D NAND C ) NAND B ) ) NAND NOT ( A )'))

delExtraNOT(disjParts(conjParts(partsOf(SimpleDNF))))
#TODO: mdy delete repeated NOT, mby no mby fuck you