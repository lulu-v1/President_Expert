import tkinter as tk

import numpy as np


def ex1():
    print("Ex1")
    a = np.floor(10 * np.random.randn(3, 4))
    print(a)
    a = a.reshape(6, 2)
    print(a)


def ex2():
    print("Ex2")
    a = np.floor(10 * np.random.randn(3, 4))
    print(a)
    a = a.flatten()
    print(a)


def ex3():
    print("Ex3")
    a = np.arange(40)
    print(a.reshape(5, 4, -1))


def ex4():
    a = np.floor(10 * np.random.randn(2, 2))
    b = np.floor(10 * np.random.randn(2, 2))

    print("Array a:\n", a)
    print("Array b:\n", b)

    vertical_stack = np.vstack((a, b))
    print("Vertical stack:\n", vertical_stack)

    horizontal_stack = np.hstack((a, b))
    print("Horizontal stack:\n", horizontal_stack)


if __name__ == "__main__":
    ex4()
