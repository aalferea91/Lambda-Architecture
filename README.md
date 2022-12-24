# Lambda-Architecture
Project in which I will develop the backend for a lambda architecture simulating a Social Network with specific requirements. 

The following OpenSource technologies will be used along with some AWS services:
- MongoDB
- Flask
- Kafka
- AWS S3/HDFS
- Apache Spark y AWS EMR


## Objectives

The objective is to build the backend of a social network application implementing both the transactional layer and the analytic layer.

The basic funcionalities of our application will be:

### Transactional layer

- The app consists in a feed of text messages that will be shown by time starting from the most recent. The information stored will be: body of the message, date of the message, user, and total number of likes of the message.

- The users will be able to interact with the messages by posting a like or also by deleting the like for each message.
- 
### Analytical layer

The architecture should be able to support the following analytics queries:
 - Number of messages per day/user
 - Number of likes per message/day/user

- Add a non-transactional component that will allow us to follow usage of the application, capturing the time each user spends watching a message. (This data will be simulated but an ingestion an analysis procedure must be built)

### Extra

Implement a system to analyze the sentiment of each message sent by the user and store that information into the database.

<img width="638" alt="1  Introduccion" src="https://user-images.githubusercontent.com/92360704/195833896-8db13c09-97b2-4b0c-8ffe-69a79ee01cc7.PNG">


### Resolution
#### Transactional Layer
1. Database + API

Create a new project in Mongodb and create a database. In this case I used a shared cluster with the recommended configuration with no costs:

![image](https://user-images.githubusercontent.com/92360704/202858849-47e5f3db-f7d3-484c-a68e-4726c3041687.png)

For the security configuration we will use authentication through username and password, and we will add the ip 0.0.0.0/0 to the IP Access List (this is not a good practice in a proffesional environment but for the purpose of this project it's ok).

![image](https://user-images.githubusercontent.com/92360704/202859233-58ef37a5-44a1-4e4e-a658-84fd728ee995.png)

![image](https://user-images.githubusercontent.com/92360704/202859348-f7d4faf4-5e23-4378-a5d2-87348f54d6a3.png)

After the creation of the cluster I will connect to it using Mongodb's native drivers with Python 3.6:

![image](https://user-images.githubusercontent.com/92360704/202859630-9717df5e-8b8e-4e95-821b-3324581aacfa.png)

![image](https://user-images.githubusercontent.com/92360704/202859737-b3db9ecc-cde6-4ce1-9af7-4973a0ab591c.png)

Create a database for our project and a collection to store the comments of the users. Then create a flask API with the following endpoints:
- POST /comments
- GET /comments
- POST /comments/<comment_id>/like\
https://github.com/aalferea91/Lambda-Architecture/blob/main/Database%2BAPI.ipynb

2. Kafka Stream

Run a Kafka server in EC2 that connects to our database and everytime a like gets posted, it goes to Kafka topic. And then the consumer for this topic will be a python script running in EC2 that will update the likes collection in our database.

The reason why we dont include this last call to our database in our API is because its not a good practice to program multiple database actions in the same API (in case that there are a lot of API requests, it might happen that that huge number of requests to the database end up overloading the server).

To create a server with Kafka we will select the following options in EC2:
- Ubuntu Server


![image](https://user-images.githubusercontent.com/92360704/203983375-5f5fd88d-8a30-4a1b-bbf0-6f3766137dfc.png)

![image](https://user-images.githubusercontent.com/92360704/203983451-bf1a5aff-6dc7-4f9b-82c6-9d4114ef1c63.png)

![image](https://user-images.githubusercontent.com/92360704/203983624-c5e68d28-5fe5-40b3-8265-bb1405580495.png)

![image](https://user-images.githubusercontent.com/92360704/203983687-03396eb3-dc8a-436f-b613-bf5f54033896.png)

![image](https://user-images.githubusercontent.com/92360704/203983818-fa4d05e7-f8ff-4188-884b-e3c443f02022.png)

![image](https://user-images.githubusercontent.com/92360704/203983974-c8ba6ac8-c255-48fd-a947-c78674d76f0b.png)

Once the EC2 machine is running, we connect to it through ssh and we execute the following code: (https://github.com/aalferea91/Lambda-Architecture/blob/main/Kafka%20EC2.ipynb)

Now that we have the Kafka installed in our EC2 machine and running, we are going to connect it to our mongodb database through Kafka connector plugin: (https://github.com/aalferea91/Lambda-Architecture/blob/main/Kafka%20Stream.ipynb)

3. Dockerized Kafka Consumer

Only thing left in this part of the architecture is the consumer of Kafka, which in our case it's going to be a microservice in docker. Since we are also running the API in another container, we can combine both in the docker compose file (https://github.com/aalferea91/Lambda-Architecture/tree/main/dockerized)

#### Analytical Layer

To be able to capture the number views of each comment we are going to write to a Kafka topic and then with Spark we will update the collection in our mongodb for the views, and also we will store that information in a S4 bucket, in order to do analytical queries to it. We do it this way in order to separate the transactional database from our analytical database so the queries to our database will never affect the transactional layer.

1. Views Kafka Producer

In this part of the architecture we will simulate that our app has traffic from diverse aplications. We will use the notebook (https://github.com/aalferea91/Lambda-Architecture/blob/main/Views%20Generator.ipynb) to generate a volume of randomized data to our stream in the topic 'views'.

2. Views Kafka Consumer: Spark Streaming

To consume the topic of the views from Kafka we will use Spark. So first of all we will create in AWS a EMR cluster for this purpose (we will use the default options except for the following configurations:

![step1](https://user-images.githubusercontent.com/92360704/209434371-0d0e3ea4-9c51-4203-9c73-450fe0df4409.PNG)

![step2](https://user-images.githubusercontent.com/92360704/209434375-21fcaaf8-c9d2-4b97-b065-ba267a133476.PNG)

Once the cluster is created and running we will use the jupyternotebook option in order to code the actions of our cluster. We will create then a notebook that uses our recently created cluster:

![notebook](https://user-images.githubusercontent.com/92360704/209434488-2c101e36-c029-419c-b576-185850a2ba0e.PNG)

Once the notebook is created, we can open it in a  pyspark instance and execute the code in the following jupyternotebook: (link)
The previous code will: 
1. Process the data from the Kafka stream in the topic views, give it a structure and for for each row update in mongodb in the comments collection the number of views of the comment. 
2. Store the data from the stream in a S3 bucket for later analysis.

 
