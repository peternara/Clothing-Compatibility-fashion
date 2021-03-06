import json
from random import uniform, shuffle, choice
from numpy.random import choice
from time import time

class triplet_creation:
	"""
	Creates triplets, where an anchor point has just one positive and one negative example.
	"""

	def __init__(self, type_of_data, similarity, support):
		"""
		Arguments:
		typle_of_data: train, test, val.
		similarity: true is we're making triplets for training similarity embeddings. if false, we're
			making pairs for training compatibility embeddings.
		support: number of times an anchor point should appear in the dataset.

		Attributes:
		self.asin_to_cat: f(asin) -> category
		self.asin_to_url: f(asin) -> im_url
		self.category_list: f(category) -> list_of_asins_that_belong_to_category
		self.inverse_category_list: f(category) -> list_of_asins_that_do_not_belong_to_category
		self.asin_list -> list_of_all_asins
		"""
		
		self.type_of_data = type_of_data
		if similarity:
			self.objective = 'similarity'
			self.objective_stemmed = 'similar'
		else:
			self.objective = 'compatibility'
			self.objective_stemmed = 'compatible'
		self.support = support

		self.outfile = open('/data/srajpal2/AmazonDataset/Triplets/%s_training/%s_triplets.txt' % (self.objective, self.type_of_data), 'w')

		self.asin_to_cat = {}
		self.asin_to_url = {}
		self.asin_list = []
		# self.category_list = {'t':[], 'b':[], 's':[]}
		# self.inverse_category_list = {'t':[], 'b':[], 's':[]}
		
		self.no_links = 0
		self.count = 0
		
		self.initial_data_pass()
		print "Done with the initial pass."
		self.create_triplets()
		print self.count, self.no_links
		

	
	def initial_data_pass(self):
		"""
		Populates all 3 maps defined in __init__.
		"""
		# inverse_cat = {'t': ['b', 's'], 'b': ['t', 's'], 's': ['b', 't']}

		with open("/data/srajpal2/AmazonDataset/GoldStandard/%s_images.json" % self.type_of_data) as f:
			count = 0
			for line in f:
				info = json.loads(line.rstrip())
				self.asin_to_cat[info["asin"]] = info["category"]
				self.asin_to_url[info["asin"]] = info["imUrl"]
				self.asin_list.append(info["asin"])

		shuffle(self.asin_list)

		return


	def create_triplets(self):
		"""
		Passes through json of all images, and for each line creates triplets.
		"""
		
		for i in xrange(self.support):
			self.count = 0
			self.no_links = 0
			self.randlist = range(0, len(self.asin_list))
			shuffle(self.randlist)
			with open("/data/srajpal2/AmazonDataset/GoldStandard/%s_images.json" % self.type_of_data) as f:
				init_time = time()
				for line in f:
					info = json.loads(line.rstrip())
					asin, img, related, cat = info["asin"], info["imUrl"], info["related"], info["category"]
					
	                		if len(related[self.objective_stemmed])==0:
        	                		self.no_links += 1
                			
                			else:
                        			# Positive Example (from related category of anchor img)
                        			asin2 = choice(related[self.objective_stemmed])
                	       			img2 = self.asin_to_url[asin2]

		                        	# Negative Example (could be from all 3 categories.)
				                asin3 = self.asin_list[self.randlist[self.count]]
                      				img3 = self.asin_to_url[asin3]
			                        
						self.outfile.write("%s %s %s\n" % (img, img2, img3))

					self.count += 1
					if self.count%1000==0:
						print self.count, time()-init_time
		
		return


	def imgUrlTransform(self, url):
		"""
		Takes care of some minor formatting in img urls
		"""
		url = url.split('/')
		url[3] = url[3] + 'set'
		return '/'.join(url)


#print "Training Pairs"
#x1 = pair_creation('training', 10, 10)
#print "\n\nTesting Pairs"
#x2 = pair_creation('testing', 1, 0)
# print "\n\nValidation Pairs"
# x3 = pair_creation('val', 0, 1)
#triplet_creation('training', True, 10)
triplet_creation('val', True, 1)
