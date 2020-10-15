import pygraphviz as pgv

d={'1': {'2': None}, '2': {'1': None, '3': None}, '3': {'2': None}}
G=pgv.AGraph(d)

G.layout(prog='dot')


G.draw('file.png')