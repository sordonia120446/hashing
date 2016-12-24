"""
Implementation of hopscotch hashing with global locking concurrency control, 
based on work done by the following talented invidividuals:
	Hila Goel, Tel Aviv University
	hila.goel@gmail.com

	Maya Gershovitz, Tel Aviv University
	mgershovitz@gmail.com

Wiki Summary:  https://en.wikipedia.org/wiki/Hopscotch_hashing

Website:  http://cs.tau.ac.il/~multi/2015a/chhm.htm

Created on 12/25/2016

@author:  sordonia120446
"""


class hopscotch():
	# Contants
	HOP_RANGE = 32
	ADD_RANGE = 256
	MAX_SEGMENTS = 1048576 # includes neighborhood for last hash location 

	class bucket():
		"""
		Bucket is the table object.
		Each bucket contains a key and data pairing (as in a usual hashmap),
		and an "hop_info" variable, containing the information 
		regarding all the keys that were initially mapped to the same bucket. 
		"""
		def __init__(self):
			self._hop_info = 0
			self._key = -1
			self._data = -1

		# def get_hop_info(self):
		# 	return self._hop_info

		# def get_key(self):
		# 	return self._key

		# def get_data(self):
		# 	return self._data

	def __init__(self):
		size = self.MAX_SEGMENTS + self.ADD_RANGE
		self.segments_arrays = [] # array of buckets
		for ind in range(0, size):
			self.segments_arrays.append( self.bucket() )
		# concurrency stuff
		# BUSY = -1
		# _lock = 

	def trial(self):
		"""
		Debug method to verify the appropriate number of keys stored.  
		"""
		key_count = 0
		for ind in range(0, self.MAX_SEGMENTS + self.ADD_RANGE):
			tmp = self.segments_arrays[ind]
			if (tmp._key != -1):
				key_count += 1
		print("The number of keys are {}".format(key_count))

# TODO:  may be beneficial to refactor remove code to reduce repeat logic
	def remove(self, key):
		"""
		Checks to see if the key exists.  
		If so, reset the bucket's contents to default, including _hop_info.  
		"""
		hash_index = key & (self.MAX_SEGMENTS - 1)
		start_bucket = self.segments_arrays[hash_index]
		hop_info = start_bucket._hop_info
		mask = 1
		print(start_bucket._key)
		for ind in range(0, self.HOP_RANGE):
			if ( (mask & hop_info) >= 1 ):
				"""
				Will occur if reached the first bit of the bucket with a key.  
				"""
				check_bucket = self.segments_arrays[hash_index + ind]
				if (key == check_bucket._key):
					"""
					Clear the bucket data.  Flip bits for _hop_info.  
					"""
					rc = check_bucket._data
					check_bucket._key = -1
					check_bucket._data = -1
					start_bucket._hop_info &= ~(1<<ind)
					return rc
			mask <<= 1
		return -1

	def contains(self, key):
		hash_index = key & (self.MAX_SEGMENTS - 1)
		start_bucket = self.segments_arrays[hash_index]
		hop_info = start_bucket._hop_info
		mask = 1
		for ind in range(0, self.HOP_RANGE):
			if ( (mask & hop_info) >= 1 ):
				check_bucket = self.segments_arrays[hash_index + ind]
				if (key == check_bucket._key):
					return True
			mask <<= 1
		return False

	def get_value(self, key):
		hash_index = key & (self.MAX_SEGMENTS - 1)
		start_bucket = self.segments_arrays[hash_index]
		hop_info = start_bucket._hop_info
		mask = 1
		for ind in range(0, self.HOP_RANGE):
			if ( (mask & hop_info) >= 1 ):
				check_bucket = self.segments_arrays[hash_index + ind]
				if (key == check_bucket._key):
					return check_bucket._data
			mask <<= 1
		return -1

	def find_closer_bucket(self, free_bucket_index, free_distance, val):
		"""
		The hopscotch magic happens here.  
		This function returns a list of three values:  [free_distance, val, new_free_bucket_index] 

		FYI:  
		free_bucket_index --> index of first empty bucket in table
		free_distance     --> gap between start_bucket & newly freed bucket
		"""
		result = [0,0,0]
		allotted_distance = self.HOP_RANGE - 1 # this will determine how far we can move the bucket
		move_bucket_index = free_bucket_index - allotted_distance
		move_bucket = segments_arrays[move_bucket_index]

		while (allotted_distance > 0):
			start_hop_info = move_bucket._hop_info
			move_free_distance = -1
			mask = 1
			for ind in range(0, allotted_distance):
				if ( (mask & start_hop_info) >= 1 ):
					move_free_distance = ind
					break # TODO find a better way to implement w/o break
			# When a suitable bucket is found, it's content is moved to the old free bucket
			if (-1 != move_free_distance):
				if (start_hop_info == move_bucket._hop_info):
					print('transferring bucket')
					new_free_bucket_index = move_bucket_index + move_free_distance
					new_free_bucket = segments_arrays[new_free_bucket_index]
					# updates move_bucket's hop_info to indicate newly inserted bucket
					move_bucket._hop_info = move_bucket._hop_info | (1 << allotted_distance)
					segments_arrays[free_bucket_index]._data = new_free_bucket._data
					segments_arrays[free_bucket_index]._key = new_free_bucket._key
					# not sure if below is needed
					# new_free_bucket._key = -1
					# new_free_bucket._data = -1
					move_bucket._hop_info = move_bucket._hop_info & ( ~(1 << move_free_distance) )
					# commented out confusingly ordered output; swapped outputs around to match input order
					# result[0] = (free_distance)
					# result[1] = (val)
					# result[2] = (new_free_bucket_index)
					result[0] = new_free_bucket_index
					result[1] = free_distance
					result[2] = val
					return result
			move_bucket_index += 1
			move_bucket = segments_arrays[move_bucket_index]
			allotted_distance -= 1 # count down to a smaller distance from free_bucket
		# if no free bucket found
		segments_arrays[free_bucket_index]._key = -1
		return result

	def insert(self, key, data):
		"""
		In tandem with helper function find_closer_bucket, this is where the 
		hopscotch magic happens.  
		First, check if the key already exists in the table.  
		"""
		val = 1
		hash_index = key & (self.MAX_SEGMENTS - 1)
		start_bucket = self.segments_arrays[hash_index]
		# lock table if doing parallel operation
		if self.contains(key):
			return False
		# look for free space to add the new bucket within the neighborhood of start_bucket
		free_bucket_index = hash_index
		free_bucket = self.segments_arrays[free_bucket_index]
		free_distance = 0
		while (free_distance < self.ADD_RANGE):
			if (-1 == free_bucket._key):
				free_bucket._key = -1
				break
			free_bucket_index += 1
			free_bucket = self.segments_arrays[free_bucket_index]
			free_distance += 1
		# TODO:  integrate below if-statement into while loop, and replace break with this
		if (free_distance < self.ADD_RANGE):
			while (val != 0):
				if (free_distance < self.HOP_RANGE):
					# Inserts the new bucket to the free space
					start_bucket._hop_info = start_bucket._hop_info | (1 << free_distance)
					free_bucket._data = data
					free_bucket._key = key
					return True
				else:
					# Free space not found in neighborhood of start_bucket.  
					# Clear space, hopscotch style.  
					closest_bucket_info = self.find_closer_bucket(free_bucket_index, free_distance, val)
					free_bucket_index = closest_bucket_info[0]
					free_distance = closest_bucket_info[1]
					val = closest_bucket_info[2]
					free_bucket = self.segments_arrays[free_bucket_index]
		print('Resized table')
		return False


















# Tests
H = hopscotch()
H.trial()
H.remove(2)
H.insert(1, "Nicki Minaj")
H.insert(2, "justiiiiin")
H.contains(1)
print(H.get_value(1))















