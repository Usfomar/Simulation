#Performing 10 simulation runs for PortaCome problem
# and determine the probability of loss, the maximum profit,the maximum lass, and the avergae profit and draw histograms
import random
import math
import matplotlib.pyplot as pt

# Variables
Selling_Price_Per_Unit = 249
Total_Fixed_Cost = 1000000

Parts_Cost = []
Direct_Labor_Cost = []
First_Year_Demand = []

Outcome = []
Profit = []


Loss_Counter = 0
Largest_Profit = 0
Smallest_Profit = 0


# This num is a generated number from zero to one
def Generate_Direct_Labor_Cost(num):
    if num < 0.1:
        return 43
    elif num < 0.3:
        return 44
    elif num < 0.7:
        return 45
    elif num < 0.9:
        return 46
    else:
        return 47


# Function to generate a random number from a normal distribution
def random_normal(mean, std_dev):
    u1 = random.random()
    u2 = random.random()
    z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
    return z0 * std_dev + mean


# This function creates the histograms
def Do_Histogram(List, name):
    pt.title(name)
    pt.xlabel('Value')
    pt.ylabel('Frequency')
    pt.hist(List, color='blue' , bins = 10)
    filename = name + '.png'
    pt.savefig(filename, format='png')



Number_of_Runs = int(input("Enter the number of runs: "))

for i in range(Number_of_Runs):

    Parts_Cost.append(int(random.uniform(80, 100)))
    Direct_Labor_Cost.append(Generate_Direct_Labor_Cost(random.random()))  # generate a random num from zero to one and send it as a param to Generate_C1 To return the value
    First_Year_Demand.append(random_normal(15000, 4500))
    Outcome.append(int((249 - Parts_Cost[i] - Direct_Labor_Cost[i]) * First_Year_Demand[i] - Total_Fixed_Cost))

    # Get The largest and the smallest profit value
    if Outcome[i] > Largest_Profit:
        Largest_Profit = Outcome[i]
    if Outcome[i] < Smallest_Profit:
        Smallest_Profit = Outcome[i]

    if Outcome[i] < 0:
        Loss_Counter += 1


for item in Outcome:
    if item >= 0:
        Profit.append(item)




Prob_of_Loss = float(Loss_Counter / Number_of_Runs)
Profit_Average = sum(Profit) / len(Profit)

pt.hist(Parts_Cost , color = 'blue' , bins=10)
pt.title('Parts Costs')
pt.savefig('Parts_Cost.png' , format='png')

pt.hist(Outcome , color ='blue' , bins=10)
pt.title('Outcome')
pt.savefig('Outcome.png' , format='png')

Do_Histogram(Direct_Labor_Cost , 'Direct_Labor_Cost')
Do_Histogram(First_Year_Demand , 'First_Year_Demand')


# Do_Histogram(Outcome, 'Profit Histogram')
# Do_Histogram(First_Year_Demand, 'First Year Demand Histogram')
# Do_Histogram(Direct_Labor_Cost, 'Direct Labor Cost Histogram')
# Do_Histogram(Parts_Cost, 'Parts Cost Histogram')

print(f"The probability of loss in this model for {Number_of_Runs} Runs is {Prob_of_Loss}")
print(f"The maximum Profit: {Largest_Profit}")
print(f"The maximum loss : {abs(Smallest_Profit)}")
print(f"The average of the profit values is: {Profit_Average}")
