# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 22:24:48 2023

@author: James
"""
import sqlite3
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def month_to_int(month_name):
    """
    This converts a month into its corresponding datetime integer value.
    It takes input in the format of a string and returns an integer value.
    """
    month_dict = {
        'january': 1,
        'february': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11,
        'december': 12
    }
    return month_dict.get(month_name.lower())

def get_dataframe_for_genre_popularity():
    """
    This retrieves every rental entry within the sql rental business database
    It gathers the rental index,genre,rental start and rental end dates.
    It then returns this as a dataframe. This dataframe is used to
    identify the most popular genres.
    """
    connection = sqlite3.connect('RentalCompany.db')
    cursor = connection.cursor()
    
    query="""
    SELECT GR.'Rental Index',GG.'Genre',GP.'Rental Start Date',GP.'Rental End Date'
    FROM 'Game Rentals' as GR
    INNER JOIN'Rental Periods' as GP on GP.'Rental Index'=GR.'Rental Index'
    INNER JOIN'Game Rental Dates' as GRD ON GRD.'Game Id'=GR.'Game Id'
    INNER JOIN'Game Catalogue' as GC ON GC.'Catalogue Index'=GRD.'Catalogue Index'
    INNER JOIN'Game Genres'as GG ON GC.'Title'=GG.'Title'
    """
    
    df = pd.read_sql_query(query, connection)
    
    connection.close()
    return(df)

def get_dataframe_for_title_popularity():
    """
    This retrieves every rental entry within the sql rental business database
    It gathers the rental index,game title,rental start and rental end dates.
    It then returns this as a dataframe. This dataframe is used to
    identify the most popular titles.
    """
    connection = sqlite3.connect('RentalCompany.db')
    cursor = connection.cursor()
    
    query="""
    SELECT GR.'Rental Index',GC.'Title',GP.'Rental Start Date',GP.'Rental End Date'
    FROM 'Game Rentals' as GR
    INNER JOIN'Rental Periods' as GP on GP.'Rental Index'=GR.'Rental Index'
    INNER JOIN'Game Rental Dates' as GRD ON GRD.'Game Id'=GR.'Game Id'
    INNER JOIN'Game Catalogue' as GC ON GC.'Catalogue Index'=GRD.'Catalogue Index'
    """
    
    df = pd.read_sql_query(query, connection)
    
    connection.close()
    return(df)

def most_popular_title_for_month(month):
    """
    This function determines the most popular game titles for a given month.
    It takes a month as input and return a tuple containing a str and series.
    The str declares the most popular game title of them all, whilst the series
    shows the popularity for each game title present.
    """
    # This function is assumed to return a DataFrame with a 'Rental End Date' column
    data = get_dataframe_for_title_popularity()
    
    # Convert 'Rental End Date' to datetime if it's not already
    data['Rental End Date'] = pd.to_datetime(data['Rental End Date'], format='%d-%m-%Y')
    
    # Extract the month from 'Rental End Date'
    data['Rental End Month'] = data['Rental End Date'].dt.month
    
    # Filter the data for rows where the month is October (10)
    october_data = data[data['Rental End Month'] == month]
    
    
    # Get the value counts in descending order
    title_counts = october_data['Title'].value_counts()
    title_proportions = title_counts / title_counts.sum()

    # Most common title and its count
    most_common_title = title_counts.idxmax()
    
    return(most_common_title,title_proportions)

def most_popular_genre_for_month(month):
    """
    This function determines the most popular game genres for a given month.
    It takes a month as input and return a tuple containing a str and series.
    The str declares the most popular game  genre of them all, whilst the series
    shows the popularity for each game genre present.
    """
    # This function is assumed to return a DataFrame with a 'Rental End Date' column
    data = get_dataframe_for_genre_popularity()
    
    # Convert 'Rental End Date' to datetime if it's not already
    data['Rental End Date'] = pd.to_datetime(data['Rental End Date'])
    
    # Extract the month from 'Rental End Date'
    data['Rental End Month'] = data['Rental End Date'].dt.month
    
    # Filter the data for rows where the month is October (10)
    october_data = data[data['Rental End Month'] == month]
    
    
    # Get the value counts in descending order
    genre_counts = october_data['Genre'].value_counts()
    
    genre_proportions = genre_counts / genre_counts.sum()
    # Most common title and its count
    most_common_genre = genre_counts.idxmax()
    
    return(most_common_genre,genre_proportions)

def most_popular_title_for_month_graph(month):
    """
    This function creates a graph to show the most popular game genres for a given month.
    It takes a month as input and return a graph.
    """
    month=month_to_int(month)
    # Assume this function returns a DataFrame with a 'Rental End Date' column
    data = get_dataframe_for_title_popularity()
    
    # Convert 'Rental End Date' to datetime if it's not already
    data['Rental End Date'] = pd.to_datetime(data['Rental End Date'])
    
    # Extract the month from 'Rental End Date'
    data['Rental End Month'] = data['Rental End Date'].dt.month
    
    # Filter the data for rows where the month matches
    month_data = data[data['Rental End Month'] == month]
    
    # Get the value counts in descending order
    title_counts = month_data['Title'].value_counts()
    
    # Most common title and its count
    most_common_title = title_counts.idxmax()
    
    # Create a bar chart to serve as a histogram for title frequency
    fig, ax = plt.subplots(figsize=(10, 8))
    title_counts.plot(kind='bar', ax=ax)
    
    datetime_object = datetime.strptime(str(month), "%m")
    full_month_name = datetime_object.strftime("%B")

    # Set the title and labels
    ax.set_title(f'Most Popular Game Titles for {full_month_name}')
    ax.set_xlabel('Game Title')
    ax.set_ylabel('Rental Frequency')
    
    # Rotate the x-axis labels to show them better
    plt.xticks(rotation=45, ha='right')
    
    # Adjust the padding between and around subplots
    plt.tight_layout()
    
    # Return the most common title and the figure
    return fig

def most_popular_genre_for_month_graph(month):
    
    """
    This function creates a graph to show the most popular game titles for a given month.
    It takes a month as input and return a graph.
    """
    # Assume this function returns a DataFrame with a 'Rental End Date' column
    data = get_dataframe_for_genre_popularity()
    
    # Convert 'Rental End Date' to datetime if it's not already
    data['Rental End Date'] = pd.to_datetime(data['Rental End Date'])
    
    # Extract the month from 'Rental End Date'
    data['Rental End Month'] = data['Rental End Date'].dt.month
    
    # Filter the data for rows where the month matches
    month_data = data[data['Rental End Month'] == month]
    
    # Get the value counts in descending order
    genre_counts = month_data['Genre'].value_counts()
    
    # Most common genre and its count
    most_common_genre = genre_counts.idxmax()
    
    # Convert month number to full month name
    datetime_object = datetime.strptime(str(month), "%m")
    full_month_name = datetime_object.strftime("%B")
    
    # Create a bar chart to serve as a histogram for genre frequency
    fig, ax = plt.subplots(figsize=(10, 8))
    genre_counts.plot(kind='bar', ax=ax)

    # Set the title and labels
    ax.set_title(f'Most Popular Game Genres for {full_month_name}')
    ax.set_xlabel('Game Genre')
    ax.set_ylabel('Rental Frequency')
    
    # Rotate the x-axis labels to show them better
    plt.xticks(rotation=45, ha='right')
    
    # Adjust the padding between and around subplots
    plt.tight_layout()
    
    # Return the most common genre and the figure
    return fig

def games_to_purchase(total_budget,popularity):
    """
    Allocates a specified total budget across game genres or titles based on their popularity.
    Take input paramaters in the form of a budget and a series objects.
    It outputs out a series object which is a proportion.
    """
    popularity = pd.to_numeric(popularity, errors='coerce')
    budget_allocation = popularity * int(total_budget)
    return(budget_allocation)

def check_purchase_costs_for_game(title):
    """
    Obtains cost for certain game titles for different platforms.
    """
    connection_to_sql_database=sqlite3.connect('RentalCompany.db')
    cursor=connection_to_sql_database.cursor()
    query="""SELECT Platform,"Purchase Price" FROM 'Game Catalogue' AS GC WHERE GC.'Title' =? """
    cursor.execute(query, (title,))
    costs=cursor.fetchall()
    connection_to_sql_database.close()
    return(costs)

def games_to_buy(total_budget,month_of_choice):
    """
    Determines the number of copies of popular games to buy within a given budget 
    for a specified month. It does this by first determining the allocation of the 
    total budget across highly demanded games based on their popularity and then calculates 
    the average cost of each game across different platforms to estimate the 
    number of copies that can be purchased."""
    most_popular_titles = most_popular_title_for_month(month_to_int(month_of_choice))[1]
    games_budget_allocation = games_to_purchase(total_budget, most_popular_titles)
    
    # Function to calculate the average platform cost for a game
    def calculate_average_cost(game_title):
        platform_costs = check_purchase_costs_for_game(game_title)
        if platform_costs:
            total_cost = sum(cost for _, cost in platform_costs)
            return total_cost / len(platform_costs)
        else:
            return 0  # Return 0 if there are no platforms to avoid division by zero
    
    # Process each popular game
    list_of_popular_games = list(games_budget_allocation.index)
    messages_for_each_game=[]
    for index, game in enumerate(list_of_popular_games):
        average_game_cost = calculate_average_cost(game)
        message_1=(f"Game: {game}")
        allocated_budget_for_game = games_budget_allocation[index]
    
        if average_game_cost > 0:
            number_of_copies_to_buy = allocated_budget_for_game / average_game_cost
            message_2=(f"Number of Copies to Buy: {number_of_copies_to_buy:.0f}")
        else:
            print("Cannot calculate the number of copies to buy due to zero cost.")
        messages_for_each_game.append([message_1,message_2])
    return(messages_for_each_game)

"""
You can test out some of the functions to see if they work by uncommenting the two below.
"""
#print(games_to_buy(10000,"October"))
#most_popular_title_for_month_graph("October")