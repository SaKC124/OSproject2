# Devlog for OSProject2
## Log 1: Nov 13 5:55pm
### Right now I am planning on how I should go about doing this program and looking at the python programs given as references to what I need to do and looking at the sample output.Using python, I'm thinking the project will be one python file that will contain multiple methods. Thats all I know for now

## Log 2: Nov 13 8:00pm
### The program will consist of about 3 methods, we will have the main method, a method for customer, and a method for teller. I am going to start probably with creating customer queue, shared resources, global counter, and teller management variables to be used in all methods and start working on the main method and outline both the customer and teller methods along the way

## Log 3: Nov 13 10:10pm
### As I have been doing the main method I have a better idea of how the main method is going to work and what I'm doing for it. The main method starts by creating the teller threads, which after that, the bank opens. The customer threads are then created. The threads will are created for both the customer and teller using for loops. Then a thread will start to manage customer queue amd wait till all customers are done and then tell the tellers to stop and let them fnish their last customer. The main method will essentially outline the process of the relationship between teller and customer and initiate threads, and determines when it ends by tracking the queue. The teller class would do its thing with being assigned to a teller and taking action based off what its requested to do by customer. And customer would wait in queue till teller is available and requests transaction, wait till its done then leaves the bank. I am going to finish the main method and then work on the customer method followed by teller.

## Log 4: Nov 13 11:59pm
### Mostly finished main, but going to start on some of customer method up until the part where teller would recive request from customer and then work on some of the teller method until where the teller recieves customers transaction request

## Log 5: Nov 14 4:11pm
### Finishing up the teller method and customer method. The teller method will run in a while loop as customers are coming to the bank and ends when there are no customers. It will use if else statements to take actions based off of the type of transaction it needs to do. The customer method randomlt will generate for each customer what kind of transavtion its doing and enters door to talk to teller when available. It waits till transaction is done and then leaves the bank. There arent any loops needed for that

## Log 6: Nov 14 10:23pm
### So much is going on and I've written so much that I have to make sure I am not missing anything at all. I'm tracing and checking my program making sure everything looks like it will be called before I run the program, making sure the program is calling the semaphores and the locks and conditions are in and being called. I'm going to do some final touches and start running the program 
