#!/usr/bin/env python3

"""
Copyright (c) 2018 Matthew Emerson

A simple python implementation of Huffman coding
"""

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

def frequencies(text):
    """Return a dict of frequencies for each letter found in text"""
    freq = {}
    for c in text:
        freq.setdefault(c, 0)
        freq[c] += 1
    return freq


class BitIter:
    """Used to iterate through through an int bit by bit. Includes a length to add left padding 0's"""

    def __init__(self, i, length):
        self.i = i
        # self.length = i.bit_length() + offset
        self.length = length

    def __iter__(self):
        self.current_bit = 0
        return self

    def __next__(self):
        if self.current_bit >= self.length:
            raise StopIteration
        b = (self.i >> (self.length - self.current_bit - 1)) & 1
        self.current_bit += 1
        return b

    def __repr__(self):
        return "{0:0{1}b}".format(self.i, self.length)


class HuffmanNode:
    """Nodes used in HuffmanTree"""

    def __init__(self, char_list, freq=0, left=None, right=None):
        """
        Creates a new node

        :param char_list: list of chars found in this node and below
        :param freq: The occurrences of all chars in char_list in the input
        :param left: The 1 node
        :param right: The 0 node
        """
        self.char_list = char_list
        self.freq = freq
        self.left = left
        self.right = right

    def __repr__(self):
        return "<HuffmanNode: char_list='{}', freq={}, left={}, right={}>".format(self.char_list, self.freq, self.left,
                                                                                  self.right)

    def __lt__(self, other):
        return self.freq < other.freq

    def __le__(self, other):
        return self.freq <= other.freq

    def __gt__(self, other):
        return self.freq > other.freq

    def __ge__(self, other):
        return self.freq >= other.freq


class HuffmanTree:
    """Sets up a Huffman Tree for encoding and decoding text"""
    graph_node_list = []

    def build_tree(self, text):
        """
        Users letter frequency found in text to construct the Huffman tree

        :param text: Input text to use for calculating letter frequencies
        """
        if not text:
            raise ValueError
        self.input = text
        self.char_freqs = frequencies(self.input)
        pqueue = PriorityQueue()
        for k, v in self.char_freqs.items():
            pqueue.push(HuffmanNode([k], v, None, None))
        """lay 2 phan tu nho nhat"""
        left = pqueue.pop()
        right = pqueue.pop()

        while left and right:
            """"Gop 2 node nho thanh 1 node lon hon va tiep tuc"""
            pqueue.push(HuffmanNode(left.char_list + right.char_list, left.freq + right.freq, left, right))
            left = pqueue.pop()
            right = pqueue.pop()

        self.head = left
        self.code_dict = {}
        for c in self.head.char_list:
            self.code_dict[c] = self.get_code(c)

    def encode_tree(self):
        """
        Serializes the dict of Huffman {char: (code_length, code)} into a bytes for reconstructing the tree
        :return: bytes of packed codes
        """
        if hasattr(self, 'encoded_tree'):
            return self.encoded_tree
        else:
            out = struct.pack("H", in_width)
            out += struct.pack("H", in_height)
            out += struct.pack("H", len(self.head.char_list))
            for i in self.head.char_list:
                length, code = self.get_code(i)
                # out += struct.pack("B", ord(i))
                out += struct.pack("B", i)
                out += struct.pack("B", length)
                out += struct.pack("H", code)
            return out

    def get_code(self, char):
        """
        Get the Huffman code for a character. If we already have a constructed code table, grab
        the character from self.code_dict, otherwise traverse the tree.

        :param char: Input char
        :return: Tuple of (code_length, code)
        """

        # Check if there's already a code_dict compiled and contains the search char
        if hasattr(self, 'code_dict'):
            if char in self.code_dict:
                return self.code_dict[char]
        code_string = ''
        # Otherwise build the code by traversing the tree
        n = self.head
        if not n.left and not n.right:
            length = 1
            code = 1
        else:
            length = 0
            code = 0
        while n.left or n.right:
            if n.left and char in n.left.char_list:
                code = (code << 1) | 1
                n = n.left
                length += 1
                code_string += '1'
                if not n.left and not n.right:
                    create_TreeLeaf(start=code_string[0:len(code_string) - 1], end=code_string, text=str(char)+': '+ code_string)
                elif code_string not in self.graph_node_list:
                    create_TreeNode(start=code_string[0:len(code_string)-1], end=code_string, text=code_string)
                    self.graph_node_list.append(code_string)
            elif n.right and char in n.right.char_list:
                code = (code << 1) | 0
                length += 1
                n = n.right
                code_string += '0'
                if not n.left and not n.right:
                    create_TreeLeaf(start=code_string[0:len(code_string) - 1], end=code_string, text=str(char)+': '+ code_string)
                elif code_string not in self.graph_node_list:
                    create_TreeNode(start=code_string[0:len(code_string) - 1], end=code_string, text=code_string)
                    self.graph_node_list.append(code_string)
        return length, code

    def get_graph(self):
        ###Graph the Huffman Tree
        with open('output/' + file_name + '_graph.dot', 'w') as f:
            f.write(dot.source)
        subprocess.call('dot -Tpng output/' + file_name + '_graph.dot -o output/image/' + file_name + '_graph.png', shell=True)
        ###install Graphviz && run 'dot -c' in cmd when get errors

    def get_code_string(self, char, n=None):
        """Get the binary Huffman code in string form (ex. '11001')"""
        if n is None:
            n = self.head
        if n.left is not None:
            if char in n.left.char_list:
                return '1' + self.get_code_string(char, n.left)
        if n.right is not None:
            if char in n.right.char_list:
                return '0' + self.get_code_string(char, n.right)
        return ''

    def get_char(self, code, max_length=0):
        """
        Given a code, traverses the tree to retrieve the character

        :param code: The binary code to search for
        :param max_length: The length of the code (used to generate left padding 0's)
        :return: Tuple of (Length of code, Character)
        """
        bits = BitIter(code, max_length)
        n = self.head
        length = 0
        for bit in bits:
            if not n:
                return None, None
            if not n.left and not n.right:
                # We reached a leaf, but there are more bits left
                break
            else:
                length += 1
                if bit == 1:
                    n = n.left
                else:
                    n = n.right
        if not n or n.left or n.right:
            # Node doesn't exist or node isn't a leaf
            return None, None
        else:
            # Reached a leaf
            return length, n.char_list[0]

    def encode(self, text, file):
        """
        Encodes input using the Huffman codes generated in the constructor

        Each code is inserted into a byte before being packed into bytes. If there is any
        overflow (the byte + code is larger then 8 bits) then the first 8 bits are packed
        and the byte is set to the remaining 8 bits. If there are any bits remaining, the last
        byte will be padded with 0's.

        Returns the output of encoding with the first byte being padding, the next two bytes
        being the length of data (in bytes), then the bytes.

        0               1               2               3
        0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |     Padding   |            Length             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |  Data (padded with 0's to the nearest byte)   |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

        :return: encoded output as bytes
        """
        output = self.encode_tree()
        byte = 0
        num_bits = 0
        total_length = 0
        for c in text:
            length, code = self.get_code(c)
            # Add the returned code to the byte
            byte = (byte << length) | code
            num_bits += length

            # Overflow - byte contains more then 8 bits
            if num_bits >= 8:
                overflow = num_bits - 8

                # Pack the first 8 bits
                output += struct.pack("B", byte >> overflow)
                total_length += 1

                # Set the byte to the remaining bits
                byte = byte & ((1 << overflow) - 1)
                num_bits = overflow

        if num_bits != 0:
            padding = 8 - num_bits

            # Pack any bits that are remaining
            output += struct.pack("B", byte << padding)
            total_length += 1
        fout = open(file, 'wb')
        fout.write(output)
        return output

    def decode(self, buf):
        """
        Decodes buf using the generated Huffman tree.

        The first byte should be the padding found at the end of the
        buffer. The next two bytes should be the total length of input in
        bytes.

        See encode

        :param buf: Binary buffer to decode
        :return: The decoded text
        """
        global in_width, in_height
        char_list = []
        codes = {}
        in_width = struct.unpack_from("H", buf)[0]
        in_height = struct.unpack_from("H", buf, 2)[0]
        header_length = struct.unpack_from("H", buf, 4)[0] * 4 + 2 + 4
        for i in range(6, header_length, 4):
            char, code_length, code = struct.unpack_from("BBH", buf, i)
            char_list.append(char)
            codes[char] = (code_length, code)
            # print(char)
        self.char_list = char_list
        self.code_dict = codes

        self.head = HuffmanNode([])
        print(self.code_dict.items())
        for k, v in self.code_dict.items():
            self.head.char_list.append(k)
            bits = BitIter(v[1], v[0])
            n = self.head
            for bit in bits:
                if bit == 1:
                    if not n.left:
                        n.left = HuffmanNode([k])
                    else:
                        n.left.char_list.append(k)
                    n = n.left
                else:
                    if not n.right:
                        n.right = HuffmanNode([k])
                    else:
                        n.right.char_list.append(k)
                    n = n.right

        total_length = len(buf) - header_length
        decoded_text = ''
        decoded_array = []
        previous_bits = 0
        previous_bits_length = 0
        i, count = 0, 0
        while True:
            # See if there is a code from the previous byte
            code_length, char = self.get_char(previous_bits, previous_bits_length)
            if code_length:
                # Found a code - calculate any left over bits
                decoded_text += str(char)
                decoded_array.append(char)
                count += 1
                if count > in_height * in_width:
                    break
                decoded_text += ' '
                previous_bits_length -= code_length
                mask = (1 << previous_bits_length) - 1
                previous_bits = previous_bits & mask
            else:
                # Didn't find a code - Unpack another byte
                if i > total_length - 1:
                    break
                previous_bits = (previous_bits << 8) | struct.unpack_from("B", buf, i + header_length)[0]
                previous_bits_length += 8
                i += 1

        return decoded_text, decoded_array

    def decode_file(self, filename):
        """
        Decodes buf using the generated Huffman tree.

        The first byte should be the padding found at the end of the
        buffer. The next two bytes should be the total length of input in
        bytes.

        See encode

        :param buf: Binary buffer to decode
        :return: The decoded text
        """
        global in_width, in_height
        file = open(filename, 'rb')
        buf = file.read()
        char_list = []
        codes = {}
        in_width = struct.unpack_from("H", buf)[0]
        in_height = struct.unpack_from("H", buf, 2)[0]
        header_length = struct.unpack_from("H", buf, 4)[0] * 4 + 2 + 4
        for i in range(6, header_length, 4):
            char, code_length, code = struct.unpack_from("BBH", buf, i)
            char_list.append(char)
            codes[char] = (code_length, code)
            # print(char)
        self.char_list = char_list
        self.code_dict = codes

        self.head = HuffmanNode([])
        print(self.code_dict.items())
        for k, v in self.code_dict.items():
            self.head.char_list.append(k)
            bits = BitIter(v[1], v[0])
            n = self.head
            for bit in bits:
                if bit == 1:
                    if not n.left:
                        n.left = HuffmanNode([k])
                    else:
                        n.left.char_list.append(k)
                    n = n.left
                else:
                    if not n.right:
                        n.right = HuffmanNode([k])
                    else:
                        n.right.char_list.append(k)
                    n = n.right

        total_length = len(buf) - header_length
        decoded_text = ''
        decoded_array = []
        previous_bits = 0
        previous_bits_length = 0
        i, count = 0, 0
        while True:
            # See if there is a code from the previous byte
            code_length, char = self.get_char(previous_bits, previous_bits_length)
            if code_length:
                # Found a code - calculate any left over bits
                decoded_text += str(char)
                decoded_array.append(char)
                count += 1
                if count > in_height * in_width - 1:
                    break
                decoded_text += ' '
                previous_bits_length -= code_length
                mask = (1 << previous_bits_length) - 1
                previous_bits = previous_bits & mask
            else:
                # Didn't find a code - Unpack another byte
                if i > total_length - 1:
                    break
                previous_bits = (previous_bits << 8) | struct.unpack_from("B", buf, i + header_length)[0]
                previous_bits_length += 8
                i += 1

        return decoded_text, decoded_array

    def print_code_table(self):
        """Prints a table of all characters, codes, and code lengths found in the input"""
        for i in self.head.char_list:
            length, code = self.get_code(i)
            print("'{0}'\t\t{1}\t\t{1:0{2}b}".format(i, code, length))

    def __repr__(self):
        return "<HuffmanTree: head={}>".format(self.head)

def read_image(path, type, width=None, height=None):
    img_array = []
    img_src = cv.imread(path + '.' + type)
    if (width is not None) and (height is not None):
        img_src = cv.resize(img_src, (width, height))
    img_src = cv.cvtColor(img_src, cv.COLOR_BGR2GRAY)
    # img_src = cv.equalizeHist(img_src)
    img_src = 350 - img_src
    cv.imwrite(path + '_gray.' + type, img_src)
    (img_width, img_height) = img_src.shape
    img_1d = img_src.reshape(img_width * img_height)
    print(str(img_width) + ' ' + str(img_height))
    for c in img_1d:
        img_array.append(c)
    return img_array, img_width, img_height


if __name__ == "__main__":
    global in_width, in_height, str_size, file_name
    file_name = 'tb'
    in_str, in_width, in_height = read_image('data/' + file_name, 'jpg')
    # print("Original text: {}\n".format(in_str))
    tree = HuffmanTree()
    tree.build_tree(in_str)
    encoded_text = tree.encode(in_str, 'encoded/' + file_name + '_encoded.dat')
    tree.get_graph()
    print("Encoded text: {}\n".format(" ".join("{:02x}".format(c) for c in encoded_text)))
    tree.print_code_table()
    new_tree = HuffmanTree()
    # decoded_text, decoded_array = new_tree.decode(encoded_text)
    decoded_text, decoded_array = new_tree.decode_file('encoded/' + file_name + '_encoded.dat')
    decoded_array = np.reshape(decoded_array, (in_width, in_height))
    decoded_img = np.array(decoded_array, dtype=np.uint8)
    cv.imshow('Decoded_image', decoded_img)
    cv.waitKey(0)
    # print("Decoded text: {}\n".format(decoded_text))
    print("Total length of input (in bytes): {}".format(in_height * in_width))
    # print("Total length of encoded text (in bytes): {}".format(len(encoded_text)))
    # print("Compression ratio: {}:1".format(str_size / len(encoded_text)))
