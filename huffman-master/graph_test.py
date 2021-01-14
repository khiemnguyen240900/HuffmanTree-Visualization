import struct, os, subprocess

from priority_queue import PriorityQueue

import cv2 as cv
import numpy as np

from graphviz import Digraph
from sympy import *

init_printing()
dot = Digraph(comment='Huffman Tree')

def create_TreeNode(start=None, end=None, text=None):
    dot.node(end, text, shape='doublecircle')
    dot.edge(start, end)


def create_TreeLeaf(start=None, end=None, text=None):
    dot.node(end, text, shape='invhouse', color='black', fillcolor='yellow', style='filled')
    dot.edge(start, end)


def convert(char_array):
    return "".join(char_array)

def graphTree():
    ###Graph the Huffman Tree
    with open('output/graph.dot', 'w') as f:
        f.write(dot.source)
    subprocess.call('dot -Tpng output/graph.dot -o output/image/graph.png', shell=True)
    ###install Graphviz && run 'dot -c' in cmd when get errors

create_TreeNode(start='1',end='10',text='10')