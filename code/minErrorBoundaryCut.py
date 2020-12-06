import copy
import math
import numpy as np


def minErrorBoundaryCut(e_arr):

	# The input parameter is the array e where eij = ((Pixel in B1) - (Pixel in new Block))^2 for the overlap region between B1 that is Block till now and New Block

	r = len(e_arr)
	c = len(e_arr[0])

	E = [ [0]*c for i in range(r)]


	for i in range(0,r):
		for j in range(0,c):


			if i==0:
				# First row
				E[i][j] = e_arr[i][j]

			else:
				if j==0:
				# First column

					E[i][j] = e_arr[i][j] + min(E[i-1][j],E[i-1][j+1])

				else:

					if j==c-1:
					# Last Column

						E[i][j] = e_arr[i][j] + min(E[i-1][j-1],E[i-1][j])

					else:

						E[i][j] = e_arr[i][j] + min(E[i-1][j-1],E[i-1][j],E[i-1][j+1])

	print(E[0])
	print(E[1])
	print(E[2])
	# Matrix E is formed.
	# To find the minimum cost path, we start with the minimal value of E in the last row and trace back.

	#to find minimum cost in last row of E

	border_index = [0]*r
	min_cost = min( E[-1] )

	for j in range(0,c):
		if E[-1][j]== min_cost:
			border_index[-1] = j;

	

	for i in range(r-2, -1, -1):

		j = border_index[i+1]


		if j==0:
			# first column

			if E[i][j]<E[i][j+1]:
				border_index[i]=j
			else:
				border_index[i]=j+1

		else:
			if j==c-1:

				# last column

				if E[i][j-1]<E[i][j]:
					border_index[i]=j-1
				else:
					border_index[i]=j

			else:
				# others
				nextmin_cost = min(E[i][j-1],E[i][j],E[i][j+1])

				for k in range(j-1,j+2):
					if E[i][k] == nextmin_cost:
						border_index[i] = k

	for i in range(0,r):
		print(border_index[i])
    # Border index is the vector of indices where the border is cut between the existing block and new block

    # This is implemented for a vertical cut. For a horizontal cut, we will take transpose of input array followed by transpose of the output.



# eg 

arr= [ [3,2,3],
       [5,2,0],
       [3,1,6]]

minErrorBoundaryCut(arr)












	