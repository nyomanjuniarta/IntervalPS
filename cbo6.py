"""
FCA - Python libraries to support FCA tasks
Copyright (C) 2017  Victor Codocedo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import print_function
import argparse
from IntervalPattern6 import MaxLengthIntervalPattern, dict_printer, PSCbO
from fca.io.transformers import List2IntervalsTransformer
from fca.io.input_models import FormalContextModel
from time import time


def exec_ex6(filepath, theta, min_col):
    """
    Execute CbO over pattern structures

    Notice that the algorithm is different and it also works differently
    PSCbO lists objects one by one, in a bottom-up way
    """
    fctx = FormalContextModel(filepath=filepath, transformer=List2IntervalsTransformer(int))
    MaxLengthIntervalPattern.THETA = theta
    MaxLengthIntervalPattern.MIN_COL = min_col
    dict_printer(PSCbO(fctx, pattern=MaxLengthIntervalPattern, lazy=False, silent=False).poset, transposed=True)


if __name__ == '__main__':
    start_time = time()
    __parser__ = argparse.ArgumentParser(description='Example 6 - Interval with theta value with CbO')
    __parser__.add_argument('context_path', metavar='context_path', type=str, help='path to the formal context')
    __parser__.add_argument('-t', '--theta', metavar='theta', type=int, help='Maximal length for intervals [0,inf]', default=0)
    __parser__.add_argument('-c', '--min_col', metavar='min_col', type=int, help='Minimal number of columns in a bicluster', default=0)
    __args__ = __parser__.parse_args()
    exec_ex6(__args__.context_path, __args__.theta, __args__.min_col)
    end_time = time()
    print(end_time - start_time)
# okay decompiling ex6_cbo_ps.pyc
