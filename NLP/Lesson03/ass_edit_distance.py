from functools import lru_cache

solution = {}


@lru_cache(maxsize=2 ** 10)
def edit_distance(string1, string2):
    if len(string1) == 0: return len(string2)
    if len(string2) == 0: return len(string1)

    tail_s1 = string1[-1]
    tail_s2 = string2[-1]

    candidates = [
        (edit_distance(string1[:-1], string2) + 1, 'DEL {}'.format(tail_s1)),  # string 1 delete tail
        (edit_distance(string1, string2[:-1]) + 1, 'ADD {}'.format(tail_s2)),  # string 1 add tail of string2
    ]

    if tail_s1 == tail_s2:
        both_forward = (edit_distance(string1[:-1], string2[:-1]) + 0, '')
    else:
        both_forward = (edit_distance(string1[:-1], string2[:-1]) + 1, 'SUB {} => {}'.format(tail_s1, tail_s2))

    candidates.append(both_forward)

    min_distance, operation = min(candidates, key=lambda x: x[0])

    solution[(string1, string2)] = operation

    return min_distance


def parse_solution(str1, str2):
    if len(str1) == 0 and len(str2) == 0:
        return ''
    temp_str = solution[(str1, str2)]
    temp_str1 = str1
    temp_str2 = str2
    if temp_str.find('ADD') > -1:
        temp_str2 = str2[:-1]
        temp_str += "  " + str1 + str2[-1]
    elif temp_str.find('DEL') > -1:
        temp_str1 = str1[:-1]
        temp_str += "  " + temp_str1
    elif temp_str.find('SUB') > -1:
        temp_str2 = str2[:-1]
        temp_str1 = str1[:-1]
        temp_str += "  " + str1[:-1] + str2[-1]
    else:
        temp_str2 = str2[:-1]
        temp_str1 = str1[:-1]
        temp_str += str1
    parse_solution(temp_str1, temp_str2)
    return parse_solution(temp_str1, temp_str2) + ' \n ' + temp_str

print(edit_distance('ABCDEG', 'ABCCEFH'))
print(solution)
print(parse_solution('ABCDEG', 'ABCCEFH'))