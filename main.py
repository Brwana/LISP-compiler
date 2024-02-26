
import customtkinter
import tkinter as tk
from enum import Enum
import re
import pandas
import pandastable as pt
from PIL import ImageTk
from nltk.tree import *
import customtkinter
from PIL import Image, ImageTk
from tkinter import Toplevel
import tkinter as tk
from tkinter import ttk
import colormath
import jupyterlab
import graphviz
import pandas

from automata.fa.dfa import DFA
from visual_automata.fa.dfa import VisualDFA
# Import module
from tkinter import *

import tkinter as tk
from enum import Enum
import re
import getkey

import os



class Token_type(Enum):

    Integer = 2
    Dot = 3
    Semicolon = 4
    EqualOp = 5
    LessThanOp = 6
    GreaterThanOp = 7
    NotEqualOp = 8
    PlusOp = 9
    MinusOp = 10
    MultiplyOp = 11
    DivideOp = 12
    Identifier = 13
    Constant = 14
    Error = 2
    comment = 23
    string = 24
    when = 25
    dotimes = 26
    t = 27
    read = 28
    setq = 29
    nil = 30
    write = 31
    modOp = 32
    remOp = 33
    GreaterthanorEqual = 34
    LessthanorEqual = 35
    bracketL = 36
    bracketR = 37
    Incf = 38
    Decf = 39
    epsilon = 40
    sin = 41
    cos = 42
    tan = 43
    defconstant = 44


# class token to hold string and token type
class token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }

    # Reserved word Dictionary

ReservedWords = {
    "setq": Token_type.setq,
    "dotimes": Token_type.dotimes,
    "nil": Token_type.nil,
    "write": Token_type.write,
    "read": Token_type.read,
    "t": Token_type.t,
    "when": Token_type.when,
    "E": Token_type.epsilon,
    "sin": Token_type.sin,
    "cos": Token_type.cos,
    "tan": Token_type.tan,
    "defconstant": Token_type.defconstant,
}
Operators = {".": Token_type.Dot,
             ";": Token_type.Semicolon,
             "=": Token_type.EqualOp,
             "+": Token_type.PlusOp,
             "-": Token_type.MinusOp,
             "*": Token_type.MultiplyOp,
             "/": Token_type.DivideOp,
             "mod": Token_type.modOp,
             "rem": Token_type.remOp,
             "incf": Token_type.Incf,
             "decf": Token_type.Decf,
             ">": Token_type.GreaterThanOp,
             "<": Token_type.LessThanOp,
             ">=": Token_type.GreaterthanorEqual,
             "<=": Token_type.LessthanorEqual,
             "\"": Token_type.string,
             "(": Token_type.bracketL,
             ")": Token_type.bracketR

             }

Tokens = []  # to add tokens to list
check_tokens = []
STring = []
errors = []


def testString(text1, j):
    global count
    index = j
    while j < len(text1):
        if text1[j] == "\"":
            if text1[j - 1] == "\\":
                j = j + 1
                continue
            elif text1[j + 1] != " ":
                index = j
                count += 1

            else:
                index = j
                count += 1

        j = j + 1
    if text1[index - 1] != " ":
        pass

    return index


def find_token(text):
    text1 = list(text.lower())
    j = 0
    conc = text1[j]
    while j < len(text1):
        if ((text1[j] != " ") & (text1[j] != ";") & (text1[j] != "(") & (text1[j] != ")") & (text1[j] != "\"") & (
                text1[j] != "\n")):
            if (j == 0):
                conc = text1[j]
                j = j + 1
                continue
            else:
                conc = conc + text1[j]
                j = j + 1

        elif (text1[j] == "\n"):
            j = j + 1
            continue

        elif (text1[j] == " "):

            if (conc != "") & (conc != " ") & (conc != ";") & (conc != "(") & (conc != ")"):
                check_tokens.append(conc)
                conc = ""
            if conc == " ":
                conc = ""
            j = j + 1

        elif text1[j] == "\"":
            check_tokens.append(text1[j])
            j = testString(text1, j)

            check_tokens.append(text1[j])
            j += 1

        elif ((text1[j] == "(") or (text1[j] == ")")):

            if conc != "":
                check_tokens.append(conc)
            if (conc != ")") & (conc != "("):
                check_tokens.append(text1[j])
            conc = ""
            j = j + 1

        elif text1[j] == ";":
            if conc == ";":
                conc = ""


            j = j + 1
            while text1[j] != "\n" and (j != len(text1) - 1):
                j = j + 1
                continue
            if j == len(text1) - 1:
                break
            j = j + 1

        else:

            break

    if ((conc != "") & (conc != ";") & (conc != " ") & (conc != "(") & (conc != ")") & (conc != "\n")):
        check_tokens.append(conc)


def appending(st):
    i = 0
    while i < len(st):
        if i == 0:
            strin = st[i]
            i = i + 1
            continue
        else:
            strin = strin + st[i]
            i = i + 1
            return strin


def checkindict(check_tokens):
    for i in check_tokens:
# print(i)
        if i in ReservedWords:
            Tokens.append(token(i, ReservedWords[i]))
        elif i in Operators:

            Tokens.append(token(i, Operators[i]))
        elif re.match("^[0-9]+(\.[0-9]*)?$", i):

            Tokens.append(token(i, Token_type.Constant))
        elif re.match("^[a-z A-Z][a-zA-Z 0-9]*$", i):

            Tokens.append(token(i, Token_type.Identifier))
        else:

            Tokens.append(token(i, Token_type.Error))
    if appending(STring) is not None:
        Tokens.append(token(appending(STring), Token_type.Constant))





def check(x1):
    tex = list(x1)
    co = 0
    i=0
    while i < len(tex):
        if tex[i] == '(' or tex[i] == ')':
            co = co + 1
        i=i+1

    if co % 2 == 0:
        return True
    else:
        return False


def Parse(x1):
    j = 0
    Children = []

    lenn = 0
    while lenn < len(Tokens) - 1:
        bracketL_dict = Match(Token_type.bracketL, lenn)
        Children.append(bracketL_dict["node"])
        # ba3dih ) node else
        # temp = Tokens[bracketL_dict["index"]].to_dict()
        # #if (check(x1) == 0):
        # out["node"] = ["error"]
        # out["index"] = j + 1
        # errors.append("Syntax error :  Expected )")  # hena ana lama b2ool en el enta mda5alo 3'alat wel excpected kaza
        # Children.append(out["node"])
        # Node = Tree('error',Children)
        # temp["token_type"] != Token_type.bracketR
        List_dict = Listt(bracketL_dict["index"])
        Children.append(List_dict["node"])
        bracketR_dict = Match(Token_type.bracketR, List_dict["index"])

        Children.append(bracketR_dict["node"])
        lenn = bracketR_dict["index"]

    Node = Tree('Program', Children)
    return Node




def Listt(j):
    out = dict()
    childern = []
    if atom(j) is not None:
        atom_dict = atom(j)
        childern.append(atom_dict["node"])
        Node = Tree('List', childern)  # given non terminal and its childern
        out["node"] = Node
        out["index"] = atom_dict["index"]
        return out
    else:
        statement_dict = statement(j)
        childern.append(statement_dict["node"])
        if statement_dict["index"] > len(Tokens) - 1:
            Node = Tree('List', childern)
            out["node"] = Node
            out["index"] = statement_dict["index"]
            return out

        else:
            temp = Tokens[statement_dict["index"]].to_dict()
            if temp["token_type"] == Token_type.bracketL:

                bracketL_dict = Match(Token_type.bracketL, statement_dict["index"])
                childern.append(bracketL_dict["node"])
                List_dict = Listt(bracketL_dict["index"])
                childern.append(List_dict["node"])
                bracketR_dict = Match(Token_type.bracketR, List_dict["index"])
                childern.append(bracketR_dict["node"])
                temp = Tokens[bracketR_dict["index"]].to_dict()
                if temp["token_type"] == Token_type.bracketL:
                    bracketL1_dict = Match(Token_type.bracketL, bracketR_dict["index"])
                    childern.append(bracketL1_dict["node"])
                    List1_dict = Listt(bracketL1_dict["index"])
                    childern.append(List1_dict["node"])
                    bracketR2_dict = Match(Token_type.bracketR, List1_dict["index"])
                    childern.append(bracketR2_dict["node"])
                    Node = Tree('List', childern)
                    out["node"] = Node
                    out["index"] = bracketR2_dict["index"]
                    return out
                else:
                    Node = Tree('List', childern)
                    out["node"] = Node
                    out["index"] = bracketR_dict["index"]
                    return out
            else:
                Node = Tree('List', childern)
                out["node"] = Node
                out["index"] = statement_dict["index"]
                return out





def atom(j):
    out = dict()
    children = []
    temp = Tokens[j].to_dict()
    if temp["token_type"] == Token_type.Constant:  # early stoping i=of error
        const_dict = Match(Token_type.Constant, j)
        children.append(const_dict["node"])
        node = Tree("atom", children)
        out["node"] = node
        out["index"] = const_dict["index"]
        return out
    elif temp["token_type"] == Token_type.Identifier:
        id_dict = Match(Token_type.Identifier, j)
        children.append(id_dict["node"])
        node = Tree("atom", children)
        out["node"] = node
        out["index"] = id_dict["index"]
        return out


def statement(j):
    out = dict()
    children = []
    temp = Tokens[j].to_dict()
    if temp["token_type"] == Token_type.setq:
        setq_dict = Match(Token_type.setq, j)
        children.append(setq_dict["node"])
        id_dict = Match(Token_type.Identifier, setq_dict["index"])
        children.append(id_dict["node"])
        s2_dict = S2(id_dict["index"])
        children.append(s2_dict["node"])
        node = Tree("Statement", children)
        out["node"] = node
        out["index"] = s2_dict["index"]
        return out
    elif temp["token_type"] == Token_type.defconstant:
        defconst_dict = Match(Token_type.defconstant, j)
        children.append(defconst_dict["node"])
        id_dict = Match(Token_type.Identifier, defconst_dict["index"])
        children.append(id_dict["node"])
        const_dict = Match(Token_type.Constant, id_dict["index"])
        children.append(const_dict["node"])
        node = Tree("Statement", children)
        out["node"] = node
        out["index"] = const_dict["index"]
        return out

    elif temp["token_type"] == Token_type.write:
        write_dict = Match(Token_type.write, j)
        children.append(write_dict["node"])
        s3_dict = S3(write_dict["index"])
        children.append(s3_dict["node"])
        node = Tree("Statement", children)
        out["node"] = node
        out["index"] = s3_dict["index"]
        return out

    elif temp["token_type"] == Token_type.dotimes:
        dotimes_dict = Match(Token_type.dotimes, j)
        children.append(dotimes_dict["node"])
        Iter_dict = Iter(dotimes_dict["index"])
        children.append(Iter_dict["node"])
        bracketL_dict = Match(Token_type.bracketL, Iter_dict["index"])
        children.append(bracketL_dict["node"])
        Statement_dict = statement(bracketL_dict["index"])
        children.append(Statement_dict["node"])
        bracketR_dict = Match(Token_type.bracketR, Statement_dict["index"])
        children.append(bracketR_dict["node"])

        node = Tree("Statement", children)
        out["node"] = node
        out["index"] = bracketR_dict["index"]
        return out

    elif temp["token_type"] == Token_type.when:
        when_dict = Match(Token_type.when, j)
        children.append(when_dict["node"])
        bracketL_dict = Match(Token_type.bracketL, when_dict["index"])
        children.append(bracketL_dict["node"])
        cond_dict = condition(bracketL_dict["index"])
        children.append(cond_dict["node"])
        bracketR2_dict = Match(Token_type.bracketR, cond_dict["index"])
        children.append(bracketR2_dict["node"])
        bracketL1_dict = Match(Token_type.bracketL, bracketR2_dict["index"])
        children.append(bracketL1_dict["node"])
        Statement_dict = statement(bracketL1_dict["index"])
        children.append(Statement_dict["node"])
        bracketR_dict = Match(Token_type.bracketR, Statement_dict["index"])
        children.append(bracketR_dict["node"])
        node = Tree("Statement", children)
        out["node"] = node
        out["index"] = bracketR_dict["index"]
        return out

    elif temp["token_type"] == Token_type.read:
        read_dict = Match(Token_type.read, j)
        children.append(read_dict["node"])
        id_dict = Match(Token_type.Identifier, read_dict["index"])
        children.append(id_dict["node"])
        node = Tree("Statement", children)
        out["node"] = node
        out["index"] = id_dict["index"]
        return out


    elif condition(j):
        cond_dict = condition(j)
        children.append(cond_dict["node"])
        Node = Tree('Statement', children)
        out["node"] = Node
        out["index"] = cond_dict["index"]
        return out

    elif Operator(j) is not None:
        op_dict = Operator(j)
        children.append(op_dict["node"])
        Node = Tree('Statement', children)
        out["node"] = Node
        out["index"] = op_dict["index"]
        return out

    elif Trig(j) is not None:
        trig_dict = Trig(j)
        children.append(trig_dict["node"])
        const_dict = Match(Token_type.Constant, trig_dict["index"])
        children.append(const_dict["node"])
        Node = Tree('Statement', children)
        out["node"] = Node
        out["index"] = const_dict["index"]
        return out

    else:
        out["node"] = ["error"]
        out["index"] = j
        return out


def Trig(j):
    out = dict()
    children = []
    temp = Tokens[j].to_dict()
    if temp["token_type"] == Token_type.sin:
        sin_dict = Match(Token_type.sin, j)
        children.append(sin_dict["node"])
        Node = Tree('Trig', children)
        out["node"] = Node
        out["index"] = sin_dict["index"]
        return out
    elif temp["token_type"] == Token_type.cos:
        cos_dict = Match(Token_type.cos, j)
        children.append(cos_dict["node"])
        Node = Tree('Trig', children)
        out["node"] = Node
        out["index"] = cos_dict["index"]
        return out
    elif temp["token_type"] == Token_type.tan:
        tan_dict = Match(Token_type.tan, j)
        children.append(tan_dict["node"])
        Node = Tree('Trig', children)
        out["node"] = Node
        out["index"] = tan_dict["index"]
        return out


def S3(j):
    out = dict()
    children = []
    temp = Tokens[j].to_dict()
    if atom(j) is not None:
        atom_dict = atom(j)
        children.append(atom_dict["node"])
        Node = Tree('S3', children)  # given non terminal and its childern
        out["node"] = Node
        out["index"] = atom_dict["index"]
        return out
    elif temp["token_type"] == Token_type.bracketL:
        bracketL_dict = Match(Token_type.bracketL, j)
        children.append(bracketL_dict["node"]);
        s4_dict = s4(bracketL_dict["index"])
        children.append(s4_dict["node"])
        bracketR_dict = Match(Token_type.bracketR, s4_dict["index"])
        children.append(bracketR_dict["node"])
        Node = Tree('S3', children)  # given non terminal and its childern
        out["node"] = Node
        out["index"] = bracketR_dict["index"]
        return out



    elif stringg(j) is not None:
        string_dict = stringg(j)
        children.append(string_dict["node"])
        Node = Tree('S3', children)  # given non terminal and its childern
        out["node"] = Node
        out["index"] = string_dict["index"]
        return out

    else:
        out["node"] = ["error"]
        out["index"] = j
        return out


def Operator(j):
    out = dict()
    children = []
    arith_dict = Arithop(j)
    children.append(arith_dict["node"])



    if atom(arith_dict["index"]) is not None:

        atom_dict = atom(arith_dict["index"])
        children.append(atom_dict["node"])
        if atom(atom_dict["index"]) is not None:
            atom2_dict = atom(atom_dict["index"])

            children.append(atom2_dict["node"])

            if  atom2_dict["index"]<len(Tokens) and atom(atom2_dict["index"]) is not None :
                atom3_dict = atom(atom2_dict["index"])
                children.append(atom3_dict["node"])
                Node = Tree('operator', children)
                out["node"] = Node
                out["index"] = atom3_dict["index"]
                return out
            else:
                Node = Tree('operator', children)
                out["node"] = Node
                out["index"] = atom2_dict["index"]
                return out


        else:
            Node = Tree('operator', children)  # given non terminal and its childern
            out["node"] = Node
            out["index"] = atom_dict["index"]
            return out

    else:
        bracketL_dict = Match(Token_type.bracketL, arith_dict["index"])
        children.append(bracketL_dict["node"])
        List_dict = Listt(bracketL_dict["index"])
        children.append(List_dict["node"])
        bracketR_dict = Match(Token_type.bracketR, List_dict["index"])
        children.append(bracketR_dict["node"])
        Node = Tree('operator', children)  # given non terminal and its childern
        out["node"] = Node
        out["index"] = bracketR_dict["index"]
        return out


def Arithop(j):
    out = dict()
    children = []
    temp = Tokens[j].to_dict()
    if temp["token_type"] == Token_type.PlusOp:
        plus_dict = Match(Token_type.PlusOp, j)
        children.append(plus_dict["node"])
        node = Tree("Arithmatic Operator", children)
        out["node"] = node
        out["index"] = plus_dict["index"]
        return out
    elif temp["token_type"] == Token_type.MinusOp:
        minus_dict = Match(Token_type.MinusOp, j)
        children.append(minus_dict["node"])
        node = Tree("Arithmatic Operator", children)
        out["node"] = node
        out["index"] = minus_dict["index"]
        return out
    elif temp["token_type"] == Token_type.MultiplyOp:
        multi_dict = Match(Token_type.MultiplyOp, j)
        children.append(multi_dict["node"])
        node = Tree("Arithmatic Operator", children)
        out["node"] = node
        out["index"] = multi_dict["index"]
        return out
    elif temp["token_type"] == Token_type.DivideOp:
        divide_dict = Match(Token_type.DivideOp, j)
        children.append(divide_dict["node"])
        node = Tree("Arithmatic Operator", children)
        out["node"] = node
        out["index"] = divide_dict["index"]
        return out
    elif temp["token_type"] == Token_type.modOp:
        mod_dict = Match(Token_type.modOp, j)
        children.append(mod_dict["node"])
        node = Tree("Arithmatic Operator", children)
        out["node"] = node
        out["index"] = mod_dict["index"]
        return out

    elif temp["token_type"] == Token_type.remOp:
        rem_dict = Match(Token_type.remOp, j)
        children.append(rem_dict["node"])
        node = Tree("Arithmatic Operator", children)
        out["node"] = node
        out["index"] = rem_dict["index"]
        return out
    elif temp["token_type"] == Token_type.Decf:
        decf_dict = Match(Token_type.Decf, j)
        children.append(decf_dict["node"])
        node = Tree("Arithmatic Operator", children)
        out["node"] = node
        out["index"] = decf_dict["index"]
        return out
    elif temp["token_type"] == Token_type.Incf:
        incf_dict = Match(Token_type.Incf, j)
        children.append(incf_dict["node"])
        node = Tree("Arithmatic Operator", children)
        out["node"] = node
        out["index"] = incf_dict["index"]
        return out
    else:
        out["node"] = ["error"]
        out["index"] = j
        return out


def S2(j):
    out = dict()
    children = []
    temp = Tokens[j].to_dict()
    if temp["token_type"] == Token_type.Constant:
        const_dict = Match(Token_type.Constant, j)
        children.append(const_dict["node"])
        node = Tree("S2", children)
        out["node"] = node
        out["index"] = const_dict["index"]
        return out
    elif temp["token_type"] == Token_type.bracketL:
        bracketL_dict = Match(Token_type.bracketL, j)
        children.append(bracketL_dict["node"])
        stat_dict = statement(bracketL_dict["index"])
        children.append(stat_dict["node"])
        bracketR_dict = Match(Token_type.bracketR, stat_dict["index"])
        children.append(bracketR_dict["node"])
        t = Tokens[bracketR_dict["index"]].to_dict()

        if checkbracket == False:

            children.append(["error"])
            bracketR_dict["index"] = bracketR_dict["index"] + 1
            temp = Tokens[bracketR_dict["index"]].to_dict()
            global flag
            flag = True
            while flag:
                if temp["token_type"] == Token_type.bracketL:

                    bracketL1_dict = Match(Token_type.bracketL, bracketR_dict["index"])
                    children.append(bracketL1_dict["node"])
                    state_dict = statement(bracketL1_dict["index"])
                    children.append(state_dict["node"])
                    bracketR1_dict = Match(Token_type.bracketR, state_dict["index"])
                    children.append(bracketR1_dict["node"])
                    t = Tokens[bracketR1_dict["index"]].to_dict()
                    print("ghh")
                    print(bracketR1_dict["index"] + 1)

                    if t["token_type"] == Token_type.bracketR:
                        children.append(["error"])
                        bracketR1_dict["index"] = bracketR1_dict["index"] + 1
                    else:
                        Node = Tree('S2', children)
                        out["node"] = Node
                        out["index"] = bracketR1_dict["index"]
                        return out
                    temp = Tokens[bracketR1_dict["index"]].to_dict()
                    if temp["token_type"] == Token_type.bracketL:
                        bracketL2_dict = Match(Token_type.bracketL, bracketR1_dict["index"])
                        children.append(bracketL2_dict["node"])
                        state3_dict = statement(bracketL2_dict["index"])
                        children.append(state3_dict["node"])
                        bracketR2_dict = Match(Token_type.bracketR, state3_dict["index"])
                        children.append(bracketR2_dict["node"])

                        Node = Tree('S2', children)
                        out["node"] = Node
                        out["index"] = bracketR2_dict["index"]
                        return out
                    else:
                        Node = Tree('S2', children)
                        out["node"] = Node
                        out["index"] = bracketR1_dict["index"]
                        return out
                else:
                    Node = Tree('S2', children)
                    out["node"] = Node
                    out["index"] = bracketR_dict["index"]
                    return out

        else:
            Node = Tree('S2', children)
            out["node"] = Node
            out["index"] = bracketR_dict["index"]
            return out


    elif temp["token_type"] == Token_type.t:
        t_dict = Match(Token_type.t, j)
        children.append(t_dict["node"])
        node = Tree("S2", children)
        out["node"] = node
        out["index"] = t_dict["index"]
        return out
    elif temp["token_type"] == Token_type.nil:
        nil_dict = Match(Token_type.nil, j)
        children.append(nil_dict["node"])
        node = Tree("S2", children)
        out["node"] = node
        out["index"] = nil_dict["index"]
        return out

    elif temp["token_type"] == Token_type.read:
        read_dict = Match(Token_type.read, j)
        children.append(read_dict["node"])
        id_dict = Match(Token_type.Identifier, read_dict["index"])
        children.append(id_dict["node"])
        node = Tree("S2", children)
        out["node"] = node
        out["index"] = id_dict["index"]
        return out

    else:
        out["node"] = ["error"]
        out["index"] = j
        return out


def Iter(j):
    children = []
    out = dict()
    bracketL_dict = Match(Token_type.bracketL, j)
    children.append(bracketL_dict["node"])
    ident_dict = Match(Token_type.Identifier, bracketL_dict["index"])
    children.append(ident_dict["node"])
    const_dict = Match(Token_type.Constant, ident_dict["index"])
    children.append(const_dict["node"])
    bracketR_dict = Match(Token_type.bracketR, const_dict["index"])
    children.append(bracketR_dict["node"])
    node = Tree("Iter", children)
    out["node"] = node
    out["index"] = bracketR_dict["index"]
    return out



def condition(j):
    children = []
    out = dict()
  # if Tokens[j].to_dict()["token_type"] ==Token_type.bracketL:
    #   bracketL_dict = Match(Token_type.bracketL, j)
    #   children.append(bracketL_dict["node"])
    if Relatop(j) is not None:
        relatop_dict = Relatop(j)
        children.append(relatop_dict["node"])
        atom1_dict = atom(relatop_dict["index"])
        children.append(atom1_dict["node"])
        atom2_dict = atom(atom1_dict["index"])
        children.append(atom2_dict["node"])

        node = Tree("condition", children)
        out["node"] = node
        out["index"] = atom2_dict["index"]
        return out


def Relatop(j):
    children = []
    out = dict()
    temp = Tokens[j].to_dict()
    if temp["token_type"] == Token_type.GreaterthanorEqual:
        greaterthanorequal_dict = Match(Token_type.GreaterthanorEqual, j)
        children.append(greaterthanorequal_dict["node"])
        node = Tree("Relatop", children)
        out["node"] = node
        out["index"] = greaterthanorequal_dict["index"]
        return out
    elif temp["token_type"] == Token_type.LessthanorEqual:
        lessthanorequal_dict = Match(Token_type.LessthanorEqual, j)
        children.append(lessthanorequal_dict["node"])
        node = Tree("Relatop", children)
        out["node"] = node
        out["index"] = lessthanorequal_dict["index"]
        return out
    elif temp["token_type"] == Token_type.GreaterThanOp:
        greaterthan_dict = Match(Token_type.GreaterThanOp, j)
        children.append(greaterthan_dict["node"])
        node = Tree("Relatop", children)
        out["node"] = node
        out["index"] = greaterthan_dict["index"]
        return out
    elif temp["token_type"] == Token_type.LessThanOp:
        lessthan_dict = Match(Token_type.LessThanOp, j)
        children.append(lessthan_dict["node"])
        node = Tree("Relatop", children)
        out["node"] = node
        out["index"] = lessthan_dict["index"]
        return out
    elif temp["token_type"] == Token_type.EqualOp:
        equal_dict = Match(Token_type.EqualOp, j)
        children.append(equal_dict["node"])
        node = Tree("Relatop", children)
        out["node"] = node
        out["index"] = equal_dict["index"]
        return out




def s4(j):
    children = []
    out = dict()
 # temp = Tokens[j].to_dict()
    if condition(j) is not None:
        cond_dict = condition(j)
        children.append(cond_dict["node"])
        node = Tree("s4", children)
        out["node"] = node
        out["index"] = cond_dict["index"]
        return out
    elif Operator(j) is not None:
        oper_dict = Operator(j)
        children.append(oper_dict["node"])
        node = Tree("s4", children)
        out["node"] = node
        out["index"] = oper_dict["index"]
        return out
    else:
        out["node"] = ["error"]
        out["index"] = j
        return out


global count
count = 0


def stringg(j):
    children = []
    out = dict()
    doublequot1_dict = Match(Token_type.string, j)
    children.append(doublequot1_dict["node"])
    if count == 2:
        children.append(["String"])
        doublequot2_dict = Match(Token_type.string, doublequot1_dict["index"])
        children.append(doublequot2_dict["node"])
        node = Tree("STRING", children)
        out["node"] = node
        out["index"] = doublequot2_dict["index"]
        return out
    else:
        children.append(["error"])
        node = Tree("STRING", children)
        out["node"] = node
        out["index"] = doublequot1_dict["index"]
        return out




def Match(a, j):
    output = dict()
    if j < len(Tokens):# hena lao el j 3adet yb2a el machine expected b2eet el string enta msh katebha
        Temp = Tokens[j].to_dict()
        if Temp['token_type'] == a:# hatly mn goa el temp el token type el ana kont mdyahalo f duct_output
            j += 1
            output["node"] = [Temp['Lex']]
            output["index"] = j# b record j 3shan da el index el hakamel b3deeh
            return output
        else:
            output["node"] = ["error"]
            output["index"] = j + 1
            errors.append("Syntax error : " + Temp[
                'Lex'])# hena ana lama b2ool en el enta mda5alo 3'alat wel excpected kaza
            return output
    else:
        output["node"] = ["error"]
        output["index"] = j + 1
        return output


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("600x475")
root.title("Lisp Compiler")
root.resizable(False, False)
bg = PhotoImage(file="F:\second semster\design of compilers\images\images\\background_2.png")
lable1 = customtkinter.CTkLabel(master=root, image=bg)
lable1.place(x=0, y=0)
label = customtkinter.CTkLabel(master=root, text="LISP Compiler", font=('Georgia', 50), bg_color="#201F23",
                               text_color="#479ECE")
label.place(x=90, y=200)
button = customtkinter.CTkButton(master=root, text="Start", width=120, height=60, fg_color="#479ECE",
                                 text_color="#201F23", font=('Georgia', 30),
                                 command=lambda: create_window("Start"), border_width=0)
button.place(x=150, y=400)

root1 = tk.Tk()

canvas1 = tk.Canvas(root1, width=400, height=300, relief='raised', background="#201F23")
canvas1.pack()

entry1 = tk.Entry(root1)
entry1.pack(expand=True, fill=tk.BOTH)
canvas1.create_window(200, 140, window=entry1)


def create_window(button_name):
    global new_window
    global window_3
    global entry1
    if button_name == "Start":
        label.destroy()
        button.destroy()
        button1 = customtkinter.CTkButton(master=root, text="Scanner", font=('Georgia', 20), width=200, height=60,
                                          fg_color="#479ECE", text_color="#201F23",
                                          command=lambda: create_window("Scanner"))
        button1.place(x=150, y=250)
        button2 = customtkinter.CTkButton(master=root, text="Parser", width=200, height=60,
                                          fg_color="#479ECE", font=('Georgia', 20), text_color="#201F23",
                                          command=lambda: create_window("Parser"))

        button2.place(x=150, y=350)

    if button_name == "Scanner":
        new_window = customtkinter.CTkToplevel(root)
        new_window.attributes('-topmost', True)
        new_window.geometry("600x475")
        new_window.title("Scanner")
        new_window.resizable(False, False)
        bg = PhotoImage(file="F:\second semster\design of compilers\images\images\\background_2.png")
        lablel2 = customtkinter.CTkLabel(new_window, image=bg)
        lablel2.place(x=0, y=0)
        comment_button = customtkinter.CTkButton(master=new_window, text="Comment DFA", width=130, height=60,
                                                 fg_color="#479ECE", text_color="#201F23"
                                                 , command=lambda: create_window("Comment DFA"))
        comment_button.place(x=50, y=200)
        constant_button = customtkinter.CTkButton(master=new_window, text="Constants DFA", width=130, height=60,
                                                  fg_color="#479ECE", text_color="#201F23",
                                                  command=lambda: create_window("Constants DFA"))
        constant_button.place(x=200, y=200)
        string_button = customtkinter.CTkButton(master=new_window, text="String DFA", width=130, height=60,
                                                fg_color="#479ECE", text_color="#201F23",
                                                command=lambda: create_window("String DFA"))
        string_button.place(x=50, y=300)
        identifier_button = customtkinter.CTkButton(master=new_window, text="Identifier DFA", width=130, height=60,
                                                    fg_color="#479ECE", text_color="#201F23",
                                                    command=lambda: create_window("Identifier DFA"))
        identifier_button.place(x=200, y=300)
        operation_button = customtkinter.CTkButton(master=new_window, text="Reserved Words DFA", width=130, height=60,
                                                   fg_color="#479ECE", text_color="#201F23",
                                                   command=lambda: create_window("Reserved Words DFA"))
        operation_button.place(x=50, y=400)
        operator_button = customtkinter.CTkButton(master=new_window, text="Operators DFA", width=130, height=60,
                                                  fg_color="#479ECE", text_color="#201F23",
                                                  command=lambda: create_window("Operators DFA"))
        operator_button.place(x=200, y=400)

    if button_name == "Identifier DFA":
        window_2 = customtkinter.CTkToplevel(new_window)
        new_window.attributes('-topmost', False)
        window_2.attributes('-topmost', True)
        window_2.geometry("671x640")
        window_2.title("Identifier DFA")
        window_2.resizable(False, False)
        bg2 = PhotoImage(
            file="F:\second semster\design of compilers\images\images\Identifiers.png")
        lable2 = customtkinter.CTkLabel(master=window_2, image=bg2)
        lable2.place(x=0, y=0)
    if button_name == "Comment DFA":
        window_2 = customtkinter.CTkToplevel(new_window)
        new_window.attributes('-topmost', False)
        window_2.attributes('-topmost', True)
        window_2.geometry("1196x576")
        window_2.title("Comment DFA")
        window_2.resizable(False, False)
        bg2 = PhotoImage(
            file="F:\second semster\design of compilers\images\images\Comment.png")
        lable2 = customtkinter.CTkLabel(master=window_2, image=bg2)
        lable2.place(x=0, y=0)
    if button_name == "Constants DFA":
        window_2 = customtkinter.CTkToplevel(new_window)
        new_window.attributes('-topmost', False)
        window_2.attributes('-topmost', True)
        window_2.geometry("1039x582")
        window_2.title("Constants DFA")
        window_2.resizable(False, False)
        bg2 = PhotoImage(
            file="F:\second semster\design of compilers\images\images\Constants.png")
        lable2 = customtkinter.CTkLabel(master=window_2, image=bg2)
        lable2.place(x=0, y=0)
    if button_name == "String DFA":
        window_2 = customtkinter.CTkToplevel(new_window)
        new_window.attributes('-topmost', False)
        window_2.attributes('-topmost', True)
        window_2.geometry("1073x447")
        window_2.title("String DFA")
        window_2.resizable(False, False)
        bg2 = PhotoImage(
            file="F:\second semster\design of compilers\images\images\\String.png")
        lable2 = customtkinter.CTkLabel(master=window_2, image=bg2)
        lable2.place(x=0, y=0)
    if button_name == "Reserved Words DFA":
        window_2 = customtkinter.CTkToplevel(new_window)
        new_window.attributes('-topmost', False)
        window_2.attributes('-topmost', True)
        window_2.geometry("600x600")
        window_2.title("Reserved Words DFA")
        window_2.resizable(False, False)
        bg2 = PhotoImage(
            file="F:\second semster\design of compilers\images\images\\reserved_words_2.png")
        lable2 = customtkinter.CTkLabel(master=window_2, image=bg2)
        lable2.place(x=0, y=0)
    if button_name == "Operators DFA":
        window_2 = customtkinter.CTkToplevel(new_window)
        new_window.attributes('-topmost', False)
        window_2.attributes('-topmost', True)
        window_2.geometry("300x300")
        window_2.title("Operators DFA")
        window_2.resizable(False, False)
        bg2 = PhotoImage(
            file="F:\second semster\design of compilers\images\images\\Operatorsssssss.png")
        lable2 = customtkinter.CTkLabel(master=window_2, image=bg2)
        lable2.place(x=0, y=0)

    if button_name == "Parser":
        label1 = tk.Label(root1, text='Scanner Phase', background="#201F23", fg="#479ECE")
        label1.config(font=('helvetica', 14))
        canvas1.create_window(200, 25, window=label1)

        label2 = tk.Label(root1, text='Source code:', background="#201F23", fg="#479ECE")
        label2.config(font=('helvetica', 10))
        canvas1.create_window(200, 100, window=label2)
        button1 = tk.Button(root1, text='Scan', bg="#201F23", fg="#201F23", font=('helvetica', 9, 'bold'),
                            command=lambda: Scan(), background="#479ECE")
        canvas1.create_window(200, 180, window=button1)
   #  button1.place(x=100,y=100)
    #   button1.event_add(Scan())


global checkbracket


def Scan():
    x1 = entry1.get()
    print("X1")
    print(x1)
    global checkbracket
    checkbracket = check(x1)
    find_token(x1)
    checkindict(check_tokens)
    print(len(Tokens))
    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
  # print(df)

    # to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    # start Parsing
    Node = Parse(x1)

    # to display errorlist
    df1 = pandas.DataFrame(errors)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()
    Node.draw()
    # clear your list

    # label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
    # canvas1.create_window(200, 210, window=label3)

    # label4 = tk.Label(root, text="Token_type"+x1, font=('helvetica', 10, 'bold'))
    # canvas1.create_window(200, 230, window=label4)


# # GUI


root.mainloop()

"""### """
