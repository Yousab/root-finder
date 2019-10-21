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
