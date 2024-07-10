import numpy as np
import random
import statistics
import math
# importing all required libraries

class Social_Analysis:
    # defining a new class for our project
    def _init_(self, friends, message, time):
        # initialisation
        self.friends = np.array(friends) # this graph only represents the adjancy matrix of the graph (kinda followers-following)
        self.temp_friends = np.array(friends)
        for i in range(min([self.friends.shape[0],self.friends.shape[1]])):
            self.temp_friends[i][i] = 0
        if (self.friends.shape[0]!=self.friends.shape[1]):
            print("Warning! The adjacency friends of a graph is always a square friends but the argument friends isn't a square friends")
        self.time = np.array(time) # time is basically how old is the account in days
        self.message = np.array(message) # -ve values actually means there is no message between the users
        # decimal value in message recevied from a person / message sent to that person
        
    def mode(self, array):
        # returns the mode value of an array
        return statistics.multimode(list(array))
    
    def inverse(self, array):
        # inverse of an array
        return np.linalg.inv(array)
    
    def remove_negvalue(self,list):
        # remove -ve values from
        new_list = []
        for i in list:
            if i>=0:
                new_list.append(i)
        return new_list
    
    def npopular_ids(self, n_popular = 1, no_of_tries = 100, no_of_iteration = 1000):
        # This functions displays n most famous persons
        # no_of_tries is the no of times the code runs
        # no_of_iteration means the no of times we go to a person and choose and a radom person from it's followers list and increase the person's point
        popular_arr = np.zeros((n_popular,no_of_tries))
        for i in range(no_of_tries):
            points = np.zeros(self.friends.shape[0])
            person = random.randint(0,self.friends.shape[0]-1)
            for j in range(no_of_iteration*self.friends.shape[0]):
                points[person] += 1
                friends = []
                for k in range(self.friends.shape[1]):
                    if (self.friends[person][k]==1):
                        friends.append(k)
                person = friends[random.randint(0,len(friends)-1)]
            temp = np.argsort(points)[::-1][:n_popular]
            for m in range(n_popular):
                popular_arr[m][i] = temp[m]
        most_famous = np.full(n_popular,0)
        for n in range(n_popular):
            most_famous[n] = int(self.mode(popular_arr[n])[0]) # taking the most occuring value
        return most_famous
    
    def fake_ids(self, depth=50, starting_person=None, threshold_percent=0.25, threshold_message=0.6, threshold_message_ratio=0.8, threshold_time=10):
        # determining fake ids in a social network
        depth = depth*self.friends.shape[0]
        if (starting_person==None):
            starting_person = self.npopular_ids() # By default the starting person is the most famous person
        points = np.zeros(self.temp_friends.shape[0])
        multiplier = np.zeros(self.temp_friends.shape[0])
        pre_multiplier = np.full(self.temp_friends.shape[0],1.0)
        temp_multiplier = np.zeros(self.temp_friends.shape[0])
        for i in range(self.temp_friends.shape[1]):
            multiplier[i] = self.temp_friends[starting_person,i]
        for i in range(depth):
            for j in range(self.temp_friends.shape[0]):
                points[j] += pre_multiplier[j]*multiplier[j] # both factors pre_mutiplier and multipliers are multiplied with each other
            for j in range(self.temp_friends.shape[0]):
                if (multiplier[j]!=0):
                    for k in range(self.temp_friends.shape[1]):
                        temp_multiplier[k] += self.temp_friends[j][k]
            pre_multiplier = multiplier
            multiplier = temp_multiplier            
        x = points[np.argsort(points)[::-1][0]]
        for i in range(self.temp_friends.shape[0]):
            points[i] = points[i]/x
        # All the elements in y are peoples which are the 25% most suspectible persons who can be fake
        y = np.argsort(points)[0:(math.ceil(self.friends.shape[0]*threshold_percent)):1]
        z = []
        for i in y:
            if (self.time[i]>=threshold_time):
                z.append(i)
        # All the elements in z are peoples who can still be fake even after applying threshold_time
        fake = []
        message_list = np.array(self.remove_negvalue(self.message[i]))
        for i in z:
            if (message_list[np.argsort(message_list)[::-1][len(message_list)-math.floor(threshold_message*len(message_list))+1]] < threshold_message_ratio):
                fake.append(i)
        return fake
    
    def fake_ids_points(self, depth=50, starting_person=None):
        # gives relative score for every node
        depth = depth*self.friends.shape[0]
        if (starting_person==None):
            starting_person = self.npopular_ids()
        points = np.zeros(self.temp_friends.shape[0])
        multiplier = np.zeros(self.temp_friends.shape[0])
        pre_multiplier = np.full(self.temp_friends.shape[0],1.0)
        temp_multiplier = np.zeros(self.temp_friends.shape[0])
        for i in range(self.temp_friends.shape[1]):
            multiplier[i] = self.temp_friends[starting_person,i]
        for i in range(depth):
            for j in range(self.temp_friends.shape[0]):
                points[j] += pre_multiplier[j]*multiplier[j]
            for j in range(self.temp_friends.shape[0]):
                if (multiplier[j]!=0):
                    for k in range(self.temp_friends.shape[1]):
                        temp_multiplier[k] += self.temp_friends[j][k]
            pre_multiplier = multiplier
            multiplier = temp_multiplier            
        x = points[np.argsort(points)[::-1][0]]
        for i in range(self.temp_friends.shape[0]):
            points[i] = points[i]/x
        return points
    
    def new_friend_suggestion(self, threshold_friend = 0.34, depth=50):
        # It suggest new friends
        reliability = self.fake_ids_points(depth)
        suggestion = np.full((self.temp_friends.shape[0],self.temp_friends.shape[1]),0)
        for i in range(self.temp_friends.shape[0]):
            for j in range(self.temp_friends.shape[1]):
                if (self.temp_friends[i,j]==1):
                    for k in range(self.temp_friends.shape[1]):
                        if (self.temp_friends[j,k]==1 and self.temp_friends[i,k]==0):
                            # i and j are friends and j and k are friends but i and k are not friends thus suggesting it as a new connection
                            suggestion[i,k] = (1*reliability[k]>threshold_friend)
        for i in range(min([self.friends.shape[0],self.friends.shape[1]])):
            suggestion[i][i] = 0
        return suggestion
                            
                            
graph= [[1, 0, 0, 0, 1, 0, 0, 1],
        [0, 1, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 1, 0, 1, 1],
        [1, 0, 1, 1, 0, 0, 1, 1]]
message = [[-1, 100, 1.61, 0.96, 1.0, 0.2, 4, 1],
          [0, -1, 0.2, 0, 1.66, 1.56, 1.72, 1.31],
          [0.62, 5, -1, 2, 0.23, 0.4, 100, 0],
          [1.04, 100, 0.5, -1, 0, 1.0, 0.5, 0],
          [1.0, 0.6, 4.34, 100, -1, 1.66, 100, 1.0],
          [5, 0.64, 2.5, 1.0, 0.6, -1, 0, 1.0],
          [0.25, 0.58, 0,2, 0, 100, -1, 1.0],
          [1.0, 0.76, 100, 100, 1.0, 1.0, 1.0, -1]]
time = [500,234,1,435,20,59,96,104,200,365]

graph2 = [[1, 0, 0, 0, 1, 0, 0, 1],
          [0, 1, 0, 0, 0, 1, 0, 1],
          [0, 0, 1, 0, 1, 0, 0, 0],
          [0, 1, 0, 1, 0, 1, 0, 1],
          [0, 0, 0, 0, 1, 1, 0, 1],
          [1, 0, 0, 0, 0, 1, 0, 1],
          [0, 0, 0, 1, 0, 0, 1, 1],
          [0, 0, 1, 0, 0, 0, 1, 1]]
message2 = [[-1, 100, 1.61, 0.96, 1.0, 0.2, 4, 1],
          [0, -1, 0.2, 0, 1.66, 1.56, 1.72, 1.31],
          [0.62, 5, -1, 2, 0.23, 0.4, 100, 0],
          [1.04, 100, 0.5, -1, 0, 1.0, 0.5, 0],
          [1.0, 0.6, 4.34, 100, -1, 1.66, 100, 1.0],
          [5, 0.64, 2.5, 1.0, 0.6, -1, 0, 1.0],
          [0.25, 0.58, 0,2, 0, 100, -1, 1.0],
          [1.0, 0.76, 100, 100, 1.0, 1.0, 1.0, -1]]
time2 = [3,9,150,357,96,199,675,909,56,99]

friends = Social_Analysis(graph,message,time)
print(friends.npopular_ids(8))
print(friends.fake_ids_points())
print(friends.fake_ids_points(50,4)) # Almost same even if we change the starting person
print(friends.fake_ids())
print(friends.new_friend_suggestion(0.30))

friends2 = Social_Analysis(graph2,message2,time2)
print(friends2.npopular_ids(8))
print(friends2.fake_ids())
print(friends2.new_friend_suggestion(0.15))