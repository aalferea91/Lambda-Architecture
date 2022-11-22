# Lambda-Architecture
Project in which I will develop the backend for a lambda architecture simulating a Social Network with specific requirements. 

The following OpenSource technologies will be used along with some AWS services:
-MongoDB
-Flask
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
-POST /comments
-GET /comments

