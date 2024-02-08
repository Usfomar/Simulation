import random
from prettytable import PrettyTable
import matplotlib.pyplot as pt



# Functions that needed in our simulation
def generate_type():  # This function specifies if the customer express or regular (60% 40%)
    x = random.random()
    if x <= 0.6:
        return "express"
    else:
        return "regular"


def generate_inter_arrival():  # returns the inter-arrival time of each customer
    x = random.random()
    if x < 0.16:
        return 0
    elif x < 0.39:
        return 1
    elif x < 0.69:
        return 2
    elif x < 0.9:
        return 3
    else:
        return 4


def generate_service_time_express():  # returns the service time of express customers
    x = random.random()
    if x < 0.3:
        return 1
    elif x < 0.7:
        return 2
    else:
        return 3


def generate_service_time_regular():  # returns the service time of regular customers
    x = random.random()
    if x < 0.2:
        return 3
    elif x < 0.7:
        return 5
    else:
        return 7


# This function returns the maximum queue length of a cashier
def get_maximum_queue_length(cashier_queue, size_of_cashier):
    maximum = 0
    for index in range(size_of_cashier):
        n = 0
        for i in range(index + 1, size_of_cashier):
            if cashier_queue[index].completion_time > cashier_queue[i].arrival_time:
                n += 1
            maximum = max(maximum, n)
    return maximum

# Do a histogram and save it as png image
def Do_Histogram(l, name):
    pt.title(name)
    pt.xlabel('Value')
    pt.ylabel('Frequency')
    pt.hist(l, color='blue' , bins = 20 , range=(0,50),edgecolor = 'black')
    filename = name + '.png'
    pt.savefig(filename, format='png')
    print(f"Histogram saved to {filename}")




# Class customer
class Customer:
    AllCustomers = []  # All Customers list

    def __init__(self):  # Constructor
        self.id = -1
        self.CustomerType = generate_type()
        self.waiting_time = 0
        self.arrival_time = 0
        self.inter_arrival_time = generate_inter_arrival()
        self.completion_time = 0
        self.CustomerType = generate_type()
        if self.CustomerType == "express":  # Generate service time for each express and regular customer
            self.service_time = generate_service_time_express()

        else:
            self.service_time = generate_service_time_regular()

        Customer.AllCustomers.append(self)  # add all customers to the list called AllCustomers

    # Used for print the customer in friendly way
    def __repr__(self):  # Used to print the Customer class
        return f"Id: {self.id}\tType: {self.CustomerType}\tService Time: {self.service_time}\tInter arrival-time: {self.inter_arrival_time}\tArrival Time: {self.arrival_time}\tCompletion Time: {self.completion_time}\n"


# End of Customer class


# Express Cashier classr
class ExpressCashier:
    Number_of_all_waiting_customers = 0  # Number of waiting customers in Express cashier
    Maximum_length_in_waiting_queue = 0  # Maximum length of waiting queue at the same time
    length_of_the_queue = 0  # Number of waiting customers right now
    AllExpressCustomers = []  # The list that contains all express customers
    available_time = 0  # is the time when the cashier is available
    Idle_time = 0  # The time that the cashier has no customers


# End of Express cashier class


# Regular Cashier class
class RegularCashier:
    Number_of_all_waiting_customers = 0  # Number of waiting customers in Regular cashier
    Maximum_length_in_waiting_queue = 0  # Maximum length of waiting queue at the same time
    AllRegularCustomers = []  # The list that contains all express customers
    length_of_the_queue = 0
    available_time = 0  # is the time when the cashier is available
    Idle_time = 0  # The time that the cashier has no customers
    Number_of_express_customers = 0  # Number of express customers that enters regular customers


# End of Regular Cashier class


# Start simulation

# Get the number of customers from the user
Number_of_Customers = int(input("How many customers: "))
customers = []  # list of customers

Total_Service_Time_Express = 0
Total_Service_Time_Regular = 0

Total_Waiting_Time_Express = 0
Total_Waiting_Time_Regular = 0

Total_Inter_arrival_Time = 0


for i in range(Number_of_Customers):  # Loops on Number of Customers
    customers.append(Customer())
    customers[i].id = i + 1
    Total_Inter_arrival_Time += customers[i].inter_arrival_time

    # Check if the customer is express or regular
    if customers[
        i].CustomerType == "regular" or ExpressCashier.length_of_the_queue > 1.5 * RegularCashier.length_of_the_queue:  # Enter the regular cashier if the type of customer is regular,
        # or he is express but the length of express cashier is more than 1.5* the length of regular cashier

        Total_Service_Time_Regular += customers[
            i].service_time  # Calculate the total service time for regular customers
        if customers[
            i].CustomerType == "express":  # if the customer is express increase the number of express customers in regular cashier by one
            RegularCashier.Number_of_express_customers += 1

        if len(RegularCashier.AllRegularCustomers) == 0:  # compute the arrival time
            customers[i].arrival_time = customers[i].inter_arrival_time
        else:
            customers[i].arrival_time = RegularCashier.AllRegularCustomers[-1].arrival_time + customers[
                i].inter_arrival_time  # get the arrival time by adding the arrival time of the previous customer in the same cashier and the inter-arrival time of current customer

        RegularCashier.AllRegularCustomers.append(customers[i])  # Then add the customer to the list of his cashier

        if customers[i].arrival_time > RegularCashier.available_time:  # Computes the idle time of regular cashier
            RegularCashier.Idle_time += customers[i].arrival_time - RegularCashier.available_time

        if customers[i].arrival_time < RegularCashier.available_time:  # Means that the customer will wait

            RegularCashier.Number_of_all_waiting_customers += 1
            RegularCashier.length_of_the_queue += 1

            # Calculate the waiting time and completion time in case of waiting
            customers[i].waiting_time = RegularCashier.available_time - customers[i].arrival_time
            Total_Waiting_Time_Regular += customers[i].waiting_time
            customers[i].completion_time = customers[i].waiting_time + customers[i].arrival_time + customers[
                i].service_time

        else:  # The customer will not wait
            RegularCashier.length_of_the_queue -= 1  # decrease the length of the waiting queue
            if RegularCashier.length_of_the_queue < 0:
                RegularCashier.length_of_the_queue = 0
                # Calculate the completion time
                customers[i].completion_time = customers[i].arrival_time + customers[i].service_time

        # Update the available time of the cashier
        RegularCashier.available_time = customers[i].completion_time

    else:  # The customer is express and enters the express cashier

        Total_Service_Time_Express += customers[
            i].service_time  # Calculate the total service time for express customers
        if len(ExpressCashier.AllExpressCustomers) == 0:
            customers[i].arrival_time = customers[i].inter_arrival_time
        else:
            customers[i].arrival_time = ExpressCashier.AllExpressCustomers[-1].arrival_time + customers[
                i].inter_arrival_time  # get the arrival time by adding the arrival time of the previous customer in the same cashier and the inter-arrival time of current customer

        ExpressCashier.AllExpressCustomers.append(customers[i])  # Then add the customer to the list of his cashier

        if customers[i].arrival_time > ExpressCashier.available_time:  # Computes the idle time of express cashier
            ExpressCashier.Idle_time += customers[i].arrival_time - ExpressCashier.available_time

        if customers[i].arrival_time < ExpressCashier.available_time:  # Means that the customer will wait

            ExpressCashier.Number_of_all_waiting_customers += 1
            ExpressCashier.length_of_the_queue += 1
            customers[i].waiting_time = ExpressCashier.available_time - customers[i].arrival_time
            Total_Waiting_Time_Express += customers[i].waiting_time
            customers[i].completion_time = customers[i].waiting_time + customers[i].arrival_time + customers[
                i].service_time

        else:  # The customer will not wait
            ExpressCashier.length_of_the_queue -= 1

            if ExpressCashier.length_of_the_queue < 0:  # To prevent the length of the queue become negative
                ExpressCashier.length_of_the_queue = 0

            customers[i].completion_time = customers[i].arrival_time + customers[i].service_time

        # Update the available time of the cashier
        ExpressCashier.available_time = customers[i].completion_time


Number_of_Express_Customers = len(ExpressCashier.AllExpressCustomers)
Number_of_Regular_Customers = len(RegularCashier.AllRegularCustomers)

# Printing the results
Cs = PrettyTable()
Cs.field_names = ["id", "inter_arrival_time", "arrival", "service time", "type", "completion", "waiting"]
for customer in Customer.AllCustomers:
    Cs.add_row(
        [customer.id, customer.inter_arrival_time, customer.arrival_time, customer.service_time, customer.CustomerType,
         customer.completion_time, customer.waiting_time])
print(Cs)

print("Express")
i = 1
express = PrettyTable()
express.field_names = ["Index", "id", "inter_arrival_time", "arrival", "service time", "type", "completion", "waiting"]
for customer in ExpressCashier.AllExpressCustomers:
    express.add_row([i, customer.id, customer.inter_arrival_time, customer.arrival_time, customer.service_time,
                     customer.CustomerType, customer.completion_time, customer.waiting_time])
    i += 1
print(express)
print("-----------------------------------------------------------------------------------------------")
print("Regular")
k = 1
regular = PrettyTable()
regular.field_names = ["Index", "id", "inter_arrival_time", "arrival", "service time", "type", "completion", "waiting"]
for customer in RegularCashier.AllRegularCustomers:
    regular.add_row([k, customer.id, customer.inter_arrival_time, customer.arrival_time, customer.service_time,
                     customer.CustomerType, customer.completion_time, customer.waiting_time])
    k += 1
print(regular)

print(
    f"The number of regular customers is {Number_of_Regular_Customers}\nThe number of express customers is {Number_of_Express_Customers}")
print(f"The number of express customers who enter the regular cashier is {RegularCashier.Number_of_express_customers}")

print(
    f"The average of waiting time of express customers is {round(Total_Waiting_Time_Express / Number_of_Express_Customers)}")
print(
    f"The average of waiting time of Regular customers is {round(Total_Waiting_Time_Regular / Number_of_Regular_Customers)}")

print(
    f"The maximum express cashier queue length is {get_maximum_queue_length(ExpressCashier.AllExpressCustomers, Number_of_Express_Customers)}")
print(
    f"The maximum Regular cashier queue length is {get_maximum_queue_length(RegularCashier.AllRegularCustomers, Number_of_Regular_Customers)}")

print(
    f"The idle time of express cashier is {ExpressCashier.Idle_time}\nThe idle time of regular cashier is {RegularCashier.Idle_time}")

print(
    f"The probability of a customer waits in express cashier is {round(ExpressCashier.Number_of_all_waiting_customers / Number_of_Express_Customers, 2)}")
print(
    f"The probability of a customer waits in regular cashier is {round(RegularCashier.Number_of_all_waiting_customers / Number_of_Regular_Customers, 2)}")

print(f"The Experimental average of inter-arrival time is {round(Total_Inter_arrival_Time / Number_of_Customers, 2)}")
print(
    f"The experimental average of service time of express customers is {round(Total_Service_Time_Express / Number_of_Express_Customers, 2)}")
print(
    f"The experimental average of service time of regular customers is {round(Total_Service_Time_Regular / Number_of_Regular_Customers, 2)}")



# For Doing Histograms
waiting_express_time = []
service_express_time = []
waiting_regular_time = []
service_regular_time = []

for c in ExpressCashier.AllExpressCustomers:
    waiting_express_time.append(c.waiting_time)
    service_express_time.append(c.service_time)

for c in RegularCashier.AllRegularCustomers:
    waiting_regular_time.append(c.waiting_time)
    service_regular_time.append(c.service_time)

Do_Histogram(waiting_express_time , "Waiting Express Time")
Do_Histogram(service_express_time , "Service Express Time")
Do_Histogram(waiting_regular_time , "Waiting Regular Time")
Do_Histogram(service_regular_time , "Service Regular Time")

