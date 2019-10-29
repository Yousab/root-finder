# -*- encoding: utf-8 -*-
"""
Author: Yousab Maged
Date: 21,Oct 2019
"""

from math import *
import pandas as pd
from datetime import datetime


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
class FixedPoint:

    def __init__(self, equation_str):
        self.equation_str = str(equation_str)  # ex: x^5 + 2 * x^2 - 3
        return

    def f(self, x):
        res = eval(self.equation_str)
        return res

    def g(self, x):
        new_x = eval(self.equation_str) + x
        return new_x

    def solve_fixed_point(self, x0, tolerance=10e-5, maxiter=100):
        start_time = datetime.now()
        e = 1
        i = 0
        xp = [x0]
        fx = [self.f(x0)]
        returned_values = {'convergence': False}
        while i < maxiter:
            new_x = self.g(x0)
            e = abs(x0 - new_x)
            if e > 1:
                break
            x0 = new_x
            y = self.f(x0)
            xp.append(x0)
            fx.append(y)
            if abs(self.f(x0)) < tolerance:
                returned_values['convergence'] = True
                returned_values['x0'] = x0
                returned_values['xp'] = xp
                returned_values['fx'] = fx
                break
            i += 1
        end_time = datetime.now()
        returned_values['time'] = (end_time - start_time).microseconds
        return returned_values


# this is for testing
# fixedPoint = FixedPoint('2*(x**2)+5*x+2')
# for i in [2, 1, -1, -2]:
#     result = fixedPoint.solve_fixed_point(x0=i, tolerance=0.001, maxiter=100)
#     print(result)
#     print()
