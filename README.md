# SOFT8023-Assignment-1-Spelling-Bee
 
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Patterns](#patterns)
* [Status](#status)

## General info
This is client-server distributed application based on the New York Times’ Spelling Bee game.

## Technologies
* Python: 3.6
* grpc: 1.41.0

## Setup
First run the server.py file to start the server. Next run the client.py file to start the client. Enjoy!!

## Patterns
Patterns used:
* [Template pattern](#template-pattern)
* [Singleton pattern](#singleton-pattern)
* [Factory pattern](#factory-pattern)

### Template pattern

* Where:

* Why:

### Singleton pattern

* Where:

GameRegistry class (located in game_registry.py)

* Why:

This class manages the creation, registration and retrieval of games as they are being requested by the user. We want only one instance of this class to be created so the games created and retrieved are unique. In a single-threaded application this may not make a big difference, but in the next assignments, when we use multithreading and multiple users, this will ensure that multiple users will not get, for example, different instances of the class as this can product undesirable effects (e.g. 2 users trying to play together the same game. One user creates a game using a instance of the GameRegistry.class, and the other users tries to join the game using another different instance of the GameRegistry.class. The second user may not be able to access the game as the game has been created and registered in the first instance)

### Factory pattern

* Where:

* Why:

## Status
This will be further developed in the next assignment.
