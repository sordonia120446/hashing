"""
Implementation of basic hashing.  

Source of tutorial:  http://interactivepython.org/runestone/static/pythonds/SortSearch/Hashing.html

Created on 12/25/2016

@author: sordonia120446
"""



def hash_string(astring, tablesize):
	"""
	Note that anagrams will collide.  
	"""
	sum = 0
	for pos in range(len(astring)):
		sum = sum + ord(astring[pos])
	return sum%tablesize

class HashTable:
	"""
	Creates a hash table, which is a pair of parallel lists. 
	slots --> list of keys
	data  --> list of values
	"""
	def __init__(self):
		self.size = 101 # this should be a sufficiently large prime number
		self.slots = [None] * self.size
		self.data = [None] * self.size

	def put(self,key,data):
		"""
		Basic hash insert.  

		Hash function is a simple remainder method.  

		Collision resolution via linear probing open-addressing.  Prone to clustering.  
		"""
		hashed_key = self.hash_0(key, len(self.slots))

		if self.slots[hashed_key] == None:
			self.slots[hashed_key] = key
			self.data[hashed_key] = data
		else:
			if self.slots[hashed_key] == key:
				self.data[hashed_key] = data  #replace
			else:
				next_slot = self.probe(hashed_key,len(self.slots))
				while self.slots[next_slot] != None and self.slots[next_slot] != key:
					next_slot = self.probe(next_slot,len(self.slots))
					if self.slots[next_slot] == None:
						self.slots[next_slot]=key
						self.data[next_slot]=data
					else:
						self.data[next_slot] = data #replace

	def hash_0(self,key,size):
		"""
		Basic hash function based on remainder method.  
		"""
		return key%size

	def hash_1(self, key, size): 
		"""
		Universal class of hash function
		"""
		a = 11
		b = 13
		return (a*key+b)%size

	def hash_2(self, key, size): 
		"""
		Universal class of hash function
		"""
		a = 17
		b = 19
		return (a*key+b)%size

	def probe(self,oldhash,size):
		"""
		Basic linear probing open-addressing resolution for collisions.  
		Adds the current hashkey by 1, and recalculates the hash using basic remainder method.  
		"""
		return (oldhash+1)%size

	def get(self,key):
		"""
		Basic hash retrieval.  

		Hash function is a simple remainder approach.  

		If initial key retrieval is unsuccessful, probe down the slots until finding the corresponding key.  
		"""
		start_slot = self.hash_0(key,len(self.slots))

		data = None
		stop = False
		found = False
		position = start_slot
		while self.slots[position] != None and not found and not stop:
			if self.slots[position] == key:
				found = True
				data = self.data[position]
			else:
				position=self.probe(position,len(self.slots))
				if position == start_slot:
					stop = True
		return data

	def __getitem__(self,key):
		return self.get(key)

	def __setitem__(self,key,data):
		self.put(key,data)



#---------------------------------------------------------------------------------------------------
# Test stuff


H = HashTable()
m = H.size
print(m)
H[54] = "cat"
H[hash_string('dog', m)] = 'dog'
H.put(10, 'allonsy')
H.put(hash_string('cheeseburger', m), 'cheeseburger')

print(H.slots)
print(H.data)

print(H.__getitem__(10))























