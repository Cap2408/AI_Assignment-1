import sys

class Block:
	""" abstraction of block, top = '0': means it is clear, bottom = '1':means OnT(Block), pick up means top = '-1' """

	def __init__(self,top,idn,bottom):
		self.top = top
		self.id = idn
		self.bottom = bottom

	def print(self):
		""" print function """
		print("block :",self.id,"top :",self.top,"bottom :",self.bottom,"\n")

	def identity(self):
		""" return string : identity of self """
		return self.id	

	def modify_name(self,new_id):
		""" setting name to actual one """
		self.id = new_id

	def edit_bottom(self,new_bottom):
		"""modifying bottom of selfblock"""
		self.bottom = new_bottom

	def edit_top(self,new_top):
		"""modifying bottom of selfblock"""
		self.top = new_top	

block_dict = {}
block_dict1 = {}
block_temp = {}
goals = []
arm = '0'

def initialize(initial_state,goal_state):
	""" Creation of initial state and goal state from files """
	global block_dict
	global block_dict1
	global goals
	global block_temp
	print("Enter the number of blocks in the Block World Problem:")
	a = int(input())
	
	""" creating blocks for prediactes. initialization and placing on the table. """
	block_list= []
	for i in range(a):
		block_list.append(Block('0',str(i),'1'))
	
	block_list1= []
	for i in range(a):
		block_list1.append(Block('0',str(i),'1'))	 	
	
	#for i in range(len(block_list)):
	#	block_list[i].print()
	
	
	j = 0
	
	f = open(initial_state)
	for line in f:
		line = line.strip("\n")
		pred = line.split(" ")
		try:
			block_dict[pred[1]]
	
		except:
			if(j<a):
				block_list[j].modify_name(pred[1])
				block_temp = {pred[1]:block_list[j]}
				block_dict.update(block_temp)
				j += 1

		if(len(pred)==3):
			try:
				block_dict[pred[2]]
		
			except:
				if(j<a):
					block_list[j].modify_name(pred[2])
					block_temp = {pred[2]:block_list[j]}
					block_dict.update(block_temp)
					j += 1
	
		if(pred[0]=='ONT'):
			pass
	
		if(pred[0]=='ON'):
			block1 = block_dict[pred[1]]
			block2 = block_dict[pred[2]]
			block1.edit_bottom(pred[2])
			block2.edit_top(pred[1])
	
	#for i in range(len(block_list)):
	#	block_list[i].print()
	
	
	j = 0
	
	f = open(goal_state)
	for line in f:
		line = line.strip("\n")
		pred = line.split(" ")
	#	print("Line 59",j)
		try:
			block_dict1[pred[1]]
	
		except:
			if(j<a):
				block_list1[j].modify_name(pred[1])
				block_temp = {pred[1]:block_list1[j]}
				block_dict1.update(block_temp)
				j += 1
	
	#	print("Line 69",j)
		if(len(pred)==3):
			try:
				block_dict1[pred[2]]
		
			except:
				if(j<a):
					block_list1[j].modify_name(pred[2])
					block_temp = {pred[2]:block_list1[j]}
					block_dict1.update(block_temp)
					j += 1
	#	print("Line 79",j)
	
		if(pred[0]=='ONT'):
			pass
	
		if(pred[0]=='ON'):
			block1 = block_dict1[pred[1]]
			block2 = block_dict1[pred[2]]
			block1.edit_bottom(pred[2])
			block2.edit_top(pred[1])
	
	#for i in range(len(block_list1)):
	#	print(block_list1[i].identity())
	
	for i in range(a):
		block1 = block_list[i]
		index = block1.identity()
		block2 = block_dict1[index]
	
		if(block2.bottom!=block1.bottom):
			if(block2.bottom!='1'):
				goals.append('ON('+block2.identity()+','+block2.bottom+')')
			else:
				goals.append('ONT('+block2.identity()+')')
	
	#for i in range(len(goals)):
	#	print(goals[i],'\n')


def do_stack(a,b):
	""" Check preconditions and execute """
	global block_dict
	global arm
	if(b.top!='0'):
		do_unstack(block_dict[b.top],b)
	#also put down the block in hand and pick up 
	if(arm!=a.identity()):
		if(arm=='0'):
			if(a.bottom=='1'):
				do_pick_up(a)
			else:
				do_unstack(a,block_dict[a.bottom])
		else:
			do_put_down(block_dict[arm])
			if(a.bottom=='1'):
				do_pick_up(a)
			else:
				do_unstack(a,block_dict[a.bottom])
	print('Stack('+a.identity()+','+b.identity()+')')
	a.bottom = b.identity()
	b.top = a.identity()
	a.top = '0'
	arm = '0'

def do_unstack(a,b):
	""" Check preconditions and execute """
	global arm
	global block_dict
	if(arm!='0'):
		do_put_down(block_dict[arm])
	if(a.top!='0'):
		do_unstack(block_dict[a.top],a)
	if(a.top=='0'):
		if(arm!='0'):
			do_put_down(block_dict[arm])
	print('UnStack('+a.identity()+','+b.identity()+')')
	arm = a.identity()
	a.bottom = '0'
	a.top = '-1'
	b.top = '0'

def do_pick_up(a):
	""" Check preconditions and execute """
	global arm
	global block_dict
	if(arm!='0'):
		do_put_down(block_dict[arm])
	if(a.top!='0'):
		do_unstack(block_dict[a.top],a)
		do_put_down(block_dict[arm])

	print('PU('+a.identity()+')')
	arm = a.identity()
	a.top = '-1'
	a.bottom = '0'

def do_put_down(a):
	""" Check preconditions and execute """
	global arm
	global block_dict
	a.top = '0'
	a.bottom = '1'
	arm = '0'
	print('PD('+a.identity()+')')

def planner(goals,block_dict):
	""" The Planner Function """
	#global goals
	#global block_dict
	for i in range(len(goals)):
		print(goals[i])

	for i in range(len(goals)):
		if(goals[i][:3]=='ONT'):
			block = block_dict[goals[i][4]]
			if(block.bottom=='1'):
				pass
			else:
				do_unstack(block,block_dict[block.bottom])
				do_put_down(block)
		else:
			block1 = block_dict[goals[i][3]]
			block2 = block_dict[goals[i][5]]
			do_stack(block1,block2)
	
if __name__ == "__main__":
	initial_state = sys.argv[1]
	final_state = sys.argv[2]
	initialize(initial_state,final_state)
	planner(goals,block_dict)