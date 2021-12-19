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
* pika: 1.2.0

## Setup
First run the game_server.py file to start the game server. Next run the game_client.py file to start the client.
Optionally run the stats_server.py and stats_client.py
Enjoy!!

## Patterns
Patterns used:
* [Template pattern](#template-pattern)
* [Singleton pattern](#singleton-pattern)
* [Factory pattern](#factory-pattern)

### Template pattern

* Where:

WordGame class (located in domain/word_game.py)  
GameManager class (located in domain/word_game.py)  
LookupService class (located in services/lookup_service.py)  

* Why:

**WordGame class**  
Abstract class containing a skeleton of high level operations that are common to many different word games. Some operations are abstract (implementation needs to be provided by sub-class) and some have already been implemented.

Methods where implementation have been provided (usually common to different word games):
* is_word_in_dictionary => Checks if a word is in a dictionary.
* check_word => Takes a word as argument and returns the word score, total score and a message.
 
Methods where implementation needs to be provided (different word games may have different implementations):
* calculate_word_score => Calculates the score of the word.
* evaluate_word => Checks if a word is valid and returns a message.


**GameManager class**  
Abstract class containing a skeleton of high level operations that are common to a game. All 3 methods defined are abstract as different games may implement them differently:
* setup_game => operations to be performed before the game starts (e.g. initialize some variables, etc.)
* start_game => operations to be performed during the game.
* stop_game => operations to be performed when the game ends (e.g. do some calculations, etc.)


**LookupService class**  
Abstract class containing a skeleton of high level operations that are common to a dictionary lookup service. Only the following method has been defined as abstract: 
* load_source_file => loads the data from a file to a dictionary. Different lookup services that use dictionaries may have different ways to load the information depending on the type of file (e.g. json, xml, csv)


### Singleton pattern

* Where:

GameRegistry class (located in services/game_registry.py)

* Why:

**GameRegistry class**  
This class manages the creation, registration and retrieval of games as they are being requested by the user. We want only one instance of this class to be created so the games created and retrieved are unique. In a single-threaded application this may not make a big difference, but in the next assignments, when we use multithreading and multiple users, this will ensure that multiple users will not get, for example, different instances of the class as this can produce undesirable effects (e.g. 2 users trying to play together the same game. One user creates a game using a instance of the GameRegistry.class, and the other users tries to join the game using another different instance of the GameRegistry.class. The second user may not be able to access the game as the game has been created and registered in the first instance)


### Factory pattern

* Where:

SpellingBeeGameFactory class (located in domain/word_game.py)
LookupServiceFactory class (located in services/lookup_service.py)

* Why:

**SpellingBeeGameFactory class**

We define the factory method "create_game" that encapsulates the creation of word games of type SpellingBee. By passing parameters of game_mode and word_lookup_service, we can retrieve a custom SpellingBee game. For instance, to create a multi-player game we pass the "MultiCoop" parameter as game_mode and a particular word lookup service that we want to use. If in the future we want to add more types or other lookup services we just need to modify this class.

**LookupServiceFactory class**

In this case we define the factory method "create_lookup_service" that encapsulates the creation of lookup services. By passing parameters of lookup_type and source_files_dict, we can retrieve a custom lookup service. For example, in the SpellingBee game we create a JSON Lookup service by passing the "JSON" parameter as lookup_type and a dictionary containing JSON source files. If in the future we need to create another lookup service (e.g. that retrieves information from XML files) we just need to extend the LookupService class (e.g. add a XMLLookupService class) and modify this method to include that class.

## Status
Could be further developed to include a Multiplayer competitive mode, etc.
