# -*- encoding: utf-8 -*-
"""
Author: Yousab Maged
Date: 21,Oct 2019
"""

from math import *
import pandas as pd


class BiSection:

    fn            = ''

    #fn is the f(x) which is a form input
    def __init__(self, fn):
        self.fn       = fn

    # Evaluate f(x)
    def f(self, x):
        #return (667.38/x)*(1-exp(-0.145843*x))-40
        return eval(self.fn)

    #Generate table values in (x,y) points, Get x lower and x upper
    #x param is the initial x from a form input
    #s param is the x incrementer step
    def generate_table(self, x, s):
        returnedValues = dict()
        table_dict={}
        fx, fx_old = 0, 0
        while fx*fx_old >= 0:
            fx_old = fx
            fx = self.f(x)
            table_dict[x] = self.f(x)
            x = x+s
        returnedValues['xl'] = x-2*s
        returnedValues['xu'] = x-s
        returnedValues['table'] = table_dict
        return returnedValues
        #bisect(xl, xu, 0.000001)

    def bisect_iter(self,xl,xu,iMax):
        iter=0
        while iter <= iMax:
            xm  = (xl+xu)/2
            fl= self.f(xl)
            fm = self.f(xm)
            test = fl * fm
            if test < 0:
                xu = xm
            elif test > 0:
                xl = xm
            else:
                break
            iter = iter +1
        xr = xm
        return xr

    def bisect_error(self,xl,xu,eValue):
        iter=0
        xm_old=0
        while True:
            xm  = (xl+xu)/2
            if abs(xm - xm_old) >= eValue:
                fl=self.f(xl)
                fm = self.f(xm)
                test = fl * fm
                if test < 0:
                    xu = xm
                elif test > 0:
                    xl = xm
                else:
                    break
                iter = iter +1
            else:
                break
        xr = xm
        return xr

    #Apply the bisect algorithm
    #xl is the lower x bound value
    #xu is the upper x bound value
    def bisect(self,xl, xu, es):
        while True:
            xm = (xl+xu)/2
            fl = self.f(xl)
            fm = self.f(xm)
            test = fl * fm
            if test < 0:
                xu = xm
            elif test > 0:
                xl = xm
            else:
                break
        xr = xm
        return xr


class Secant:

    def __init__(self, fn_str):
        self.fn_str = str(fn_str)

    def fn(self, x):
        return eval(self.fn_str)

    def secant(self, x0, x1, iterr, err):
        i = 1
        table_dict = dict()
        returnedValues = dict()
        returnedValues['xl'] = x0
        returnedValues['xu'] = x1
        while True:
            try:
                table_dict[x0] = self.fn(x0)
                x_new = x1 - ((x1-x0) / (self.fn(x1) - self.fn(x0))) * self.fn(x1)
            except ZeroDivisionError:
                print("dividing by zero error")
            if abs(x_new - x1) <= err or i == iterr:
                table_dict[x_new] = self.fn(x_new)
                returnedValues['table'] = table_dict
                return x_new, i, returnedValues
            else:
                x0 = x1
                x1 = x_new
                i += 1

from numpy.linalg import norm
class fixedPoint:
    def __init__(self, equation_str):
        self.equation_str = str(equation_str)  # ex: x^5 + 2 * x^2 - 3
        return

    def get_new_x(self, x):
        new_x = eval(self.equation_str) + x
        return new_x

    def solve_fixed_point(self, x0, tol=10e-5, maxiter=100):
        e = 1
        i = 0
        xp = [x0]
        while e > tol and i < maxiter:
            new_x = self.get_new_x(x0)
            e = norm(x0 - new_x)
            x0 = new_x
            xp.append(x0)
            i += 1
        return x0, xp
