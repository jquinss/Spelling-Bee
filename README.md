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

WordGame class (located in word_game.py)
GameManager class (located in word_game.py)
LookupService class (located in lookup_service.py)

* Why:

WordGame class
Abstract class containing a skeleton of high level operations that are common to many different word games. Some operations are abstract (implementation needs to be provided by sub-class) and some have already been implemented.

Methods where implementation have been provided (usually common to different word games):
* is_word_in_dictionary => Checks if a word is in a dictionary.
* check_word => Takes a word as argument and returns the word score, total score and a message.
 
Methods where implementation needs to be provided (different word games may have different implementations):
* method calculate_word_score => Calculates the score of the word.
* method evaluate_word => Checks if a word is valid and returns a message.


GameManager class
Abstract class containing a skeleton of high level operations that are common to a game. All 3 methods defined are abstract as different games may implement them differently:
* method setup_game => operations to be performed before the game starts (e.g. initialize some variables, etc.)
* method start_game => operations to be performed during the game.
* method stop_game => operations to be performed when the game ends (e.g. do some calculations, etc.)


LookupService class
Abstract class containing a skeleton of high level operations that are common to a dictionary lookup service. Only the following method has been defined as abstract: 
* load_source_file => loads the data from a file to a dictionary. Different lookup services that use dictionaries may have different ways to load the information depending on the type of file (e.g. json, xml, csv)

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
