import numpy as np
import matplotlib.pyplot as pt
import random

import pandas as pd

num_of_customers = int(input("Pls Enter the number of customers in the simulation"))

Inter_Arrival_Time = np.full(num_of_customers, 0.0)
Arrival_Time = np.full(num_of_customers, 0.0)
Service_Start_Time = np.full(num_of_customers, 0.0)
Waiting_Time = np.full(num_of_customers, 0.0)
Service_Time = np.full(num_of_customers, 0.0)
Completion_Time = np.full(num_of_customers, 0.0)
Time_In_System = np.full(num_of_customers, 0.0)
Available_Time_ATM1 = np.full(num_of_customers, 0.0)
Available_Time_ATM2 = np.full(num_of_customers, 0.0)

Waiting_Customers = 0

Number_in_queue = 0
Maximum_number_in_the_queue = Number_in_queue

Service_Time_Mean = 2
Service_Time_STD = 0.5


#Get a random number using the mean and the standard deviation

def Get_Random(mean, std):
    return np.random.normal(mean, std)

def Do_Histogram(List, name):
    pt.title(name)
    pt.xlabel('Value')
    pt.ylabel('Frequency')
    pt.hist(List, color='blue' , bins = 20)
    filename = name + '.png'
    pt.savefig(filename, format='png')




for i in range(num_of_customers):

    Inter_Arrival_Time[i] = round(random.uniform(0,5),1)
    if i == 0:
        Arrival_Time[i] = Inter_Arrival_Time[i]
    else:
        Arrival_Time[i] = Arrival_Time[i-1] + Inter_Arrival_Time[i]



    Service_Time[i] = round(Get_Random(Service_Time_Mean, Service_Time_STD),1)


    if Arrival_Time[i] >= Available_Time_ATM1[i-1]:
        if Number_in_queue > 0:
            Number_in_queue -= 1
        Service_Start_Time[i] = Arrival_Time[i] + Waiting_Time[i]
        Completion_Time[i] = Service_Time[i] + Service_Start_Time[i]
        Available_Time_ATM1[i] = Completion_Time[i]
        if i != 0:
            Available_Time_ATM2[i] = Available_Time_ATM2[i-1]

    elif Arrival_Time[i] >= Available_Time_ATM2[i-1]:
        if Number_in_queue > 0:
            Number_in_queue -= 1
        Service_Start_Time[i] = Arrival_Time[i] + Waiting_Time[i]
        Completion_Time[i] = Service_Time[i] + Service_Start_Time[i]
        Available_Time_ATM2[i] = Completion_Time[i]
        Available_Time_ATM1[i] = Available_Time_ATM1[i-1]
    else:
        Number_in_queue+=1
        Waiting_Customers+=1
        Waiting_Time[i] = min(Available_Time_ATM2[i-1] , Available_Time_ATM1[i-1]) - Arrival_Time[i]
        Service_Start_Time[i] = Arrival_Time[i] + Waiting_Time[i]
        Completion_Time[i] = Service_Time[i] + Service_Start_Time[i]

        if Available_Time_ATM1[i] < Available_Time_ATM2[i]:
            Available_Time_ATM2[i] = Available_Time_ATM2[i - 1]
            Available_Time_ATM1[i] = Completion_Time[i]
        else:
            Available_Time_ATM1[i] = Available_Time_ATM1[i-1]
            Available_Time_ATM2[i] = Completion_Time[i]


        if Number_in_queue > Maximum_number_in_the_queue:
            Maximum_number_in_the_queue = Number_in_queue

    Time_In_System[i] = Service_Time[i] + Waiting_Time[i]


table = {'Customers': np.arange(1,num_of_customers+1),
         'Inter_Arrival_Time':Inter_Arrival_Time,
         'Arrival_Time' : Arrival_Time,
         'Service Start Time' : Service_Start_Time,
         'Waiting Time' : Waiting_Time,
         'Service Time' : Service_Time ,
         'Completion Time': Completion_Time,
         'Time_In_System':Time_In_System ,
         'Time Available ATM 1': Available_Time_ATM1 ,
         'Time Available ATM 2' : Available_Time_ATM2}


Average_Waiting_Time = Waiting_Time.sum()/len(Waiting_Time)
Total_Time_of_Simulation = Completion_Time[num_of_customers-1]-Inter_Arrival_Time[0]


df = pd.DataFrame(table)
print(df.head(15).to_string(index=False))

print(f"The Average of Waiting Time {round(Average_Waiting_Time,2)}")
print(f"Number of customers who had to wait is {Waiting_Customers}")
print(f"The probability that a customer will have to wait is {round(Waiting_Customers/num_of_customers , 2)}")
print(f"The total time of the simulation is {round(Total_Time_of_Simulation,2)} minutes")
print(f"The average time in system is {round(Time_In_System.sum()/num_of_customers , 2)}")
print(f"The utilization of ATMs is {round(Service_Time.sum()/Total_Time_of_Simulation,2)*100}%")
print(f"The maximum number in the queue is {Maximum_number_in_the_queue}")

Do_Histogram(Waiting_Time , "Waiting Time")
