# Zadanie 1 - Parkujeme

# Meno: Roman Dzhulai
# Spolupráca: Varvara Cherniavska
# Použité zdroje: 
# Čas potrebný na vypracovanie: 

import csv
import math
from collections import Counter

def load_parking_records(file_path):  # 0.75b
    """
    Loads and returns parking records.
     - file_path: path to csv file with parking records
    Returns: list of tuples with number late, parking start hour and minute
             and parking end hour and minute.
    """
    with open(file_path, 'r', encoding="utf-8") as csvfile:
        fieldnames = ['license_plate', 'start_hour', 'start_minute',           
            'end_hour', 'end_minute']
        csv_reader = csv.DictReader(csvfile, fieldnames=fieldnames)

        parking_records = list()

        for row in csv_reader:
            parking_records.append(
                (row['license_plate'], int(row['start_hour']),
                int(row['start_minute']), int(row['end_hour']),
                int(row['end_minute'])))
        
    return parking_records

def load_prices(file_path):  # 0.75b
    """
    Loads and returns parking pricing.
     - file_path: path to txt file with prices
    Returns: dictionary with prices for 30m, 1h, 3h, 6h, 1d, h+
    """
    parking_pricing = dict()
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            listedline = line.strip().split(sep=": ", maxsplit=1)
            parking_pricing[listedline[0]] = float(listedline[1]) 
    return parking_pricing


def calculate_parking_time(start_h, start_m, end_h, end_m):  # 0.5b
    """
    Calculates and returns the duration of parking in minutes
    based on start and end time.
    """
    parking_time = 60 - start_m + 60 * (end_h - start_h - 1) + end_m
    return parking_time


def get_parking_fee(time_in_minutes, prices):  # 1b
    """
    Calculates and returns the price of parking for a given amount
    of time based on pricing.
    """
    hours = time_in_minutes // 60
    minutes = time_in_minutes % 60
    
    parking_fee = 0.0
    
    if(time_in_minutes < 15): 
        pass
    
    elif(time_in_minutes < 30):
        parking_fee = prices["30m"] 
        
    elif(hours == 1 and minutes == 0):
        parking_fee = prices["1h"]
        
    elif(hours < 3):    
        calc_fee = prices["1h"] + (hours) * prices["h+"]
        parking_fee = prices["3h"] if calc_fee > prices["3h"] else calc_fee 
        
    elif(hours == 3 and minutes == 0):
        parking_fee = prices["3h"]
        
    elif(hours < 6):
        calc_fee = prices["3h"] + (hours - 2) * prices["h+"]
        parking_fee = prices["6h"] if calc_fee > prices["6h"] else calc_fee
    
    elif(hours == 6 and minutes == 0):
        parking_fee = prices["6h"]
    
    elif(hours < 24):
        calc_fee = prices["6h"] + (hours - 5) * prices["h+"]
        parking_fee = prices["1d"] if calc_fee > prices["1d"] else calc_fee
    
    elif(hours == 24 and minutes == 0):
        parking_fee = prices["1d"]

    else:
        parking_fee = prices["1d"] + (hours - 23) * prices["h+"]
    
    return parking_fee

def calculate_average_parking_fee(records, prices):  # 0.5b
    """
    Calculates the average amount paid for parking during the day.
    """
    parking_fee = 0.0
        
    for __, sthour, stmin, enhour, enmin in records:
        parking_time = calculate_parking_time(sthour, stmin, enhour, enmin)
        parking_fee += get_parking_fee(parking_time, prices)
    
    average_fee = parking_fee / len(records)
    
    return average_fee


def calculate_average_parking_time(records):  # 0.5b
    """
    Calculates the average length of parking for the day.
    """
    parking_time = 0.0
    
    for __, sthour, stmin, enhour, enmin in records:
        parking_time += calculate_parking_time(sthour, stmin, enhour, enmin)
    
    average_time = parking_time / len(records)
    
    return average_time


def calculate_average_stays(records):  # 0.5b
    """
    Calculates the average number a car was parked during the day.
    """
    license_plates = [a[0] for a in records]
    
    average_stays = float(len(license_plates) / len(set(license_plates)))
    
    return average_stays


def get_most_common_region(records):  # 1b
    """
    Returns the code of the most common region of cars parked during the day.
    """
    c = Counter([x[0][:2] for x in records])
    
    return c.most_common(1)[0][0]


def get_busiest_hour(records):  # 0.5b
    """
    Returns the hour when the most cars were parked at the parking lot.
    It considers cars that were parked before or at the given hour
    and stayed at the parking lot until or after the given hour.
    """
    num_parked = [0] * 24
    
    for __, sthour, __, enhour, __ in records:
        for i in range(sthour - 1, enhour):
            num_parked[i] += 1
            
    max_parked = max(num_parked)
    
    for i, num in enumerate(num_parked):
        if max_parked == num:
            return i + 1


def get_total_time_in_minutes(hours: int, minutes: int) -> int:
    return hours*60+minutes
    

def get_max_number_of_cars(records):  # 2b
    """
    Returns the highest number of cars parked at the parking lot in a given
    minute.
    """
    start_minutes = [get_total_time_in_minutes(x[1], x[2]) for x in records]
    end_minutes = [get_total_time_in_minutes(x[3], x[4]) for x in records]
    
    open_minute = start_minutes[0] // 60 * 60
    close_minute = math.ceil(max(end_minutes) / 60) * 60
    
    parked_cars_in_minute = [0] * (close_minute - open_minute)

    for s, e in list(zip(start_minutes, end_minutes)):
        for i in range(s - open_minute, e - open_minute):
            parked_cars_in_minute[i] += 1
        
    max_number_of_cars = max(parked_cars_in_minute)
        
    return max_number_of_cars, parked_cars_in_minute


def optimize_hourly_fee(records, prices):  # 2b
    """
    Returns the fee of additional hours that will maximize income for
    the parking lot.
    """
    custom_prices = dict(prices)
    
    total_fees = list()
    
    possible_prices = [x/10 for x in range(int(prices["30m"]*10), 
                                           int(prices["1h"]*10))]
    
    for p in possible_prices:
        custom_prices["h+"] = p
        parking_fee = 0.0
        for __, sthour, stmin, enhour, enmin in records:
            parking_time = calculate_parking_time(sthour, stmin, enhour, enmin)
            parking_fee += get_parking_fee(parking_time, custom_prices)  
        total_fees.append((p , parking_fee))
    
        
    return max(total_fees, key=lambda x: x[1])[0]
