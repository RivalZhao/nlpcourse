from collections import defaultdict

if(1 == 1 and None):
    print("true")
else:
    print("false")
default = None
key = 1
print(default or key, end='\n =============== \n')

i = 0
seq = ['one', 'two', 'three']
for element in seq:
    print(i, seq[i])
    i += 1

strings = ('puppy', 'kitten', 'puppy', 'puppy',
           'weasel', 'puppy', 'kitten', 'puppy')
counts = {}
counts = defaultdict(int)
for kw in strings:
    counts.setdefault(kw, 0)
    counts[kw] += 1
print(counts)
#counts = defaultdict(int)
print(counts['puppy'])
print(counts['puppy2'])