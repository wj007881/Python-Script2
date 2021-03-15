# -*- coding: utf-8 -*-
#author:Ryan
#time  :2021/3/15
arr=[]
for i in range(1,100):
	for j in range(2,i-1):
		if i%j==0:
			print('{}能被{}整除,所以不是质数'.format(i,j))

			break
		else:
			print("{}是质数".format(i))
			if i not in arr:
			 arr.append(i)
print(arr)