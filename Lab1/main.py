def prefix_function(s: str):
    n = len(s)
    pi = [0 for i in range(n)]
    for i in range(1, n):
        j = pi[i-1]
        while j > 0 and s[i] != s[j]:
            j = pi[j-1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi

def kmp(pattern: str, text: str):
    pi = prefix_function(pattern)
    ops_cnt = 0
    j = 0
    n = len(text)
    k = len(pattern)
    for i in range(n):
        old_j = j
        while j > 0 and text[i] != pattern[j]:
            ops_cnt += 1
            j = pi[j-1]
        if j != old_j:
            ops_cnt -= 1
        if text[i] == pattern[j]:
            ops_cnt += 1
            j += 1
        if j == k:
            return i - j + 1, ops_cnt
    return -1


def naive(pattern: str, text: str):
    """Возвращает индекс первого вхождения
        подстроки в строку и количество операций"""
    p_len = len(pattern)
    t_len = len(text)
    ops_cnt = 0
    for i in range(t_len - p_len + 1):
        found_flag = True
        for j in range(i, i + p_len):
            ops_cnt += 1
            if text[j] != pattern[j - i]:
                found_flag = False
                break
        if found_flag:
            return i, ops_cnt
    return -1


def boyer_moore(pattern, text):
    """Возвращает индекс первого вхождения
        подстроки в строку и количество операций"""
    p_len = len(pattern)
    t_len = len(text)
    ops_cnt = 0
    if p_len > t_len:
        return -1
    image = {}
    num = 0
    for char in reversed(pattern[:-1]):
        num += 1
        if char not in image:
            image[char] = num
    if pattern[-1] not in image:
        image[pattern[-1]] = p_len

    offset = 0
    text_idx = offset + p_len - 1
    while text_idx < t_len:
        pattern_idx = p_len - 1
        ops_cnt += 1
        while text[text_idx] == pattern[pattern_idx] and pattern_idx >= 0:
            ops_cnt += 1
            text_idx -= 1
            pattern_idx -= 1
        if pattern_idx != p_len - 1:
            ops_cnt -= 1
        if pattern_idx == -1:
            return offset, ops_cnt
        else:
            key_char = text[offset + p_len - 1]
            if key_char in image:
                offset += image[key_char]
            else:
                offset += p_len
        text_idx = offset + p_len - 1
    return -1


def find_substr(method, pattern, text):
    """Возвращает индекс первого вхождения
        подстроки в строку, количество операций и время,
        за которое отработала функция method"""
    import time
    start = time.time()
    index, operations = method(pattern, text)
    end = time.time()
    time = (end - start)
    return index, operations, time


files_list = []
for i in range(1, 5):
    files_list.append((f'bad_t_{i}.txt', f'bad_w_{i}.txt'))
    files_list.append((f'good_t_{i}.txt', f'good_w_{i}.txt'))


with open('output.txt', 'w') as output:
    for text_file, pattern_file in files_list:
        print(text_file, pattern_file, file=output)
        with open(f'./benchmarks/{text_file}', 'r', encoding='utf8') as t_file:
            with open(f'./benchmarks/{pattern_file}', 'r', encoding='utf8') as p_file:
                text = t_file.read()
                pattern = p_file.read()

                print('--------------------------', file=output)
                index, operations, time = find_substr(naive, pattern, text)
                print('Naive algorithm:', file=output)
                print(f'Index: {index}', file=output)
                print(f'Operations count: {operations}', file=output)
                print(f'Time in seconds: {time}', file=output)

                print('--------------------------', file=output)
                index, operations, time = find_substr(boyer_moore, pattern, text)
                print('Boyer-Moore algorithm:', file=output)
                print(f'Index: {index}', file=output)
                print(f'Operations count: {operations}', file=output)
                print(f'Time in seconds: {time}', file=output)

                print('--------------------------', file=output)
                index, operations, time = find_substr(kmp, pattern, text)
                print('Knuth-Morris-Pratt algorithm:', file=output)
                print(f'Index: {index}', file=output)
                print(f'Operations count: {operations}', file=output)
                print(f'Time in seconds: {time}', file=output)

                print('--------------------------', file=output)
                print(f'Index according to python string.find(): {text.find(pattern)}\n\n\n', file=output)