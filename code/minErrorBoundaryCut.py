import numpy as np

def minErrorBoundaryCut(e_arr):
	"""
	:param e_arr: array e where eij = ((Pixel in B1) - (Pixel in new Block))^2
				  for the overlap region between B1 that is Block till now and New Block
	:return: overlap mask
	"""
	r = len(e_arr)
	c = len(e_arr[0])

	E = [[0]*c for i in range(r)]

	for i in range(0,r):
		for j in range(0,c):
			if i==0: # First row
				E[i][j] = e_arr[i][j]
			elif j==0: # First column
				E[i][j] = e_arr[i][j] + min(E[i-1][j],E[i-1][j+1])
			elif j==c-1: # Last Column
				E[i][j] = e_arr[i][j] + min(E[i-1][j-1],E[i-1][j])
			else:
				E[i][j] = e_arr[i][j] + min(E[i-1][j-1],E[i-1][j],E[i-1][j+1])

	# Matrix E is formed.
	# To find the minimum cost path, we start with the minimal value
	# of E in the last row and backtrack

	#to find minimum cost in last row of E
	border_index = [0]*r
	min_cost = min(E[-1])

	for j in range(0,c):
		if E[-1][j]== min_cost:
			border_index[-1] = j

	for i in range(r-2, -1, -1):
		j = border_index[i+1]
		if j==0: # first column
			if E[i][j]<E[i][j+1]:
				border_index[i]=j
			else:
				border_index[i]=j+1

		elif j==c-1: # last column
			if E[i][j-1]<E[i][j]:
				border_index[i]=j-1
			else:
				border_index[i]=j

		else: # others
			nextmin_cost = min(E[i][j-1],E[i][j],E[i][j+1])

			for k in range(j-1,j+2):
				if E[i][k] == nextmin_cost:
					border_index[i] = k

	overlap_mask = np.ones(np.array(e_arr).shape)
	for i in range(0,r):
		overlap_mask[i,0:border_index[i]] = np.zeros(border_index[i])
	return overlap_mask

    # Border index is the vector of indices where the border is cut
	# between the existing block and new block
    # This is implemented for a vertical cut. For a horizontal cut, we will take
	# transpose of input array followed by transpose of the output.

def minCostMask(New, Bl, Bt, overlap_type,overlap_size):
	"""
		New block to be placed. Bl is block to the left and Bt is block on top.
		According to the overlap_type, the mask would be returned
	"""
	patch_mask = np.ones(New.shape)

	if overlap_type=='v':
		e_dif = Bl[:,-overlap_size:] - New[:,0:overlap_size]
		e_arr = np.power(e_dif,2).tolist()
		patch_mask[:,0:overlap_size] = minErrorBoundaryCut(e_arr)

	elif overlap_type=='h':
		e_dif = Bt[-overlap_size:,:] - New[:overlap_size,:]
		# horizontal
		e_arr = np.power(e_dif,2)
		e_arr = e_arr.transpose()
		# vertical
		e_arr = e_arr.tolist()

		patch_mask[0:overlap_size,:] = minErrorBoundaryCut(e_arr).transpose()
		# horizontal

	elif overlap_type=='b':
		# vertical overlap
		e_difv = Bl[:,-overlap_size:] - New[:,:overlap_size]
		e_arrv = np.power(e_difv,2).tolist()

		patch_mask[:,0:overlap_size] = minErrorBoundaryCut(e_arrv)

		# horizontal overlap
		e_difh = Bt[-overlap_size:,:] - New[:overlap_size,:]
		e_arrh = np.power(e_difh,2)
		e_arrh = e_arrh.transpose()
		e_arrh = e_arrh.tolist()

		patch_mask[0:overlap_size,:] = patch_mask[0:overlap_size,:]*(minErrorBoundaryCut(e_arrh).transpose())

	else:
		print('Error')

	return patch_mask