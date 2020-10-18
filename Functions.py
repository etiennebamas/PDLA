import random
import math
import numpy as np
import matplotlib.pyplot as plt

#generates one random entry
def entry_generator(mean, n, shape, key):
    
    if(key == "Pareto"):
        return round(np.random.pareto(shape))
    
    X = mean
    for a in range(0,n):
        X = np.random.poisson(X)
    
    return X

#generates a full instance of some length using the function entry_generator for each entry
#mean value, length of instance, number of iterations n as inputs
def instance_generator(mean, length, n, shape, key):
    
    instance = []
    for i in range(0, length):
        x = entry_generator(mean, n, shape, key)
        for j in range(0,x):
            instance.append(i)
        
    return instance

#from an instance described as a list of requests, generates an array T with T[i]=# of requests at time i
def agreggate_instance(instance):
    
    instance=sorted(instance)
    
    if(len(instance)==0): return []
    
    min_time = instance[0]
    max_time = instance[len(instance)-1]
    
    instance_agreggated = [0]*min_time
    
    current = 0
    for time in range(min_time, max_time+1):
        instance_agreggated.append(0)
        while(current<len(instance) and instance[current] == time):
            instance_agreggated[time]+=1
            current+=1
            
    return instance_agreggated

#reverse operation of agreggate_instance, from an array T with T[i]=# of requests at time i, outputs an instance described as a list of requests
def deagreggate_instance(instance):
    
    result = []
    
    for i in range(0, len(instance)):
        for x in range(0, instance[i]): result.append(i)
            
    return result

#generates a noisy instance from an instance
#replacement_rate is the replacement rate described in the main paper
def noisy_instance(instance, mean, n, shape, key, replacement_rate):
        
    instance_agreggated = agreggate_instance(instance)
    
    instance_agreggated_noisy = [0]*len(instance_agreggated)
    
    for i in range(0,len(instance_agreggated)):
        drop = (random.random()<replacement_rate)
        insert = (random.random()<replacement_rate)
        instance_agreggated_noisy[i]=instance_agreggated[i]
        if(drop): instance_agreggated_noisy[i]=0
        if(insert): instance_agreggated_noisy[i]+=entry_generator(mean, n, shape, key)
                
            
    final_instance = deagreggate_instance(instance_agreggated_noisy)
    
    return final_instance

#plots an instance as an histogram
def plot_instance(instance):
    
    instance_agreggated=agreggate_instance(instance)
    
    plt.plot(instance_agreggated)
    plt.ylabel('number of requests')
    plt.xlabel('time')
    plt.show()
    
    return 0

