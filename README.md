# OSproject2

## This project is a program that runs a simulation of a bank consisting of 3 tellers and 50 customers dealing with widrawal and deposit transactions. This project simulates a bank operations with threads in python, where each thread is either a customer or a teller. The simulation starts once all teller threads are ready and opens the bank, and ends once all threads are done and the bank closes, therefore ending the program.

## The program consists of 3 methods:

## Main method
### Starts the program off by creating threads for the teller and customers, from there the method will call the thread target functions to have tellers be ready and customers lining up with knowing what transaction they want to do before the actual bank simulation starts. The method will also ensure all threads have been completed before letting tellers close the bank and program ends

## Customer Thread Method
### This method runs the customer threads, by randomly assigning the kind of transaction they do and lining up at the bank, and waiting until the teller is available and assigned to them to perform the action and leave the bank. It does all of this while communicating with the teller method that dictates its actions based on the type of transaction performed

## Teller Thread Method
### This method is the star of the show complemented by the customer method. After getting the tellers ready, most of the method runs in a while loop gets customers from a queue, followed by if statements to determine actions that the teller takes based on the type of transaction customer requests. It will keep doing this until there are no more customers in the queue, which each teller will leave for the day after they see no customers are in the queue.
