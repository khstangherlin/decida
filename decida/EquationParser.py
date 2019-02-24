################################################################################
# CLASS    : EquationParser
# PURPOSE  : simple equation parser class
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:20:03 2013
# -----------------------------------------------------------------------------
# NOTES    :
#
# LICENSE  : (BSD-new)
#
# This software is provided subject to the following terms and conditions,
# which you should read carefully before using the software.  Using this
# software indicates your acceptance of these terms and conditions.  If you
# do not agree with these terms and conditions, do not use the software.
#
# Copyright (c) 2013 Richard Booth. All rights reserved.
#
# Redistribution and use in source or binary forms, with or without
# modifications, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following Disclaimer
#       in each human readable file as well as in the documentation and/or
#       other materials provided with the distribution.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following Disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Richard Booth nor the names of contributors
#       (those who make changes to the software, documentation or other
#       materials) may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# Disclaimer
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, INFRINGEMENT AND THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# ANY USE, MODIFICATION OR DISTRIBUTION OF THIS SOFTWARE IS SOLELY AT THE
# USERS OWN RISK.  IN NO EVENT SHALL RICHARD BOOTH OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, INCLUDING,
# BUT NOT LIMITED TO, CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# IN NO EVENT SHALL THE AUTHORS OR DISTRIBUTORS BE LIABLE TO ANY PARTY
# FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
# ARISING OUT OF THE USE OF THIS SOFTWARE, ITS DOCUMENTATION, OR ANY
# DERIVATIVES THEREOF, EVEN IF THE AUTHORS HAVE BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# THE AUTHORS AND DISTRIBUTORS SPECIFICALLY DISCLAIM ANY WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.  THIS SOFTWARE
# IS PROVIDED ON AN "AS IS" BASIS, AND THE AUTHORS AND DISTRIBUTORS HAVE
# NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
# MODIFICATIONS.
################################################################################
from __future__ import print_function
from builtins import str
from builtins import range
from builtins import object
import re
import functools

class EquationParser(object) :
    """
    **synopsis**:

        Equation parser class.

        *EquationParser* parses a general algebraic equation, involving
        numbers, variables, unary and binary operations, and parentheses.
        It returns a set of simpler, parsed (space-separated) equations with
        only 1, 2, or 3 token right-hand-side expressions: assignments, unary
        operations, binary operations.

    **constructor arguments**:

        **equation** (str)

            lhs=rhs string to be parsed

        **postfix** (bool, default=False)

            if True, generate postfix notation, otherwise infix

        **varlist** (list of str, default=None)

            list of variables which are to be treated specially:
            if variable contains meta-character, it is replaced
            with a temporary name, then after parsing, re-replaced.

        **debug** (bool, default=False)

            if True, print out parsing information

        **data_function_format** (bool, default=True)

            if True, print out functions in Data-object-compatible
            format.

    **operator precedence** (low to high)::

            && ||
            < <= == != >= >
            + -   (add, sub)
            * / %
            + - ! (unary)
            ^

    **example**:

        >>> from decida.EquationParser import EquationParser
        >>> ep = EquationParser("z =V(1)* sin(x+3.0)*ID(mp2)",
        ... varlist=["V(1)", "ID(mp2)"])
        >>> eqns = ep.parse()
        >>> for eqn in eqns :
        >>>     print eqn
        zz1003 = x + 3.0
        zz1004 = sin zz1003
        zz1005 = V(1) * zz1004
        z = zz1005 * ID(mp2)

    **public methods**:

    """
    isym_re = "[a-zA-Z_$][a-zA-Z0-9_$]*"
    inum_re = "([0-9]+[.]?[0-9]*|[.][0-9]+)([eE][+-]?[0-9]+)?"
    iopn_re = "[-+*/^%]"
    ilog_re = "(<=|==|!=|>=|<|>|\|\||\&\&|!)"
    isep_re = "[()=,]"
    ichk_re = "^(%s|%s|%s|%s|%s)" % \
        (isym_re, inum_re, iopn_re, ilog_re, isep_re)
    num_re  = "^%s$" % (inum_re)
    sym_re  = "^%s$" % (isym_re)
    #=========================================================================
    # METHOD: __init__
    # NOTES:
    #   * data_function_format:
    #      Data object set_parsed format: sin(x) -> sin x
    #=========================================================================
    def __init__(self, equation, postfix=False, varlist=None,
        debug=False, data_function_format=True) :
        self.__equation = equation
        self.__postfix = postfix
        self.__stack   = []
        self.__tokens  = []
        self.__tok     = ""
        self.__uniq    = 1000
        self.__result  = []
        self.__varlist = varlist
        self.__Key2Var = {}
        self.__debug   = debug
        self.__data_function_format = data_function_format
        self.__equation_tokenized = ""
    #=========================================================================
    # METHOD: __tokenize
    #=========================================================================
    def __tokenize(self, line) :
        copy = line
        line = line.strip()
        line = re.sub(" ", "", line)
        if self.__debug :
            print("tokenize line:", line)
        lout = []
        while line :
            m = re.search(EquationParser.ichk_re, line)
            if m :
                word = m.group(1)
                lout.append(word)
                n = len(word)
                line = line[n:]
            else :
                print("character \"%s\" not recognized in line:\n%s" % (line[0], copy))
                return None
        if self.__debug :
            print("tokenized:", lout)
        return lout
    #==========================================================================
    # METHOD : __vars_sort
    # PURPOSE : sort variable names
    #==========================================================================
    def __vars_sort(self, var1, var2) :
        if   len(var1) > len(var2) :
            return -1
        elif len(var1) < len(var2) :
            return 1
        elif var1 > var2 :
            return 1
        elif var1 < var2 :
            return -1
        return 0
    #=========================================================================
    # METHOD: __map_vars
    # PURPOSE: map variables with possible meta-chars to other symbols
    #=========================================================================
    def __map_vars(self) :
        m=re.search("^([^=]+)=(.+)$", self.__equation)
        if not m :
            print("equation not in right format: LHS = RHS")
            return None
        lhs = m.group(1)
        rhs = m.group(2)
        lhs = lhs.strip()
        rhs = rhs.strip()
        if re.search("[/().-\[\]]", lhs):
            key  = self.__intvar()
            self.__Key2Var[key] = lhs
            lhs  = key
        if self.__varlist is not None :
            var_list = self.__varlist
            var_list.sort(key=functools.cmp_to_key(self.__vars_sort))
            for i, var in enumerate(var_list) :
                evar = re.escape(var)
                if re.search("[/().-\[\]]", evar):
                    key  = self.__intvar()
                    self.__Key2Var[key] = var
                    if self.__debug :
                        print("map %s to %s" % (var, key))
                    rhs = re.sub(evar, key, rhs)
        return "%s=%s" % (lhs, rhs)
    #=========================================================================
    # METHOD: __unmap_vars
    #=========================================================================
    def __unmap_vars(self) :
        olist = []
        for line in self.__result :
            toks = line.split()
            lout = []
            for tok in toks :
                if tok in self.__Key2Var :
                    tok = self.__Key2Var[tok]
                lout.append(tok)
            olist.append(" ".join(lout))
        return olist
    #=========================================================================
    # METHOD: parse
    #=========================================================================
    def parse(self) :
        """ parse the equation and return the result.

        **results**:

            * return set of parsed equations with tokenized right-hand-side
              expressions of 1, 2 or 3 (space-separated) tokens.

        """
        self.__stack  = []
        self.__result = []
        line = self.__map_vars()
        self.__tokens = self.__tokenize(line)
        self.__tokens.append("\n")
        self.__equation_tokenized = " ".join(self.__tokens)
        self.__tok    = self.__tokens.pop(0)
        self.__assignment()
        return self.__unmap_vars()
    #=========================================================================
    # METHOD: ivars
    # PURPOSE: return list of intermediate variables (in current result)
    #=========================================================================
    def ivars(self) :
        """ return list of intermediate variables in the current result.

        **results** :

            * Lists all the intermediate lhsvars created in the set
              of parsed equations.

        """
        olist = []
        for line in self.__result :
            toks = line.split()
            olist.append(toks[0])
        if olist :
            olist.pop(-1)
        return olist
    #=========================================================================
    # METHOD: __intvar
    #=========================================================================
    def __intvar(self):
        self.__uniq += 1
        return "zz%d" % (self.__uniq)
    #=========================================================================
    # METHOD: __isnum
    #=========================================================================
    def __isnum(self, s) :
        if re.search(EquationParser.num_re, s) :
            return True
        return False
    #=========================================================================
    # METHOD: __issym
    #=========================================================================
    def __issym(self, s) :
        if re.search(EquationParser.sym_re, s) :
            return True
        return False
    #=========================================================================
    # METHOD: __iszero
    #=========================================================================
    def __iszero(self, s) :
        if self.__isnum(s) :
            return eval("%s == 0.0" % (s))
        return False
    #=========================================================================
    # METHOD: __isone
    #=========================================================================
    def __isone(self, s) :
        if self.__isnum(s) :
            return eval("%s == 1.0" % (s))
        return False
    #=========================================================================
    # METHOD: __ishalf
    #=========================================================================
    def __ishalf(self, s) :
        if self.__isnum(s) :
            return eval("%s == 0.5" % (s))
        return False
    #=========================================================================
    # METHOD: __unop
    #=========================================================================
    def __unop(self, a, op) :
        if   self.__isnum(a) :
            x = eval("%s %s" % (op, a))
            return str(x)
        if len(a.split()) > 1:
            a = "( %s )" % (a)
        return "%s %s" % (op, a)
    #=========================================================================
    # METHOD: __binop
    #=========================================================================
    def __binop(self, a, b, op) :
        if   self.__isnum(a) and self.__isnum(b) :
            if op == "^" :
                x = eval("pow(%s, %s)" % (a, b))
            else :
                x = eval("%s %s %s" % (a, op, b))
            return str(x)
        if   op == "+" :
            if   self.__iszero(a) :
                return b
            elif self.__iszero(b) :
                return a
            elif self.__issym(a) and self.__issym(b) and a == b :
                return "2 * %s" % (a)
        elif op == "-" :
            if   self.__iszero(a) :
                return "- %s" % (b)
            elif self.__iszero(b) :
                return a
            elif self.__issym(a) and self.__issym(b) and a == b :
                return "0"
        elif op == "*" :
            if   self.__iszero(a) :
                return "0"
            elif self.__iszero(b) :
                return "0"
            elif self.__isone(a) :
                return b
            elif self.__isone(b) :
                return a
        elif op == "/" :
            if   self.__iszero(a) :
                return "0"
            elif self.__isone(b) :
                return a
            elif self.__issym(a) and self.__issym(b) and a == b :
                return "1"
        elif op == "^" :
            if   self.__isone(a) :
                return "1"
            elif self.__iszero(b) :
                return "1"
            elif self.__isone(b) :
                return a
            elif self.__ishalf(b) :
                return "sqrt ( %s ) " % (a)
        if len(a.split()) > 1:
            a = "( %s )" % (a)
        if len(b.split()) > 1:
            b = "( %s )" % (b)
        return "%s %s %s" % (a, op, b)
    #=========================================================================
    # METHOD: __expect
    #=========================================================================
    def __expect(self, tok_expected) :
        ok = True
        if self.__debug :
            print("expect %s see %s" % (tok_expected, self.__tok))
        if   tok_expected == "number" :
            ok = self.__isnum(self.__tok)
        elif tok_expected == "symbol" :
            ok = self.__issym(self.__tok)
        else :
            ok = (self.__tok == tok_expected)
        if not ok :
            print("expected %s but saw %s" % (tok_expected, self.__tok))
        otok = self.__tok
        if self.__tokens :
            self.__tok = self.__tokens.pop(0)
        else :
            self.__tok = ""
        return otok
    #=========================================================================
    # METHOD: __assignment
    #=========================================================================
    def __assignment(self) :
        lhs = self.__expect("symbol")
        if self.__postfix :
            self.__result.append(lhs)
        op  = self.__expect("=")
        self.__expression()
        if self.__postfix :
            self.__result.append(op)
        else :
            rhs = self.__stack.pop(-1)
            self.__result.append("%s = %s" % (lhs, rhs))
            #----------------------------------
            # eliminate lhs = intvar line
            #----------------------------------
            if len(self.__result) > 1 :
                self.__result.pop(-1)
                last = self.__result.pop(-1)
                rhs  = " ".join(last.split()[2:])
                self.__result.append("%s = %s" % (lhs, rhs))
    #=========================================================================
    # METHOD: __expression
    #=========================================================================
    def __expression(self) :
        self.__log_expression()
        ops = ("&&", "||")
        while self.__tok in ops :
            op = self.__expect(self.__tok)
            self.__log_expression()
            if self.__postfix :
                self.__result.append(op)
            else :
                a2  = self.__stack.pop(-1)
                a1  = self.__stack.pop(-1)
                lhs = self.__intvar()
                rhs = self.__binop(a1, a2, op)
                self.__stack.append(lhs)
                self.__result.append("%s = %s" % (lhs, rhs))
    #=========================================================================
    # METHOD: __log_expression
    #=========================================================================
    def __log_expression(self) :
        self.__relational()
        ops = ("<=", "<", "==", "!=", ">", ">=")
        while self.__tok in ops :
            op = self.__expect(self.__tok)
            self.__relational()
            if self.__postfix :
                self.__result.append(op)
            else :
                a2  = self.__stack.pop(-1)
                a1  = self.__stack.pop(-1)
                lhs = self.__intvar()
                rhs = self.__binop(a1, a2, op)
                self.__stack.append(lhs)
                self.__result.append("%s = %s" % (lhs, rhs))
    #=========================================================================
    # METHOD: __relational
    #=========================================================================
    def __relational(self) :
        self.__term()
        while self.__tok in ["+", "-"] :
            op = self.__expect(self.__tok)
            self.__term()
            if self.__postfix :
                self.__result.append(op)
            else :
                a2  = self.__stack.pop(-1)
                a1  = self.__stack.pop(-1)
                lhs = self.__intvar()
                rhs = self.__binop(a1, a2, op)
                self.__stack.append(lhs)
                self.__result.append("%s = %s" % (lhs, rhs))
    #=========================================================================
    # METHOD: __term
    #=========================================================================
    def __term(self) :
        self.__ufact()
        ops = ("*", "/", "%")
        while self.__tok in ops :
            op = self.__expect(self.__tok)
            self.__ufact()
            if self.__postfix :
                self.__result.append(op)
            else :
                a2  = self.__stack.pop(-1)
                a1  = self.__stack.pop(-1)
                lhs = self.__intvar()
                rhs = self.__binop(a1, a2, op)
                self.__stack.append(lhs)
                self.__result.append("%s = %s" % (lhs, rhs))
    #=========================================================================
    # METHOD: __ufact
    #=========================================================================
    def __ufact(self) :
        ops = ("+", "-", "!")
        if self.__tok in ops :
            op = self.__expect(self.__tok)
            self.__fact()
            if op in ["-", "!"] :
                if self.__postfix :
                    self.__result.append(op)
                else :
                    a1  = self.__stack.pop(-1)
                    lhs = self.__intvar()
                    rhs = self.__unop(a1, op)
                    self.__stack.append(lhs)
                    self.__result.append("%s = %s" % (lhs, rhs))
        else :
            self.__fact()
    #=========================================================================
    # METHOD: __fact
    #=========================================================================
    def __fact(self) :
        self.__factor()
        if self.__tok == "^" :
            op = self.__expect(self.__tok)
            self.__factor()
            if self.__postfix :
                self.__result.append(op)
            else :
                a2  = self.__stack.pop(-1)
                a1  = self.__stack.pop(-1)
                lhs = self.__intvar()
                rhs = self.__binop(a1, a2, op)
                self.__stack.append(lhs)
                self.__result.append("%s = %s" % (lhs, rhs))
    #=========================================================================
    # METHOD: __factor
    #=========================================================================
    def __factor(self) :
        if self.__isnum(self.__tok) :
            num = self.__expect("number")
            if self.__postfix :
                self.__result.append(num)
            else :
                self.__stack.append(num)
        elif self.__issym(self.__tok) :
            sym = self.__expect("symbol")
            if self.__tok != "(" :
                if self.__postfix :
                    self.__result.append(sym)
                else :
                    self.__stack.append(sym)
            else :
                fn = sym
                self.__expect("(")
                self.__expression()
                n = 1
                while self.__tok == "," :
                    n += 1
                    self.__expect(",")
                    self.__expression()
                self.__expect(")")
                if self.__postfix :
                    fn = "%s(%d)" % (fn, n)
                    self.__result.append(fn)
                else :
                    args = []
                    for i in range(0, n) :
                        args.append(self.__stack.pop(-1))
                    args.reverse()
                    self.__stack.append(self.__intvar())
                    lhs = self.__stack[-1]
                    if self.__data_function_format :
                        if   len(args) == 1:
                            x = args[0]
                            self.__result.append("%s = %s %s" % (lhs, fn, x))
                        elif len(args) == 2:
                            y = args[0]
                            x = args[1]
                            self.__result.append("%s = %s %s %s" % (lhs, y, fn, x))
                    else :
                        args = ",".join(args)
                        self.__result.append("%s = %s ( %s )" % (lhs, fn, args))
        elif self.__tok == "(" :
            self.__expect("(")
            self.__expression()
            self.__expect(")")
        else :
            print("unexpected syntax in %s" % (self.__equation_tokenized))
