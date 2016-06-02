import csv
import re
import sys
import math, operator

item_U = dict()
r = dict()
rate_sum = dict()
avg = dict()
def do_average():
	global rate_sum
	global item_U
	global avg
	for user in item_U:
		size = len(item_U[user])
		avg[user] = rate_sum[user]/size


def pearson_correlation(u, v):
	global rate_sum
	global item_U
	global r

	set_a = set(item_U[u])
	set_b = set(item_U[v])
	co_rated = set_a.intersection(set_b)
	co_rated =  list(co_rated)
	#print co_rated

	top = 0
	for i in co_rated:
		top += (r[(u,i)] - avg[u]) * (r[(v,i)] - avg[v])

	bottom1 = 0
	bottom2 = 0
	for i in co_rated:
		bottom1 += math.pow(r[(u,i)] - avg[u], 2)
		bottom2 += math.pow(r[(v,i)] - avg[v], 2)

	bottom1 = math.sqrt(bottom1)

	bottom2 = math.sqrt(bottom2)
    if bottom1 * bottom2 == 0:
        return 0
	pearson = float(top) / (bottom1 * bottom2)


	return pearson

def K_nearest_neighbors(d, k):
	res = dict()
	end = 0
	for w in sorted(d, key = d.get, reverse = True):
		res[w] = d[w]
		end += 1
		if end == k:
			break

	return res

def predict(user_id, item, w):
	global item_U
	global r
	top = 0
	bottom = 0
	for i in w:
		if (i, item) in r:
			top += (w[i] * r[(i,item)])
			bottom += w[i]

	if bottom == 0 or top == 0:
		return 0
	else:
		return top/bottom

def main(inputFile, user_id, t_item, k):
	global rate_sum
	global item_U
	global r
	for line in inputFile:
		#array = re.split(r'\t+', line)
		array = line.split("\t")
		user = array[0]
		rate = float(array[1])
		item = array[2]
		if item.endswith('\n'):
			item = item[:-1]
		
		if user not in item_U:
			item_U[user] = [item]
		else:
			item_U[user].append(item)

		if user not in rate_sum:
			rate_sum[user] = rate
		else:
			rate_sum[user] += rate

		r[(user,item)] = rate
		

	do_average()
	#step1: do the pearson between active user, other user
	pearson = dict()
	for other_user in rate_sum:
		if other_user != user_id:
			pearson[other_user] = pearson_correlation(user_id, other_user)

	
	#step 2: find out the k nearest neighor
	w = K_nearest_neighbors(pearson, k)
	for i in sorted(w, key = w.get, reverse = True):
		print i, w[i]
	
	#step 3: make prediction
	pred = predict(user_id, t_item, w)
	print "\n"
	print pred


if __name__ == '__main__':
	inputFile = open(sys.argv[1])#file name
	user_id = sys.argv[2]#user_id
	t_item = sys.argv[3]
	k = int(sys.argv[4])
	main(inputFile, user_id, t_item, k)