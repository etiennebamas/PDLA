import math

#An instance is represented as a list of integers which describe the arrival time of each request. [0, 1, 1, 2] describes one request at time 0, two at time 1 and one at time 2. Time are counted in time units so there is 1/d absolute time inbetween two consecutive times.
#Lambda is the robustness parameter
#heuristic is a list of times at which the heuristic solution sends an ack
#ONLINE_LA returns the total cost of the PDLA algorithm given its input
def ONLINE_LA(instance, d, Lambda, heuristic):
    
    if(len(instance)==0): return 0
    
    cost = 0
    jobs = []
    
    instance = sorted(instance)
    heuristic = sorted(heuristic)
    
    for request in instance:
        jobs.append((request, math.inf, 0))
    
    i = 0
    for times in heuristic:
        while(i<len(jobs) and jobs[i][0]<=times):
            jobs[i]=(jobs[i][0],times,0)
            i+=1
            
    fractionnal_acks = []
    
    c_lambda = (1+1/d)**(Lambda*d)
    c_1_by_lambda = (1+1/d)**(d/Lambda)
        
    time = 0
    while(jobs[len(jobs)-1][2]<1):   
        first = 0
        fractionnal_acks.append(0)
        while(first<len(jobs) and jobs[first][0]<= time):
            
            if(jobs[first][2]>=1): 
                first+=1
                continue
            
            job = jobs[first]
            
            #TODO cap increment by 1
            if(time<job[1]):
                increment = (1/d)*(job[2]+1/(c_1_by_lambda-1))
            
                for j in range(0, len(jobs)):
                    if(jobs[j][0]>time): break
                    if(jobs[j][2]>1): continue
                    jobs[j] = (jobs[j][0],jobs[j][1],jobs[j][2]+increment)
                    
                fractionnal_acks[time]+=increment
                cost+=(1/d)*(c_1_by_lambda/(c_1_by_lambda-1))
                
            else:
                increment = (1/d)*(job[2]+1/(c_lambda-1))
                
                for j in range(0, len(jobs)):
                    if(jobs[j][0]>time): break
                    if(jobs[j][2]>1): continue
                    jobs[j] = (jobs[j][0],jobs[j][1],jobs[j][2]+increment)   

                fractionnal_acks[time]+=increment
                cost+=(1/d)*(c_lambda/(c_lambda-1))
                
            first+=1
        
        time+=1
        
    #print(jobs)
        
    return cost

#TCP_OFFLINE returns the optimum cost and the corresponding list of acknowledgement times for an input
#Based on the dynamic programming algorithm of Dooly et al. in STOC 1998 (see references in the paper)
def TCP_OFFLINE(instance, d):
    
    if(len(instance)==0):
        return ([],0)
 
    instance=sorted(instance)
    
    ack_times_indices = list()
    ack_times = list()
    cost = 0
    
    S = 0
    for request in instance:
        S+=request/d
    
    #same notations as Dooly et al.
    M_min = []
    M_pt = []
    M=[]
    
    n = len(instance)
    
    M.append([0])
    M_min.append(0)
    M_pt.append(0)
    
    M.append([1+instance[0]/d])
    M_min.append(M[1][0])
    M_pt.append(0)
    
    for i in range(2,n+1):
        M_min.append(math.inf)
        M.append([])
        M_pt.append(math.inf)
        for j in range(0,i):
            if(j>0):
                M[i].append(1+(j*(instance[i-1]))/d+M_min[i-j])
            else:
                M[i].append(1+(i*(instance[i-1]))/d+M_min[0])
            if(M[i][j]<M_min[i]):
                M_min[i]=M[i][j]
                M_pt[i]=j
    
    current_size = n
    decrease = M_pt[current_size]
    ack_times_indices.append(current_size-1)
    while(decrease>0):
        current_size = current_size-decrease
        decrease = M_pt[current_size]
        ack_times_indices.append(current_size-1)
        
    ack_times_indices.reverse()
    for i in ack_times_indices:
        ack_times.append(instance[i])
        
        
    cost = M_min[n]-S
    
    return (ack_times,cost)

#given an instance and a solution as a list of acks, compute the cost of this solution on this instance
def cost(instance, d, solution):
    cost = 0
    
    jobs = []
    
    instance = sorted(instance)
    solution = sorted(solution)
    
    for request in instance:
        jobs.append((request, math.inf))
    
    i = 0
    for times in solution:
        while(i<len(jobs) and jobs[i][0]<=times):
            jobs[i]=(jobs[i][0],times)
            i+=1
    
    for job in jobs:
        cost+=(1/d)*(job[1]-job[0])

    return (cost+len(solution))