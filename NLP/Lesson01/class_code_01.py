import random


def adj(): return random.choice('蓝色的|好看的|小小的'.split('|'))


def adj_star():
    return random.choice([None, adj() + adj()])


'''----------------------------------------'''


adj_grammar = '''
sentence => noun_phrase verb_phrase
noun_phrase => Article Adj* noun
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>  蓝色的 | 好看的 | 小小的
'''



def create_grammar(grammar_str):
    grammar = {}
    for line in grammar_str.split('\n'):
        if not line.strip():
            continue
        exp, stmt = line.split('=>')
        grammar[exp.strip()] = [s.strip().split() for s in stmt.split('|')]
    return grammar

#print(grammar['Adj*'])

def generate(gram, target):
    if target not in gram:
        return target
    else:
        expaned = [generate(gram, t) for t in random.choice(gram[target])]
        return ''.join([e for e in expaned if e != 'null'])

example_grammar = create_grammar(adj_grammar)
print(example_grammar)

#print(generate(example_grammar, 'sentence'))

