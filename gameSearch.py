# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 19:56:02 2023

@author: James
"""
import sqlite3
from gameReturn import *

class Search:
    """
    This is a class which creates objects which store game data.
    It contains a function to add a new object attribute which determines game avaliability.
    """
    def __init__(self, game_id, title,platform,genre):
        
        self.game_id = game_id
        
        self.title = title
        
        self.genre = genre
        
        self.platform = platform
        
    def avalability(self,avaliable):

        self.avaliable=avaliable
        
    def __str__(self):
         
        return f"{self.game_id} copy of {self.title} on {self.platform} in genre {self.genre} is {self.avaliable}"
         
def title_search(title,platform):
    """
    Searches the sql database for games matching a specific title and game platform.
    It takes a title and platform as paramaters.
    It returns a list of tuples containing any search matches
    The tuple contains game id, title, platform and genre data attributes.
    """
    connection = sqlite3.connect('RentalCompany.db')
    cursor = connection.cursor()
    
    query="""
    SELECT  GRD.'Game Id',GC.'Title',GC.'Platform',GG.'Genre'
    FROM 'Game Rental Dates' AS GRD
    INNER JOIN 'Game Catalogue' AS GC ON GC.'Catalogue Index'=GRD.'Catalogue Index'
    INNER JOIN 'Game Genres' AS GG ON GC.'Title'=GG.'Title'
    WHERE LOWER(GC.'Title') = ? and LOWER(GC.'Platform') = ? ;
    """
    cursor.execute(query,(title,platform,))
    result = cursor.fetchall()

    connection.close()
    
    return(result)

def check_game_avaliability(game_copy):
    """
    This checks to see if a game is currently being rented or not.
    It takes a game id as input and returns a boolean expression
    True indicates the game is avaliable to hire.
    """
    return(not(is_game_hired_out(find_rental_periods_for_game(game_copy))[0]))

def get_available_games_info(title,platform):
    """
    This function generates a list of games, along with their availability and other attributes,
    based on a specific game title and platform. It queries the SQL database to find games that match
    the provided title and platform
    The function takes two parameters: the title of the game you wish to find and the platform for that game.
    It returns a list of lists, where each inner list contains the game ID and its attributes, including
    genre, availability, title, and platform.
    """
    
    game_id_list=[]
    games=title_search((title).lower(),(platform).lower())

    for game_id in games:
        game=Search(*game_id)
        
        if (check_game_avaliability(game.game_id))==True:
            game.avalability("Avaliable")
            
        else:
            game.avalability("Not Avaliable")
            
        game_id_list.append(game)

    game_information=[[game.game_id,game.title,game.genre,game.platform,game.avaliable] for game in game_id_list]
    return(game_information)


""" You can test out to see if this function works by uncommenting the below function"""
#print(get_available_games_info("CYBERPUNK 2077","nintendo switch"))