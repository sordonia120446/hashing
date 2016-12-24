#Hashing Exercises

##basic_hashing.py

This is a basic hashtable that uses open addressing to handle collisions.  It was a nice way to play around with building my own hashtable. 

##hopscotch_hashing.py

A "better" version of cuckoo hashing that can handle concurrent events.  To handle collisions, it moves buckets around in a fashion similar to linear probing, and in the spirit of cuckoo hashing.
References to authors and wiki summary included at the top.  Code is based off of a Java implementation that can be found on authors' website.  
Basic test cases provided at the bottom.  
Will add concurrency, eventually.   
