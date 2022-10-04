
def term_in_region(term1, term2):
    for i in range(len(term1)):
        if term2[i] is None:
            continue
        else:
            if term2[i] != term1[i]:
                return False

    return True


def no_of_regions(term, prev_output):
    count = 0
    for x in prev_output:
        if term_in_region(term, x):
            count += 1

    return count


def one_in_region(region, func_DC):
    count = 0
    for x in func_DC:
        if term_in_region(x, region):
            count += 1

    return count


def ans_function(func_TRUE, func_DC, prev_output):
    augmented_func_TRUE = []
    for i in range(len(func_TRUE)):
        x = func_TRUE[i]
        augmented_func_TRUE.append((no_of_regions(x, prev_output), i, x))

    augmented_func_TRUE.sort()
    return augmented_func_TRUE



def demo_assign_3(term, output):
    indices_matched = []
    term_contained_demo = []
    for i_demo in range(len(output)):
        x = output[i_demo]
        flag = False
        for j_demo in range(len(term)):
            if j_demo not in indices_matched and term[j_demo] == x[j_demo]:
                flag = True
                indices_matched.append(j_demo)

        if flag:
            term_contained_demo.append(x)

    return term_contained_demo

def opt_function_reduce(func_TRUE, func_DC):
    #Considering a minterm, and removing all other 1's in its maximally expanded region
    #We augment the number of ones together with the func_TRUE list to select the region with maximum number of ones
    all_1_prev_terms = comb_function_expansion(func_TRUE, func_DC)
    for i in range(len(func_TRUE)):
        func_TRUE[i] = term_to_list(func_TRUE[i])
    setform = set()
    for q in all_1_prev_terms:
        setform.add(tuple(q))
    augmented_func_TRUE = ans_function(func_TRUE, func_DC, setform)

    i = 0
    rem = set()
    ans = []
    ans_demo = []
    term_removed_demo = []
    term_contained_demo = []
    while i < len(augmented_func_TRUE):
        j = i + 1
        if i in rem:
            i += 1
            continue
        while j < len(augmented_func_TRUE):
            if j not in rem:
                flag = term_in_region(augmented_func_TRUE[j][2], all_1_prev_terms[augmented_func_TRUE[i][1]])
                if flag == True:
                    rem.add(j)


            j += 1
        rem.add(i)
        ans_demo.append(all_1_prev_terms[augmented_func_TRUE[i][1]])
        ans.append(list_to_term(all_1_prev_terms[augmented_func_TRUE[i][1]]))
        i += 1

    for y in all_1_prev_terms:
        if y not in ans_demo and y not in term_removed_demo:
            term_removed_demo.append(y)

    for terms in term_removed_demo:
        term_contained_demo.append(demo_assign_3(terms, ans_demo))

    for v in range(len(term_removed_demo)):
        term_removed_demo[v] = list_to_term(term_removed_demo[v])

    for v in range(len(term_contained_demo)):
        for u in range(len(term_contained_demo[v])):
            term_contained_demo[v][u] = list_to_term(term_contained_demo[v][u])

    return ans




dictionary_language = {}
for i in range(0, 26):
    dictionary_language[chr(97 + i)] = i


def term_to_list(term):
    k = len(term)
    l = []
    p = 0
    while p < k:
        if p + 1 == k and term[k - 1] != "'":
            l.append(1)
            p += 1
        elif term[p + 1] == "'":
            l.append(0)
            p += 2
        else:
            l.append(1)
            p += 1
    return l


dictionary_storage = {}
dictionary_check = {}


def legal_check(dictionary_check, term, func_TRUE, func_DC, x, i):
    m = len(term)
    if 2 ** x > len(func_TRUE) + len(func_DC):
        return False

    if x == 0:
        return tuple(term) in dictionary_check

    term_1 = term[:]
    term_2 = term[:]
    ind = 0
    for j in range(i, m):
        if term[j] is None:
            term_1[j] = 0
            term_2[j] = 1
            ind = j
            break
    return legal_check(dictionary_check, term_1, func_TRUE, func_DC, x - 1, ind) and legal_check(dictionary_check,
                                                                                                 term_2, func_TRUE,
                                                                                                 func_DC, x - 1, ind)


count = 0


def find_max_region(term, func_TRUE, func_DC, x, l):
    # returns the maximally expanded term and its size
    global count
    func_all = func_TRUE + func_DC
    m = len(term)
    if x == m:
        l = term
        return term, 2 ** x
    if 2 ** x > len(func_all):
        l = term
        return term, 2 ** x

    if tuple(term) in dictionary_storage:
        return dictionary_storage[tuple(term)]

    # print(term)
    max_size = 2 ** x  # current size
    initial_term = term
    j = None
    new_expanded_term = term
    for i in range(m):
        term_2 = term.copy()
        if not (term[i] is None):
            term_2[i] = None
        else:
            continue

        if legal_check(dictionary_check, term_2, func_TRUE, func_DC, x + 1, 0):

            max_size_new = find_max_region(term_2, func_TRUE, func_DC, x + 1, l)
            count_2 = count + 1
            count = count_2
            if max_size < max_size_new[1] or (max_size == max_size_new[1] and one_in_region(new_expanded_term, func_TRUE) < one_in_region(term_2, func_TRUE)):
                j = i
                max_size = max_size_new[1]
                initial_term = max_size_new[0]
                new_expanded_term = term_2


    l.append(new_expanded_term)
    dictionary_storage[tuple(term)] = initial_term, max_size

    return initial_term, max_size, j, l


def list_to_term(term):
    empty_string = ""
    m = len(term)
    for i in range(m):
        if term[i] == 0:
            empty_string += chr(97 + i) + "'"
        elif term[i] == 1:
            empty_string += chr(97 + i)

    if empty_string == '':
        return None
    return empty_string


def comb_function_expansion(func_TRUE, func_DC):
    func_TRUE = func_TRUE[:]
    func_DC = func_DC[:]
    func_all = func_TRUE + func_DC
    for i in range(len(func_all)):
        dictionary_check[tuple(term_to_list(func_all[i]))] = True

    for i in range(len(func_TRUE)):
        func_TRUE[i] = term_to_list(func_TRUE[i])

    for i in range(len(func_DC)):
        func_DC[i] = term_to_list(func_DC[i])
    ans = []
    for term in func_TRUE:
        ans.append((find_max_region(term, func_TRUE, func_DC, 0, [])[0]))

    dictionary_check.clear()
    dictionary_storage.clear()

    return ans


###
def term_to_list_demo(term, n):
    k = len(term)
    l = []
    for i in range(n):
        l.append(None)

    j = 0
    while j < k:
        if term[j] in dictionary_language:
            if j < k - 1 and term[j + 1] == "'":
                l[dictionary_language[term[j]]] = 0
                j += 2
            else:
                l[dictionary_language[term[j]]] = 1
                j += 1
        else:
            j += 1


    return l




'''
def demo(func_TRUE, func_DC, term, n):
    func_TRUE = func_TRUE[:]
    func_DC = func_DC[:]
    func_all = func_TRUE + func_DC
    for i in range(len(func_all)):
        dictionary_check[tuple(term_to_list(func_all[i]))] = True

    term = term_to_list_demo(term, n)
    x = 0
    for element in term:
        if element is None:
            x += 1
    for i in range(len(func_TRUE)):
        func_TRUE[i] = term_to_list(func_TRUE[i])

    for i in range(len(func_DC)):
        func_DC[i] = term_to_list(func_DC[i])

    new_term = find_max_region(term, func_TRUE, func_DC, x, [])
    literal_dropped = new_term[2]
    print(new_term[3])

    expanded_region = []
    full_expanded_term = []
    for i in range(n):
        if i == literal_dropped:
            if term[i] == 1:
                expanded_region.append(0)
            else:
                expanded_region.append(1)
            full_expanded_term.append(None)

        else:
            expanded_region.append(term[i])
            full_expanded_term.append(term[i])

    return list_to_term(expanded_region), list_to_term(full_expanded_term)

'''


func_TRUE = ["a'bc'd'", "abc'd'", "a'b'c'd", "a'bc'd", "a'b'cd"]
func_DC = ["abc'd"]

print(opt_function_reduce(func_TRUE, func_DC))