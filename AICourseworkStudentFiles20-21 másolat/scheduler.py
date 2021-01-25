import comedian
import demographic
import ReaderWriter
import timetable
import random
import math

class Scheduler:

	def __init__(self,comedian_List, demographic_List):
		self.comedian_List = comedian_List
		self.demographic_List = demographic_List

	#Using the comedian_List and demographic_List, create a timetable of 5 slots for each of the 5 work days of the week.
	#The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
	#	timetableObj.addSession("Monday", 1, comedian_Obj, demographic_Obj, "main")
	#This line will set the session slot '1' on Monday to a main show with comedian_obj, which is being marketed to demographic_obj. 
	#Note here that the comedian and demographic are represented by objects, not strings. 
	#The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
	#The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in tasks 2 and 3. 
	#Comedian (3rd argument) and Demographic (4th argument) can be assigned any value, but if the comedian or demographic are not in the original lists, 
	#	your solution will be marked incorrectly. 
	#The final, 5th argument, is the show type. For task 1, all shows should be "main". For task 2 and 3, you should assign either "main" or "test" as the show type.
	#In tasks 2 and 3, all shows will either be a 'main' show or a 'test' show
	
	#demographic_List is a list of Demographic objects. A Demographic object, 'd' has the following attributes:
	# d.reference  - the reference code of the demographic
	# d.topics - a list of strings, describing the topics that the demographic like to see in their comedy shows e.g. ["Politics", "Family"]

	#comedian_List is a list of Comedian objects. A Comedian object, 'c', has the following attributes:
	# c.name - the name of the Comedian
	# c.themes - a list of strings, describing the themes that the comedian uses in their comedy shows e.g. ["Politics", "Family"]

	#For Task 1:
	#Keep in mind that a comedian can only have their show marketed to a demographic 
		#if the comedian's themes contain every topic the demographic likes to see in their comedy shows.
	#Furthermore, a comedian can only perform one main show a day, and a maximum of two main shows over the course of the week.
	#There will always be 25 demographics, one for each slot in the week, but the number of comedians will vary.
	#In some problems, demographics will have 2 topics and in others, 3.
	#A comedian will have between 3-8 different themes. 

	#For Task 2 and 3:
	#A comedian can only have their test show marketed to a demographic if the comedian's themes contain at least one topic
		#that the demographic likes to see in their comedy shows.
	#Comedians can only manage a 4 hours of stage time, where main shows 2 hours and test shows are 1 hour.
	#A Comedian can not be on stage for more than 2 hours a day.

	#You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need. 
	#Furthermore, you should not import anything else beyond what has been imported above. 
	#To reiterate, the five calls are timetableObj.addSession, d.name, d.genres, c.name, c.talents

	#This method should return a timetable object with a schedule that is legal according to all constraints of task 1.

	#So basically, how this method schedule a right timetaible is, first we create two dictionaries, one for comedians and
	#one for demographs and we fill these up such as the key is the comedians and the demorgpahics, respectively, and the values
	#are lists of demographs where the comedian can be marketed and lists of comedian whose have the right themes for the demorgaph,
	#respectively. After, using a hueristic, based on these two dictionaries, we create 25 possbile session schedule, without the slot and days.
	#If in this schedule, a comedian (a) performs more than twice, we assign some demographs to other comedians with less than 2 
	#demographs, so (a) will have maximum 2 demographs. Hence we get a schedule where every comedian performs maximum twice.
	#Now we just have to add the days and slots to the schedule. We do this in the order: we start with comedians with 2 demographs,
	# schedule those two to seperate days, after this we just fill up the remaing slots with comedians that perform only once.
	#Therefore, this way we get the right schedule

	def createSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(1)
		
		#Here is where you schedule your timetable

		show_type = "main"
		comedian_dict = dict() #stores the possible demographics for each comedain
		demographic_dict = dict() #stores the possible comedians for each demographs
		list_ses = list()
		come_time = dict()

		for comedians in self.comedian_List:
			good_demog = list()
			for demogs in self.demographic_List:
				if(set(demogs.topics).issubset(set(comedians.themes))):
					good_demog.append(demogs)
			comedian_dict[comedians] = good_demog
		
		for demogs in self.demographic_List:
			good_comedians = list()
			for comedians in self.comedian_List:
				if(set(demogs.topics).issubset(set(comedians.themes))):
					good_comedians.append(comedians)
			demographic_dict[demogs] = good_comedians
		
		

		for demos in self.demographic_List:
			size = list()
			pos_comes = demographic_dict[demos]
			for comes in pos_comes:
				size.append(len(comedian_dict[comes]))
			index = size.index(min(size))
			list_ses.append(["Error", 0, pos_comes[index], demos, "main"])
		
		for i in range(0,25):
			come = list_ses[i][2]
			if come in come_time:
				come_time[come] += 1
			else:
				come_time[come] = 1
		
		for i in self.comedian_List:
			if i not in come_time:
				come_time[i] = 0
		
		
		for i in come_time:
			if come_time[i] > 2:
				for j in range(0,25):
					come = list_ses[j][2]
					if come == i:
						demo = list_ses[j][3]
						for l in demographic_dict[demo]:
							if come_time[l] < 2 and come_time[i] > 0:
								list_ses[j][2] = l
								come_time[i] -= 1
								come_time[l] += 1
								break
		
		
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		slot_counter = 1
		day_counter = 0
		counter = 0
		
		for i in come_time:
			if come_time[i] > 1:
				for j in list_ses:
					if j[2] == i:
						j[0] = days[day_counter]
						day_counter += 1
						j[1] = slot_counter
						counter += 1
						if day_counter > 4:
							day_counter = 0
							slot_counter += 1

		
		for i in come_time:
			if come_time[i] == 1:
				for j in list_ses:
					if j[2] == i:
						j[0] = days[day_counter]
						day_counter += 1
						j[1] = slot_counter
						counter += 1
						if day_counter > 4:
							day_counter = 0
							slot_counter += 1


		for i in list_ses:
			a = i[0]
			b = i[1]
			c = i[2]
			d = i[3]
			e = i[4]
			timetableObj.addSession(a, b, c, d, e)
			
		
						
		


		#This line generates a random timetable, that may not be valid. You can use this or delete it.
		#self.randomMainSchedule(timetableObj)
		#Do not change this line
		return timetableObj

	#Now, we have introduced test shows. Each day now has ten sessions, and we want to market one main show and one test show 
		#to each demographic. 
	#All slots must be either a main or a test show, and each show requires a comedian and a demographic. 
	#A comedian can have their test show marketed to a demographic if the comedian's themes include at least one topic the demographic likes.
	#We are now concerned with stage hours. A comedian can be on stage for a maximum of four hours a week.
	#Main shows are 2 hours, test shows are 1 hour.
	#A comedian can not be on stage for more than 2 hours a day.

	#This method creates a schedule similarly to the previous one, with the difference that in the comedian_dict and demographic_dict
	# we save the possibilities not just for the main but for the test shows too. Furthermore, we assign demographics with comedians
	#based on two criteria. The main one is, how many hours are assigned for each possible comedian, and we choose the one with the lowest,
	#and if there are more with the lowest, we choose the one from them which has the lowest value in the come_time dictionary, which
	#keeps track on each comedian how many main or test could possibly perform. Assigning like this result in a schedule where comedians
	# have evenly many shows, resulting no comedian has to perform more than 4 hours. Lastly, we assign the days and slots for the 
	#sessions the same way like in the previous method.

	def createTestShowSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(2)

		comedian_dict = dict() #stores the possible main at 0 and test at 1 demographics for each comedain
		demographic_dict = dict() #stores the possible main and test comedians for each demographs
		list_ses = list()
		come_time = dict()
		come_assigned = dict()

		for comedians in self.comedian_List:
			good_demog = list()
			for demogs in self.demographic_List:
				if(set(demogs.topics).issubset(set(comedians.themes))):
					good_demog.append(demogs)
			comedian_dict[comedians] = good_demog
		
		for demogs in self.demographic_List:
			good_comedians = list()
			for comedians in self.comedian_List:
				if(set(demogs.topics).issubset(set(comedians.themes))):
					good_comedians.append(comedians)
			demographic_dict[demogs] = good_comedians

		for comedians in self.comedian_List:
			good_demog = list()
			for demogs in self.demographic_List:
				if not (set(demogs.topics).isdisjoint(set(comedians.themes))):
					good_demog.append(demogs)
			temp = list()
			temp.append(comedian_dict[comedians])
			temp.append(good_demog)
			comedian_dict[comedians] = temp
		
		for demogs in self.demographic_List:
			good_comedians = list()
			for comedians in self.comedian_List:
				if not (set(demogs.topics).isdisjoint(set(comedians.themes))):
					good_comedians.append(comedians)
			temp = list()
			temp.append(demographic_dict[demogs])
			temp.append(good_comedians)
			demographic_dict[demogs] = temp
				
		for come in comedian_dict:
			come_time[come] = 0
			come_assigned[come] = 0
			temp = comedian_dict[come]
			for i in range(0,2):
				if i == 0:
					temp2 = temp[0]
					for mains in temp2:
						come_time[come] += 2
				if i == 1:
					temp2 = temp[1]
					for test in temp2:
						come_time[come] += 1
		
		
		for demos in demographic_dict:
			temp = demographic_dict[demos][0]
			if len(temp) == 1:
				list_ses.append(["", 0, temp[0], demos, "main"])
				come_assigned[temp[0]] += 2

		

		for demos in demographic_dict:
			pos_comes = demographic_dict[demos]
			pos_comes_main = pos_comes[0]
			for i in range(0,2):
				if i == 0 and len(pos_comes_main) != 1:
					temp = pos_comes[0]
					size = list()
					lowest_list = list()
					size2 = list()
					for comes in temp:
						size.append(come_assigned[comes])
					lowest = min(size)
					for j in range(0,len(size)):
						number = size[j]
						if number == lowest:
							lowest_list.append(temp[j])
					for comes2 in lowest_list:
						size2.append(come_time[comes2])
					pas = True
					index = size2.index(min(size2))
					while pas:
						index = size2.index(min(size2))
						if come_assigned[lowest_list[index]] > 2:
							if len(lowest_list) != 1:
								size2.pop(index)
								lowest_list.pop(index)
							else:
								pas = False
						else:
							pas = False	
					list_ses.append(["", 0, lowest_list[index], demos, "main"])
					come_assigned[lowest_list[index]] += 2
				if i == 1:
					temp = pos_comes[1]
					size = list()
					lowest_list = list()
					size2 = list()
					for comes in temp:
						size.append(come_assigned[comes])
					lowest = min(size)
					for j in range(0,len(size)):
						number = size[j]
						if number == lowest:
							lowest_list.append(temp[j])
					for comes2 in lowest_list:
						size2.append(come_time[comes2])
					index = size2.index(min(size2))
					list_ses.append(["", 0, lowest_list[index], demos, "test"])
					come_assigned[lowest_list[index]] += 1

		
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		slot_counter = 1
		day_counter = 0
		counter = 0
		
		for i in come_time:
			if come_time[i] > 2:
				for j in list_ses:
					if j[2] == i:
						j[0] = days[day_counter]
						day_counter += 1
						j[1] = slot_counter
						counter += 1
						if day_counter > 4:
							day_counter = 0
							slot_counter += 1

		for i in list_ses:
			a = i[0]
			b = i[1]
			c = i[2]
			d = i[3]
			e = i[4]
			timetableObj.addSession(a, b, c, d, e)
		
		


		#Here is where you schedule your timetable

		#This line generates a random timetable, that may not be valid. You can use this or delete it.
		#self.randomMainAndTestSchedule(timetableObj)

		#Do not change this line
		return timetableObj

	#It costs £500 to hire a comedian for a single main show.
	#If we hire a comedian for a second show, it only costs £300. (meaning 2 shows cost £800 compared to £1000)
	#If those two shows are run on consecutive days, the second show only costs £100. (meaning 2 shows cost £600 compared to £1000)

	#It costs £250 to hire a comedian for a test show, and then £50 less for each extra test show (£200, £150 and £100)
	#If a test shows occur on the same day as anything else a comedian is in, then its cost is halved. 

	#Using this method, return a timetable object that produces a schedule that is close, or equal, to the optimal solution.
	#You are not expected to always find the optimal solution, but you should be as close as possible. 
	#You should consider the lecture material, particular the discussions on heuristics, and how you might develop a heuristic to help you here.
	# 
	# 
	# My approach is the following, the method first assigns comedians and demographics to main shows, it tires to maximaize the number
	#of comedians who performs only 2 main shows. The optimal schedule regarding the main shows is, when we have 12 comdeians who
	#perform 2 main shows and 1 comedain who performs the remaining one main show. For the test shows, we schedule it similarly.
	#The method tries to maximize the number of comedians, from the remaining free ones, who perform 4 test shows. The optimal schedule
	#for the test shows is, when there are 6 comdiands who perform 4 test shows one who perform the one remaining test show.
	#The method tries to get as close as possible to this optimal schedule. After it assigned the comedians to the demographics,
	#it schedules them the following way: First it schedules the main shows. For those comedians who perform 2 main shows, it
	#schedules the two shows to folloing days, hence saving £400 on the second main show. For the comedians who perform only one
	#main show, it schedules them to days where there are odd number of open slots left, so it maximizes the number of days with even
	#number of open slots left. It will be useful when we schedule the test shows. After we scheduled the main shows, we will have
	#one odd and 4 even slots day left. For the odd day we schedule the comedian who performs only one test show. Hence we left with
	# 5 even slots day and comedians who perform even many test shows. The most optimal way to schedule test shows is the following:
	#For each comedian, schedule two of their test shows to one day, and if there are 2 more remaing test shows, schedule them to
	#another, but same day.
	#This is the most optimal way of assigning comedians with demographics and scheduling the shows.
	#  
	def createMinCostSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(3)

		#Here is where you schedule your timetable

		comedian_dict = dict() #stores the possible main at 0 and test at 1 demographics for each comedain
		demographic_dict = dict() #stores the possible main and test comedians for each demographs
		demo_dict_dec = dict()
		list_ses = list()
		come_time = dict()
		come_assigned = dict()
		demo_dec = list()
		come_time_rem = dict()
		come_test_dict = dict()

		for demos in self.demographic_List:
			demo_dec.append(demos)

		for comedians in self.comedian_List:
			good_demog = list()
			for demogs in self.demographic_List:
				if(set(demogs.topics).issubset(set(comedians.themes))):
					good_demog.append(demogs)
			comedian_dict[comedians] = good_demog
		
		for demogs in self.demographic_List:
			good_comedians = list()
			for comedians in self.comedian_List:
				if(set(demogs.topics).issubset(set(comedians.themes))):
					good_comedians.append(comedians)
			demographic_dict[demogs] = good_comedians
			demo_dict_dec[demogs] = good_comedians

		for comedians in self.comedian_List:
			good_demog = list()
			for demogs in self.demographic_List:
				if not (set(demogs.topics).isdisjoint(set(comedians.themes))):
					good_demog.append(demogs)
			temp = list()
			temp.append(comedian_dict[comedians])
			temp.append(good_demog)
			comedian_dict[comedians] = temp
		
		for demogs in self.demographic_List:
			good_comedians = list()
			for comedians in self.comedian_List:
				if not (set(demogs.topics).isdisjoint(set(comedians.themes))):
					good_comedians.append(comedians)
			temp = list()
			temp.append(demographic_dict[demogs])
			temp.append(good_comedians)
			demographic_dict[demogs] = temp

		for come in comedian_dict:
			come_time[come] = 0
			come_assigned[come] = 0
			temp = comedian_dict[come]
			for i in range(0,2):
				if i == 0:
					temp2 = temp[0]
					for mains in temp2:
						come_time[come] += 2
				if i == 1:
					temp2 = temp[1]
					for test in temp2:
						come_time[come] += 1

		for comes in self.comedian_List:
			come_time_rem[comes] = [0, comedian_dict[comes][0]]

		
		for demos in demographic_dict:
			temp = demographic_dict[demos][0]
			if len(temp) == 1:
				please = temp[0]
				list_ses.append(["", 0, please, demos, "main"])
				come_assigned[please] += 2
				demo_dec.remove(demos)
				come_time_rem[please][0] += 1
				for comes in come_time_rem:
					if demos in come_time_rem[comes][1]:
						come_time_rem[comes][1].remove(demos)
				if come_time_rem[please][0] == 2:
					for demos2 in demo_dict_dec:
						comes = demo_dict_dec[demos2]
						if please in comes:
							demo_dict_dec[demos2].remove(please)
		
							
		
		
		
		for comes in come_time_rem:
			if come_time_rem[comes][0] == 1:
				if len(come_time_rem[comes][1]) != 0:
					for demos in come_time_rem[comes][1]:
						okay = True
						for comes2 in come_time_rem:
							if come_time_rem[comes2][0] == 1:
								if demos in come_time_rem[comes2][1] and comes2 != comes:
									okay = False
						if okay:
							list_ses.append(["", 0, comes, demos, "main"])
							come_assigned[comes] += 2
							demo_dec.remove(demos)
							come_time_rem[comes][0] += 1
							for comes2 in come_time_rem:
								if demos in come_time_rem[comes2][1]:
									come_time_rem[comes2][1].remove(demos)
							for demos2 in demo_dict_dec:
								comes2 = demo_dict_dec[demos2]
								if comes in comes2:
									index2 = comes2.index(comes)
									del demo_dict_dec[demos2][index2]

		

		save = list()
		for demos in demo_dict_dec:
			delete = True
			for demos2 in demo_dec:
				if demos2 == demos:
					delete = False
			if delete:
				save.append(demos)

		for demos in save:
			del demo_dict_dec[demos]
		
		black_list = list()
		stop = False
		while len(list_ses) < 25 and not stop:
			twos = False
			for comes in come_time_rem:
				if len(come_time_rem[comes][1]) > 1:
					twos = True
					break
			if twos:
				length = list()
				for comes in come_time_rem:
					if come_time_rem[comes][0] != 0:
						length.append(0)
					else:
						length.append(len(come_time_rem[comes][1]))
				longest_come = []
				for comes in come_time_rem:
					if len(come_time_rem[comes][1]) == max(length) and comes not in black_list: #itt a baj
						longest_come = comes
						black_list.append(comes)
						break
				length_min = list()
				for demos in come_time_rem[longest_come][1]:
					length_min.append(len(demo_dict_dec[demos]))
				min_two = list()
				for i in range(0,2):
					min_two.append(come_time_rem[longest_come][1][length_min.index(min(length_min))])
					length_min[length_min.index(min(length_min))] = max(length_min) + 1
				for i in range(0,2):
					list_ses.append(["", 0, longest_come, min_two[i], "main"])
					come_assigned[longest_come] += 2
					demo_dec.remove(min_two[i])
					come_time_rem[longest_come][0] += 1
					del demo_dict_dec[min_two[i]]
					if i == 1:
						for demos in demo_dict_dec:
							if longest_come in demo_dict_dec[demos]:
								temp = demo_dict_dec[demos]
								temp.remove(longest_come)
								demo_dict_dec[demos] = temp
					for comes in come_time_rem:
						if min_two[i] in come_time_rem[comes][1]:
							come_time_rem[comes][1].remove(min_two[i])
					
			else:
				stop = True

		for comes in self.comedian_List:
			if come_time_rem[comes][0] == 0 and len(come_time_rem[comes][1]) != 0:
				come_test_dict[comes] = len(comedian_dict[comes][1])
		
		while len(list_ses) < 25:
			length = list()
			for comes in come_test_dict:
				length.append(come_test_dict[comes])
			min_value = min(length)
			min_come = list()
			for comes in come_test_dict:
				if come_test_dict[comes] == min_value:
					min_come = comes
					break
			demo = come_time_rem[min_come][1][0]
			list_ses.append(["", 0, min_come, demo, "main"])
			come_assigned[min_come] += 2
			demo_dec.remove(demo)
			come_time_rem[min_come][0] += 1
			del demo_dict_dec[demo]
			for comes in come_time_rem:
				if demo in come_time_rem[comes][1]:
					come_time_rem[comes][1].remove(demo)
			del come_test_dict[min_come]

		
		demo_test_dict = dict()
		come_test_assigned = dict() 

		for demos in self.demographic_List:
			 demo_test_dict[demos] = demographic_dict[demos][1]
		

		for comes in come_time_rem:
			come_test_assigned[comes] = 0
			if come_time_rem[comes][0] == 0:
				come_test_dict[comes] = [len(comedian_dict[comes][1]) ,comedian_dict[comes][1]]

		
		stop = False
		while len(list_ses) < 50 and not stop:
			fours = False
			for comes in come_test_dict:
				if come_test_dict[comes][0] > 3:
					fours = True
					break
			if fours:
				length = list()
				for comes in come_test_dict:
					length.append(come_test_dict[comes][0])
				max_value = max(length)
				max_come = list()
				for comes in come_test_dict:
					if max_value == come_test_dict[comes][0]:
						max_come = comes
						break		#megvan a legtobb pos testtel rendelkezo comedian
				length_min = list()
				for demos in come_test_dict[max_come][1]:
					length_min.append(len(demo_test_dict[demos])) #itt lehet a baj
				min_four_demo = list()
				for i in range(0,4):
					min_four_demo.append(come_test_dict[max_come][1][length_min.index(min(length_min))])
					length_min[length_min.index(min(length_min))] = max(length_min) + 1
				counter = 0
				for demos in min_four_demo:
					list_ses.append(["", 0, max_come, demos, "test"])
					come_test_assigned[max_come] += 1
					come_test_dict[max_come][0] -= 1
					del demo_test_dict[demos]
					for comes in come_test_dict:
						if demos in come_test_dict[comes][1]:
							come_test_dict[comes][1].remove(demos)
							come_test_dict[comes][0] -= 1
					counter += 1
					if counter == 4:
						del come_test_dict[max_come]
						for demos2 in demo_test_dict:
							if max_come in demo_test_dict[demos2]:
								demo_test_dict[demos2].remove(max_come)
			else:
				stop = True
		
		while len(list_ses) < 50:
			if len(list_ses) == 49:
				last_piece = list()
				for comes in come_test_dict:
					if come_test_dict[comes][0] != 0:
						last_piece = come_test_dict[comes][1][0]
						list_ses.append(["", 0, comes, last_piece, "test"])
						come_test_assigned[comes] += 1
						come_test_dict[comes][0] -= 1
						del demo_test_dict[last_piece]
						for comes2 in come_test_dict:
							if last_piece in come_test_dict[comes2][1]:
								come_test_dict[comes2][1].remove(last_piece)
								come_test_dict[comes2][0] -= 1
						break
			else:
				for comes in come_test_dict:
					if come_test_dict[comes][0] > 1:
						demo_1 = come_test_dict[comes][1][0]
						demo_2 = come_test_dict[comes][1][2]
						list_ses.append(["", 0, comes, come_1, "test"])
						list_ses.append(["", 0, comes, come_2, "test"])
						come_test_assigned[comes] += 2
						come_test_dict[comes][0] -= 2
						del demo_test_dict[demo_1]
						del demo_test_dict[demo_2]
						for comes2 in come_test_dict:
							if demo_1 in come_test_dict[comes2][1]:
								come_test_dict[comes2][1].remove(demo_1)
								come_test_dict[comes2][0] -= 1
							if demo_2 in come_test_dict[comes2][1]:
								come_test_dict[comes2][1].remove(demo_2)
								come_test_dict[comes2][0] -= 1
						break

		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		days_noM = ["Tuesday", "Wednesday", "Thursday", "Friday"]
		day_noF = ["Monday", "Tuesday", "Wednesday", "Thursday"]
		options = [day_noF, days_noM]
		slot_counter = 1
		day_counter = 0
		slot_assigns = list()
		for i in range(0,5):
			day_slots = list()
			for j in range(1,11):
				day_slots.append(j)
			slot_assigns.append(day_slots)
		

		counting = 0
		for i in come_assigned:
			if come_assigned[i] == 4:
				for j in list_ses:
					if i == j[2]:
						j[0] = options[0][day_counter]
						j[1] = min(slot_assigns[days.index(options[0][day_counter])])
						slot_assigns[days.index(options[0][day_counter])].remove(min(slot_assigns[days.index(options[0][day_counter])]))
						day_counter += 1
						counting += 1
						if day_counter == 4:
							options.reverse()
							day_counter = 0

		
		for comes in come_assigned:
			if come_assigned[comes] == 2:
				for ses in list_ses:
					if comes == ses[2]:
						pas = True
						length = list()
						for i in range(0,5):
							length.append(len(slot_assigns[i]))
							if len(slot_assigns[i]) % 2 == 1:
								ses[0] = days[i]
								ses[1] = min(slot_assigns[i])
								slot_assigns[i].remove(min(slot_assigns[i]))
								counting += 1
								pas = False
								break
						if pas:
							min_len = min(length)
							ses[0] = days[length.index(min_len)]
							ses[1] = min(slot_assigns[length.index(min_len)])
							slot_assigns[length.index(min_len)].remove(min(slot_assigns[length.index(min_len)]))
							counting += 1
						break
			if counting == 25:
				break
															
			# else:
			# 	for comes in come_assigned:
			# 		if come_assigned[comes] == 2:
			# 			for ses in list_ses:
			# 				if comes == ses[2]:
		
		for comes in come_test_assigned:
			if come_test_assigned[comes] == 1:
				for ses in list_ses:
					if ses[2] == comes:
						for i in range(0,5):
							if len(slot_assigns[i]) % 2 == 1:
								ses[0] = days[i]
								ses[1] = min(slot_assigns[i])
								slot_assigns[i].remove(min(slot_assigns[i]))
								counting += 1
								break

		for comes in come_test_assigned:
			if come_test_assigned[comes] > 1:
				length = list()
				for dasys in slot_assigns:
					length.append(len(dasys))
				max_two = list()
				for i in range(0,2):
					max_two.append(length.index(max(length)))
					length[length.index(max(length))] = min(length) - 1
				tracker = 0
				switch = 0
				for ses in list_ses:
					if ses[2] == comes:
						ses[0] = days[max_two[switch]]
						ses[1] = min(slot_assigns[max_two[switch]])
						slot_assigns[max_two[switch]].remove(min(slot_assigns[max_two[switch]]))
						counting += 1
						tracker += 1
						if tracker == 2:
							switch = 1
								
		

		for ses in list_ses:
			a = ses[0]
			b = ses[1]
			c = ses[2]
			d = ses[3]
			e = ses[4]
			timetableObj.addSession(a, b, c, d, e)
		


		#This line generates a random timetable, that may not be valid. You can use this or delete it.
		
		#self.randomMainAndTestSchedule(timetableObj)

		#Do not change this line
		return timetableObj


	#This simplistic approach merely assigns each demographic and comedian to a random, iterating through the timetable. 
	def randomMainSchedule(self,timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for demographic in self.demographic_List:
			comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

			timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "main")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 6:
				sessionNumber = 1
				dayNumber = dayNumber + 1

	#This simplistic approach merely assigns each demographic to a random main and test show, with a random comedian, iterating through the timetable.
	def randomMainAndTestSchedule(self,timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for demographic in self.demographic_List:
			comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

			timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "main")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1

		for demographic in self.demographic_List:
			comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

			timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "test")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1
























