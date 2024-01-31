# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 20:25:19 2023

@author: James
"""
from gameReturn import find_rental_periods_for_game,is_game_hired_out
from datetime import *
import sqlite3
import subscriptionManager_v11
from subscriptionManager_v11 import *

def insert_new_data_into_game_rentals(game_rental_data):
    """
    Same function as in database.py file.
    This function inserts new rental entries into the game rental table 
    within the rental company database.
    It takes paramater which is a tuple object as input, 
    this tuple consists of the rental index value, customer id and game id.
    """
    connection_to_sql_database=sqlite3.connect('RentalCompany.db')
    cursor=connection_to_sql_database.cursor()

    sqlite_insert_record_query="""Insert into 'Game Rentals' ('Rental Index','Customer Id','Game Id') VALUES (?,?,?)"""
    
    connection_to_sql_database.execute(sqlite_insert_record_query,game_rental_data)
    connection_to_sql_database.commit()
    connection_to_sql_database.close()
    
def insert_new_data_into_rental_periods(rental_period_data):
    """
    Same function as in database.py file.
    This function inserts new rental entries into the rental period table 
    within the rental company database.
    It takes a paramater which is a tuple object as input, 
    this tuple consists of the rental index value, rental start date and rental end date.
    """
    connection = sqlite3.connect('RentalCompany.db')
    cursor = connection.cursor()

    insert_query = """INSERT INTO 'Rental Periods' ('Rental Index', 'Rental Start Date', 'Rental End Date') VALUES (?,?,?)"""
    
    cursor.execute(insert_query, rental_period_data)
    connection.commit()
    connection.close()

def latest_customer_index():
    """
    This function look in the game rental table for the maximum rental index value.
    It returns this value.
    """
    connection = sqlite3.connect('RentalCompany.db')
    cursor = connection.cursor()
    query="""SELECT MAX(`Rental Index`) FROM 'Game Rentals' ORDER By 'Rental Index' """
    cursor.execute(query)
    row = (cursor.fetchone())[0]
    return(row)


def insert_new_rental_into_database(customer_id,game_id,formatted_date):
    """
    This function insert new data into the the sql rental database
    It insert a new rental occurence into the game rentals table and rental periods table.
    The input paramaters are the customer id, game id and formatted date.
    """
    new_rental_index = int(latest_customer_index()) + 1
    
    data_tuple = (new_rental_index, customer_id, game_id)
    
    insert_new_data_into_game_rentals(data_tuple)
    
    data_tuple=(new_rental_index,formatted_date,"")
    
    insert_new_data_into_rental_periods(data_tuple)


def does_customer_have_account(customer_id,customer_subscription_dictionary):
    """
    This function checks if inputted customer id has an account with the rental company.
    It takes a customers id and a dictionary containing all customer subscription information.
    It returns a boolean expression which is True if the customer account exists.
    """
    customer_account_status=True
    
    if (customer_subscription_dictionary.get(str(customer_id)))==None:
        
        customer_account_status=False
    
    return(customer_account_status)

def decision_process(customer_id,customer_subscription_dictionary):
    """
    This determines if a customer has an active subscription so they can rent games.
    It takes two inputs paramaters a customer id and a dictionary with all customer subscription data.
    It outputs a tuple containing a boolean and str value.
    The str value is a message telling the status of the customer account.
    It uses the subscriptionManager_v11 check_subscription to see if the customer has an active subscription.
    Active,Inactive, or Non Existent
    """
    check_customer_rentals=False
    reason="Customer has active subscription with account."
    
    if does_customer_have_account(str(customer_id),customer_subscription_dictionary)==True:
        
        if (check_subscription(str(customer_id),customer_subscription_dictionary))==True:
            check_customer_rentals=True
            
        else:
            reason="Customer has no active subscription plan."
    else:
        reason="No record of customer having an account."
    
    return(check_customer_rentals,reason)

def find_all_rental_periods_for_customer(customer_id):
    """
    This searches the sql database rental period table for all instances a customer rents out any game.
    It takes input as the customer_id and returns a list of tuples containing game hire rental end dates
    belonging to that customer.
    """
    connection = sqlite3.connect('RentalCompany.db')
    cursor = connection.cursor()

    query = """
            SELECT RP.'Rental End Date'
            FROM 'Rental Periods' AS RP
            INNER JOIN 'Game Rentals' AS GR ON GR.'Rental Index' = RP.'Rental Index'
            WHERE GR.'Customer Id' = ?
            """

    cursor.execute(query, (customer_id,))

    result = cursor.fetchall()
        
    connection.close()

    return result

def how_many_active_rentals(rental_end_dates):
    """
    This function is responsible for determining how many games a customer has hired and not returned.
    It takes input in the form of rental end dates belonging to a customer.
    The return is a value which is the total number of active game rentals.
    """
    number_of_active_customer_rentals=0
    
    for rental_end in rental_end_dates:
        
        if rental_end[0]==None or rental_end[0]=="":
            
            number_of_active_customer_rentals+=1

    return(number_of_active_customer_rentals)

def can_customer_rent_another_game(customer_id,game_id):
    """
    This function determines if a customer can rent a game and if that game is avaliable,
    provided that both attributes are correct a rental record is made in the rental database.
    The subscriptionManager_v11 functions load_subscriptions is used to convert a text file containing
    subscription data into a dictionary and the get_rental_limit is used for each customer to determine
    how many games they can rent based on there subscription.
    The input parameters are the customer_id of interest and the game_id of interest.
    The return value is a str which tells you what the rental decision.
    
    """
    todays_date=datetime.today()
    formatted_date = todays_date.strftime("%d-%m-%Y")

    customer_subscription_dictionary=load_subscriptions(r"Customer Subscription Data.txt")
    
    """The decision variable returns a tuple made up of a boolean  and string.
    If the boolean value is True it means the customer_id is an active subscription.
    The string specifys the reason if the boolean value is false"""
    decision=(decision_process(customer_id,customer_subscription_dictionary))
    
    """The game_avaliability variable returns a single boolean value, 
    a true value means the game id of interest is avalaible to rent."""
    game_avaliability=not(is_game_hired_out(find_rental_periods_for_game(game_id)))[0]

    if game_avaliability==True and decision[0]==True:
        
        current_number_of_rentals=(how_many_active_rentals(find_all_rental_periods_for_customer(customer_id)))
        subscription_service=get_rental_limit((customer_subscription_dictionary.get(str(customer_id)).get("SubscriptionType")))
        
        if (subscription_service+1) > current_number_of_rentals:
            insert_new_rental_into_database(customer_id,game_id,formatted_date)
            rental_decision=(f"Game Id {str(game_id)} succesfully rented out to {str(customer_id)}.")
       
        else:
            rental_decision=(f"{str(customer_id)} has too many active subscriptions currently.")
            
    elif game_avaliability==False and decision[0]==True:
        rental_decision=(f"Game Id {str(game_id)} currently rented out to another customer.")
    
    elif game_avaliability==True and decision[0]==False:
        rental_decision=(decision[1])
        
    elif game_avaliability==False and decision[0]==False:
        rental_decision=decision[1] + f"and Game Id {str(game_id)} currently rented out to another customer"
    
    return(rental_decision)
""" To test the function, uncomment the line below and run it to see if it correctly outputs the code
    succesful application should mean the last row in the sql dataframe should be the new value added"""
    
#print(can_customer_rent_another_game("9967","50"))
#connection = sqlite3.connect('RentalCompany.db')
#cursor = connection.cursor()
#query="""SELECT * FROM 'GAME RENTALS'"""
#cursor.execute(query)
#result = cursor.fetchall()
#print(result)
#connection.close()