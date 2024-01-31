# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 18:36:42 2023

@author: James
"""

import sqlite3
import datetime
#This module is responsbile for returning games when provided with a game id.
def does_game_exist(game_id):
    """ 
    Determines if a game with the specified game_id exists within the database.
    It takes the parameter game id and returns a boolean expression, true if game
    exists and false if games does not exist.
    """
    connection_to_sql_database=sqlite3.connect('RentalCompany.db')
    cursor=connection_to_sql_database.cursor()

    cursor.execute("SELECT COUNT(*) FROM 'Game Rental Dates' AS GRD WHERE GRD.'Game Id' =? ", (game_id,))

    game_id_existence =(cursor.fetchone())[0] > 0
    
    connection_to_sql_database.close()
    
    return(game_id_existence)

def find_rental_periods_for_game(game_id):
    """
    This collects all rental periods associsated with a specific game id from the database.
    It takes the parameter game id and returns a list of tuples with each tuple representing
    a single return date for that particular game id. 
    """
    connection = sqlite3.connect('RentalCompany.db')
    cursor = connection.cursor()

    query = """
            SELECT RP.'Rental End Date'
            FROM 'Rental Periods' AS RP
            INNER JOIN 'Game Rentals' AS GR ON GR.'Rental Index' = RP.'Rental Index'
            WHERE GR.'Game Id' = ?
            """

    cursor.execute(query, (game_id,))

    result = cursor.fetchall()

    connection.close()

    return result

def is_game_hired_out(rental_end_dates):
    """
    This deduces whether a game is currently hired out based on its rental dates.
    It takes input in the form of a list of tuples containing rent dates.
    It returns a tuple made up of a boolean and a string. The string is a message
    which identifies if the game id has multiple open rentals due to an error.
    Whilst the boolean value if True indicates the game can be returned or false
    the game is currently at the store.
    """
    open_return=0
    description="Game ID is rented out already."

    for rental_end in rental_end_dates:
        if rental_end[0]==None or rental_end[0]=="":
            
            open_return+=1
     
    if open_return>1:
         description="Game Id Rented out multiple times at same time"
         response=True
         
    elif open_return==1:
        response=True
        
    else:
        response=False 
        description="Game ID is avaliable to rent out."
        
    return(response,description)

def update_rental_period_table(game_id):
    """
    This updates the rental period sql table in the database by setting the rental end
    dates to todays date for the given game ids.
    It take the game id as input.
    """

    todays_date=datetime.date.today()
    formatted_date = todays_date.strftime("%d-%m-%Y")
    connection = sqlite3.connect('RentalCompany.db')
    new_cursor = connection.cursor()

    query = """
        UPDATE `Rental Periods`
        SET `Rental End Date` = ?
        WHERE `Rental Index` IN (
            SELECT `Rental Index`
            FROM `Game Rentals`
            WHERE `Game Id` = ?
        )
        AND (`Rental End Date` IS NULL OR `Rental End Date` = '')
        """

    new_cursor.execute(query,(formatted_date, game_id,))

    connection.commit()
    connection.close()

def returning_game(game_id):
    """
    This function processes the return of a game by updating its rental status in the sql database
    if the game exists and if the game can be returned.
    It takes game id as input and returns a str message indicating the outcome of the rental return.
    
    """
    message=(f"{str(game_id)} does not exist in rental company database,\
please double check you have inputed the correct game id to return.")
    if does_game_exist(game_id)==True:
        
        rental_dates=find_rental_periods_for_game(game_id)
        
        game_rental_status=is_game_hired_out(rental_dates)[0]
        
        if game_rental_status==True:
            update_rental_period_table(game_id)
            message=(f"{str(game_id)} successfully returned.")
            
        else:
            message=(f"{str(game_id)} is currently avaliable for hire, please double check you have inputed the correct game id.")

    return(message)

#