input: 2D array
output: 2D array

for(all people):
    i_avg = sum of i's scores/# of i's scores = X bar
    j_avg = sum of j's scores/# of j's scored = Y bar

    prod = []
    prod_sq = []

    for(every class):
        if(both ranked class):
            i_rating = input[class index][i]
            j_rating = input[class index][j]
            prod.append([(i_rating-i_avg)(j_rating-j_avg)])
            prod_sq.append([(i_rating-i_avg)^**(j_rating-j_avg)^**])

    sum = 0
    sum_sq = 0

    for p in prod:
        sum = p + sum
    for p_sq in prod_sq:
        sum_sq = p_sq + sum_sq

    coeff = [][]
    coeff[i][j] = sum/sum_sq.sqrt()
    coeff[j][i] = sum/sum_sq.sqrt()
return coeff
