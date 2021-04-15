import math

"""
input: vector of relevance scores (ints) 0-3
output: Normalized Discounted Cumulative Gain at each pos as an array
        Final Normalized Discounted Cumulative Gain
"""
def calculate_NDCG(relevance_scores):
    nb_scores = len(relevance_scores)
    DCG_arr = [None] * nb_scores
    NDCG_arr = [None] * nb_scores
    opti_NDCG_arr = [None] * nb_scores
    nb_3s = 0
    nb_2s = 0
    nb_1s = 0
    DCC = 0
    for i in range(nb_scores):
        rel_i = relevance_scores[i]
        if rel_i == 3:
            nb_3s += 1
        elif rel_i == 2:
            nb_2s += 1
        elif rel_i == 1:
            nb_1s += 1

        if rel_i != 0:
            DCC += rel_i / math.log(i + 2, 2)
        DCG_arr[i] = DCC
    opti_DCC = 0
    j = 0
    for k in range(nb_3s):
        opti_DCC += 3 / math.log(j + 2, 2)
        opti_NDCG_arr[j] = opti_DCC
        j += 1
    for l in range(nb_2s):
        opti_DCC += 2 / math.log(j + 2, 2)
        opti_NDCG_arr[j] = opti_DCC
        j += 1
    for m in range(nb_1s):
        opti_DCC += 1 / math.log(j + 2, 2)
        opti_NDCG_arr[j] = opti_DCC
        j += 1
    for n in range(j, nb_scores):
        opti_NDCG_arr[n] = opti_DCC
    for i in range(nb_scores):
        NDCG_arr[i] = DCG_arr[i] / opti_NDCG_arr[i]
    final_NDCG = NDCG_arr[i]
    return NDCG_arr, final_NDCG


"""
input: vector of relevance scores (ints) 0-3
output: precision at each pos as an array
        Final precision
"""
def calculate_precision(relevance_scores):
    count = 0
    nb_scores = len(relevance_scores)
    precision_arr = [None] * nb_scores
    for i in range(nb_scores):
        if relevance_scores[i] > 0:
            count += 1
        precision_arr[i] = count / (i + 1)
    final_precision = count / nb_scores
    return precision_arr, final_precision


"""
test_scores = [3, 1, 2, 0]
[test_NDCG_arr, test_final_NDCG] = calculate_NDCG(test_scores)
print(test_NDCG_arr)
print(test_final_NDCG)
[test_precision_arr, test_final_precision] = calculate_precision(test_scores)
print(test_precision_arr)
print(test_final_precision)
"""
