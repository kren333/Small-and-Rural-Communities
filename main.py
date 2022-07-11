import pandas as pd
import math
import mysql.connector
from matplotlib import pyplot as plt
from mysql.connector import Error
import numpy as np
import csv


# testing a function to create array of any variable for a given municipality


def get_var_mun(connection, id, var):
    getData = """SELECT CLB.`2007`.`Municipality ID`, CLB.`2007`.""" + var + """, CLB.`2008`.""" + var + """, CLB.`2009`.""" + var + """, CLB.`2010`.""" + var + """, CLB.`2011`.""" + var + """, CLB.`2012`.""" + var + """, CLB.`2013`.""" + var + """, CLB.`2014`.""" + var + """, CLB.`2015`.""" + var + """, CLB.`2016`.""" + var + """, CLB.`2017`.""" + var + """, CLB.`2018`.""" + var + """, CLB.`2019`.""" + var + """FROM CLB.`2007` 
                    JOIN CLB.`2008` on CLB.`2007`.`Municipality ID` = CLB.`2008`.`Municipality ID`
                    JOIN CLB.`2009` on CLB.`2008`.`Municipality ID` = CLB.`2009`.`Municipality ID`
                    JOIN CLB.`2010` on CLB.`2009`.`Municipality ID` = CLB.`2010`.`Municipality ID`
                    JOIN CLB.`2011` on CLB.`2010`.`Municipality ID` = CLB.`2011`.`Municipality ID`
                    JOIN CLB.`2012` on CLB.`2011`.`Municipality ID` = CLB.`2012`.`Municipality ID`
                    JOIN CLB.`2013` on CLB.`2012`.`Municipality ID` = CLB.`2013`.`Municipality ID`
                    JOIN CLB.`2014` on CLB.`2013`.`Municipality ID` = CLB.`2014`.`Municipality ID`
                    JOIN CLB.`2015` on CLB.`2014`.`Municipality ID` = CLB.`2015`.`Municipality ID`
                    join CLB.`2016` on CLB.`2015`.`Municipality ID` = CLB.`2016`.`Municipality ID`
                    join CLB.`2017` on CLB.`2016`.`Municipality ID` = CLB.`2017`.`Municipality ID`
                    join CLB.`2018` on CLB.`2017`.`Municipality ID` = CLB.`2018`.`Municipality ID`
                    join CLB.`2019` on CLB.`2018`.`Municipality ID` = CLB.`2019`.`Municipality ID`
                    where CLB.`2007`.`Municipality ID` = """ + id + """;"""

    results = read_query(connection, getData)

    data = []
    for result in results:
        data.append(result)

    onlyData = []
    for i in range(len(data)):
        onlyData.append(tuple(x for x in data[i] if type(x) == int))

    return onlyData


def scatter_plot(x, y):
    plt.scatter(x, y)
    plt.plot(x, y)


def id_tester(id):
    revData = get_var_mun(connection, id, "`Total Revenues`")
    dseData = get_var_mun(connection, id, "`Debt Service Expenditures`")
    dsrData = []

    if (len(revData[0]) == len(dseData[0])):
        for i in range(len(revData[0])):
            dsrData.append(dseData[0][i] / revData[0][i])

    time_coord = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

    # rev_coord = []
    # dse_coord = []
    dsr_coord = dsrData

    # for i in range(len(revData[0])):  # number years
    #     rev_coord.append(revData[0][i])
    #     dse_coord.append(dseData[0][i])
    #
    # np_rev_coord = np.array(rev_coord)
    # np_dse_coord = np.array(dse_coord)
    np_dsr_coord = np.array(dsr_coord)

    # scatter_plot(time_coord, np_rev_coord)
    # scatter_plot(time_coord, np_dse_coord)
    scatter_plot(time_coord, np_dsr_coord)

    plt.xlim(2007, 2019)
    plt.title(id)
    plt.ylabel("Value (dollars, unitless in case of debt service ratio)")
    plt.xlabel("Year")
    plt.show()


# polymorphic: plots variable for all municipalities

# get data from csv file 1986-2019

def pop_percent_change(id, name):
    init = np.genfromtxt("1986 - 2019 Municipal Financial Data.csv",delimiter=",",skip_header=1,usecols=(0,3,4,5,6,7,8,9,10,11,12,13,14,15))
    data = np.array(init)
    filtered_data = data[data[:,0] == int(id)]
    pop_data = filtered_data[:,1],filtered_data[:,(2)]

    # make the thing
    for i in range(33):
        pop_data[1][i+1] = (pop_data[1][i+1]-pop_data[1][0])/(pop_data[1][0])
    pop_data[1][0] = 0

    print(pop_data[1][33])


    plt.plot(pop_data[0], pop_data[1])
    plt.title(name)
    plt.xlabel("Year")
    plt.ylabel("Population (Percent change from base year)")
    plt.show()

def get_dsr_data(id, name):
    init = np.genfromtxt("1986 - 2019 Municipal Financial Data.csv",delimiter=",",skip_header=1,usecols=(0,3,4,5,6,7,8,9,10,11,12,13,14,15))
    data = np.array(init)
    filtered_data = data[data[:,0] == int(id)]
    dse_data = filtered_data[:,1],filtered_data[:,(13)]
    total_rev_data = filtered_data[:,1],filtered_data[:,(3)]

    # create dsr array and plot
    dsr_data = dse_data
    for i in range(33):
        if math.isnan(dse_data[1][i]) or dse_data[1][i] == 0:
            dsr_data[1][i] = 0
        else:
            dsr_data[1][i] = total_rev_data[1][i] / dse_data[1][i]

    plt.plot(dsr_data[0], dsr_data[1])
    plt.title(name)
    plt.xlabel("Year")
    plt.ylabel("Debt Service Ratio")
    plt.show()

def get_revs(id):
    init = np.genfromtxt("1986 - 2019 Municipal Financial Data.csv",delimiter=",",skip_header=1,usecols=(0,3,4,5,6,7,8,9,10,11,12,13,14,15))
    data = np.array(init)
    filtered_data = data[data[:,0] == int(id)]
    total_rev_data = filtered_data[:,1],filtered_data[:,(4)]
    print(total_rev_data)

# should plot dsr values from 1986 to present
def tester2(id):
    revData = get_var_mun(connection, id, "`Total Revenues`")
    dseData = get_var_mun(connection, id, "`Debt Service Expenditures`")
    dsrData = []

    if (len(revData[0]) == len(dseData[0])):
        for i in range(len(revData[0])):
            dsrData.append(dseData[0][i] / revData[0][i])

    time_coord = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

    # rev_coord = []
    # dse_coord = []
    dsr_coord = dsrData

    # for i in range(len(revData[0])):  # number years
    #     rev_coord.append(revData[0][i])
    #     dse_coord.append(dseData[0][i])
    #
    # np_rev_coord = np.array(rev_coord)
    # np_dse_coord = np.array(dse_coord)
    np_dsr_coord = np.array(dsr_coord)

    # scatter_plot(time_coord, np_rev_coord)
    # scatter_plot(time_coord, np_dse_coord)
    scatter_plot(time_coord, np_dsr_coord)

    plt.xlim(2007, 2019)
    plt.title(id)
    plt.ylabel("Value (dollars, unitless in case of debt service ratio)")
    plt.xlabel("Year")
    plt.show()

def get_var_all(connection, var):
    getData = """SELECT CLB.`2007`.`Municipality ID`, CLB.`2007`.""" + var + """, CLB.`2008`.""" + var + """, CLB.`2009`.""" + var + """, CLB.`2010`.""" + var + """, CLB.`2011`.""" + var + """, CLB.`2012`.""" + var + """, CLB.`2013`.""" + var + """, CLB.`2014`.""" + var + """, CLB.`2015`.""" + var + """, CLB.`2016`.""" + var + """, CLB.`2017`.""" + var + """, CLB.`2018`.""" + var + """, CLB.`2019`.""" + var + """ FROM CLB.`2007` 
                    JOIN CLB.`2008` on CLB.`2007`.`Municipality ID` = CLB.`2008`.`Municipality ID`
                    JOIN CLB.`2009` on CLB.`2008`.`Municipality ID` = CLB.`2009`.`Municipality ID`
                    JOIN CLB.`2010` on CLB.`2009`.`Municipality ID` = CLB.`2010`.`Municipality ID`
                    JOIN CLB.`2011` on CLB.`2010`.`Municipality ID` = CLB.`2011`.`Municipality ID`
                    JOIN CLB.`2012` on CLB.`2011`.`Municipality ID` = CLB.`2012`.`Municipality ID`
                    JOIN CLB.`2013` on CLB.`2012`.`Municipality ID` = CLB.`2013`.`Municipality ID`
                    JOIN CLB.`2014` on CLB.`2013`.`Municipality ID` = CLB.`2014`.`Municipality ID`
                    JOIN CLB.`2015` on CLB.`2014`.`Municipality ID` = CLB.`2015`.`Municipality ID`
                    join CLB.`2016` on CLB.`2015`.`Municipality ID` = CLB.`2016`.`Municipality ID`
                    join CLB.`2017` on CLB.`2016`.`Municipality ID` = CLB.`2017`.`Municipality ID`
                    join CLB.`2018` on CLB.`2017`.`Municipality ID` = CLB.`2018`.`Municipality ID`
                    join CLB.`2019` on CLB.`2018`.`Municipality ID` = CLB.`2019`.`Municipality ID`;"""
    results = read_query(connection, getData)
    data = []
    for result in results:
        data.append(result)
    return data

def scatter_all(array):
    time_coord = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    for i in range(len(array)):  # should be number of ids
        coord = []
        for j in range(len(time_coord)):  # number years
            coord.append(array[i][j])
        plt.scatter(time_coord, coord)
        plt.plot(time_coord, coord)

def all_tester(var):
    all_rev_data = get_var_all(connection, var)

    only_rev_values = []
    for i in range(len(all_rev_data)):
        only_rev_values.append(tuple(x for x in all_rev_data[i] if type(x) == int))

    scatter_all(only_rev_values)
    plt.show()


# all-csv functions

def get_var_by_year_all(connection, year, var):
    getData = """SELECT * FROM CLB.allminusdse WHERE `Reporting Year` = """ + year + """;"""
    results = read_query(connection, getData)
    data = []
    for result in results:
        data.append(result)
    return data


# server functions

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

connection = create_db_connection("localhost", "root", "Mason703450!-cmu2025!", "CLB")

# create/run queries
# id_tester("20963")
# get_dsr_data("20393", "Braddock Debt Service Coverage Ratio")
# get_dsr_data("20902", "Duquesne Debt Service Coverage Ratio")
# get_dsr_data("631202", "Monongahela Debt Service Coverage Ratio")
# get_dsr_data("651413", "Scottdale Debt Service Coverage Ratio")
# get_dsr_data("22403", "Oakmont Debt Service Coverage Ratio")

# pop_percent_change("20393", "Braddock")
# pop_percent_change("20902", "Duquesne")
# pop_percent_change("631202", "Monongahela")
# pop_percent_change("651413", "Scottdale")
# pop_percent_change("22403", "Oakmont")

get_revs("631202")
