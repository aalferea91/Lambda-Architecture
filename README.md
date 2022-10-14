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
