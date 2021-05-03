"""Maintaining rental bikes data"""
#author Muntaqa Mahmood

import copy
import math
from typing import List, TextIO

from project2_constants import (ID, NAME, LATITUDE, LONGITUDE, CAPACITY,
                       BIKES_AVAILABLE, DOCKS_AVAILABLE, IS_RENTING,
                       IS_RETURNING, NO_KIOSK_LABEL, EARTH_RADIUS,
                       SOUTH, NORTH, EAST, WEST, DIRECTIONS)

#docstring examples(test cases)
SAMPLE_STATIONS = [
    [7090, 'Danforth Ave / Lamb Ave',
     43.681991, -79.329455, 15, 4, 10, True, True],
    [7486, 'Gerrard St E / Ted Reeve Dr',
     43.684261, -79.299332, 22, 5, 17, False, False],
    [7571, 'Highfield Rd / Gerrard St E - SMART',
     43.671685, -79.325176, 19, 14, 5, True, True]]
HANDOUT_STATIONS = [
    [7000, 'Ft. York / Capreol Crt.',
     43.639832, -79.395954, 31, 20, 11, True, True],
    [7001, 'Lower Jarvis St / The Esplanade',
     43.647992, -79.370907, 15, 5, 10, True, True]]
FAKE_STATIONS = [
    [1000, 'Street Ave / Road Ave',
     43.0, -79.3, 20, 0, 20, True, True],
    [1001, 'Street Ave / Road Ave',
     43.0, -79.4, 20, 20, 0, True, True],
    [1002, 'Street Ave / Road Ave - SMART',
     43.1, -79.3, 20, 20, 0, True, True],
    [1003, 'Street Ave / Road Ave',
     42.9, -79.3, 20, 10, 10, True, True]]

# Used in docstring examples to avoid using == with floats.
EPSILON = 0.01

def is_number(value: str) -> bool:
    """Return True if and only if value represents a decimal number.

    >>> is_number('csca108')
    False
    >>> is_number('  098 ')
    True
    >>> is_number('+3.14159')
    True
    """
    return value.strip().lstrip('-+').replace('.', '', 1).isnumeric()


def get_distance(lat1: float, lon1: float,
                 lat2: float, lon2: float) -> float:
    """Return the distance in kilometers between the two locations defined
    by (lat1, lon1) and (lat2, lon2), rounded to the nearest metre.

    >>> answer = get_distance(43.659777, -79.397383, 43.657129, -79.399439)
    >>> abs(answer - 0.338) < EPSILON
    True
    >>> answer = get_distance(43.67, -79.37, 55.15, -118.8)
    >>> abs(answer - 3072.872) < EPSILON
    True
    """

    # This function uses the haversine function to find the distance
    # between two locations. Based on code at goo.gl/JrPG4j
    lon1, lat1, lon2, lat2 = (math.radians(lon1), math.radians(lat1),
                              math.radians(lon2), math.radians(lat2))
    lon_diff, lat_diff = lon2 - lon1, lat2 - lat1

    a_value = (math.sin(lat_diff / 2) ** 2 +
               math.cos(lat1) * math.cos(lat2) * math.sin(lon_diff / 2) ** 2)
    c_value = 2 * math.asin(math.sqrt(a_value))

    return round(c_value * EARTH_RADIUS, 3)


def csv_to_list(csv_file: TextIO) -> List[List[str]]:
    """Return the contents of the open CSV file csv_file as a list of
    lists, where each inner list contains the values from one line of
    csv_file.

    Docstring examples not given since results depend on data to be
    input.
    """

    csv_file.readline()  # read and discard header

    data = []
    for line in csv_file:
        data.append(line.strip().split(','))

    return data

# END HELPER FUNCTIONS

def clean_data(data: List[List[str]]) -> None:
    """Replace each string in all sublists of data as follows: replace
    with
    - an int iff it represents a whole number,
    - a float iff it represents a number that is not a whole number,
    - True iff it is 'True' (case-insensitive),
    - False iff it is 'False' (case-insensitive),
    - None iff it is 'null' or the empty string.

    >>> data = [['abc', '123', '45.6', 'true', 'False']]
    >>> clean_data(data)
    >>> data
    [['abc', 123, 45.6, True, False]]
    >>> data = [['ab2'], ['-123'], ['FALSE', '3.2'], ['3.0', '+4', '-5.0']]
    >>> clean_data(data)
    >>> data
    [['ab2'], [-123], [False, 3.2], [3, 4, -5]]
    """

    for obj in data:
        i = 0

        for var in obj:
            if is_number(var):
                int_or_float(var, obj, i)

            elif var == '' or var.lower() == 'null':
                obj.pop(i)
                obj.insert(i, None)

            else:
                form_boolean(var, obj, i)
            i = i + 1

################## 2 HELPER FUNCTIONS used in "clean_data" ###################


def form_boolean(value: str, sublist: list, index: int) -> None:
    """This helper function takes the value of a string and changes
    it to a boolean.

    >>> boolean_list = ['true', 'false']
    >>> str_bool = boolean_list[0]
    >>> form_boolean(str_bool, boolean_list, 0)
    >>> str_bool = boolean_list[0]
    >>> type(str_bool)
    <class 'bool'>

    >>> bool_list = ['abc', 'False', 'hi']
    >>> bool_str = bool_list[1]
    >>> form_boolean(bool_str, bool_list, 1)
    >>> bool_str = bool_list[1]
    >>> type(bool_str)
    <class 'bool'>
    """

    if value.casefold() == 'true':
        sublist.pop(index)
        sublist.insert(index, True)

    elif value.casefold() == 'false':
        sublist.pop(index)
        sublist.insert(index, False)

#################### 1st HELPER FUNCTION for "clean_data" ####################

def int_or_float(value: str, sublist: list, index: int) -> None:
    """This function will take an integer and changes it to an int if it is an
    integer or takes a float and changes it to a float if it is a float.

    >>> election = ['167', 'elected']
    >>> votes = election[0]
    >>> int_or_float(votes, election, 0)
    >>> votes = election[0]
    >>> type(votes)
    <class 'int'>

    >>> speed = ['99.98765']
    >>> measure = speed[0]
    >>> int_or_float(measure, speed, 0)
    >>> measure = speed[0]
    >>> type(measure)
    <class 'float'>
    """

    if float(value) % 1 == 0:
        sublist.pop(index)
        sublist.insert(index, int(float(value)))

    else:
        sublist.pop(index)
        sublist.insert(index, float(value))

def has_kiosk(station: 'Station') -> bool:
    """Return True if and only if the given station has a kiosk.

    >>> has_kiosk(SAMPLE_STATIONS[0])
    True
    >>> has_kiosk(SAMPLE_STATIONS[2])
    False
    """

    return not NO_KIOSK_LABEL in station[NAME]


def get_station_info(station_id: int, stations: List['Station']) -> list:
    """Return a list containing the following information from stations
    about the station with id number station_id:

        - station name (str)
        - number of bikes available (int)
        - number of docks available (int)
        - whether or not the station has a kiosk (bool)
    (in this order)

    If station_id is not in stations, return an empty list.

    Precondition: stations has at most one station with id station_id.

    >>> get_station_info(7090, SAMPLE_STATIONS)
    ['Danforth Ave / Lamb Ave', 4, 10, True]
    >>> get_station_info(7571, SAMPLE_STATIONS)
    ['Highfield Rd / Gerrard St E - SMART', 14, 5, False]
    """

    stn = get_station(station_id, stations)

    if station_id == stn[0]:
        stn_information = [stn[NAME], stn[BIKES_AVAILABLE],
                           stn[DOCKS_AVAILABLE], has_kiosk(stn)]

    else:
        stn_information = []

    return stn_information

def get_total(index: int, stations: List['Station']) -> int:
    """Return the sum of the column in stations given by index. Return 0
    if stations is empty.

    Preconditions: index is a valid index into each station in stations.
                   The items in stations at the position that index
                    refers to are ints.

    >>> get_total(BIKES_AVAILABLE, SAMPLE_STATIONS)
    23
    >>> get_total(DOCKS_AVAILABLE, SAMPLE_STATIONS)
    32
    """

    total = 0

    if len(stations) > 0:
        for station in stations:
            total += station[index]

    return total


def get_station_with_max_bikes(stations: List['Station']) -> int:
    """Return the station id of the station that has the most bikes
    available.  If there is a tie for the most available, return the
    station id that appears first in stations.

    Preconditions: len(stations) > 0

    >>> get_station_with_max_bikes(SAMPLE_STATIONS)
    7571
    >>> get_station_with_max_bikes(HANDOUT_STATIONS)
    7000
    """

    most_bikes = 0
    stations_id = -1

    for station in stations:
        if station[BIKES_AVAILABLE] > most_bikes:
            most_bikes = station[BIKES_AVAILABLE]
            stations_id = station[ID]

    return stations_id



def get_stations_with_n_docks(num: int, stations: List['Station']) -> List[int]:
    """Return a list containing the station ids for the stations in
    stations that have at least num docks available, in the same order
    as they appear in stations.

    Precondition: num >= 0

    >>> get_stations_with_n_docks(2, SAMPLE_STATIONS)
    [7090, 7486, 7571]
    >>> get_stations_with_n_docks(12, SAMPLE_STATIONS)
    [7486]
    """

    num_docks_list = []

    for station in stations:
        if station[DOCKS_AVAILABLE] >= num:
            num_docks_list.append(station[ID])

    return num_docks_list


def get_direction(start_id: int, end_id: int, stations: List['Station']) -> str:
    """Return the direction to travel to get from station start_id to
    station end_id according to data in stations. Possible directions
    are defined by DIRECTIONS.

    Preconditions: start_id and end_id appears in stations.
                   start_id and end_id are ids of stations at different
                   locations.

    >>> get_direction(7486, 7090, SAMPLE_STATIONS)
    'SOUTHWEST'
    >>> get_direction(1000, 1002, FAKE_STATIONS)
    'NORTH'
    """

    directions = ''
    starting_station = get_station(start_id, stations)
    ending_station = get_station(end_id, stations)

    if starting_station[LATITUDE] < ending_station[LATITUDE]:
        directions += NORTH
    elif starting_station[LATITUDE] > ending_station[LATITUDE]:
        directions += SOUTH

    if starting_station[LONGITUDE] > ending_station[LONGITUDE]:
        directions += WEST
    elif starting_station[LONGITUDE] < ending_station[LONGITUDE]:
        directions += EAST

    return directions


def get_nearest_station(lat: float, lon: float, with_kiosk: bool,
                        stations: List['Station']) -> int:
    """Return the id of the station from stations that is nearest to the
    location given by lat and lon.  If with_kiosk is True, return the
    id of the closest station with a kiosk.

    In the case of a tie, return the ID of the first station in
    stations with that distance.

    Preconditions: len(stations) > 1

    If with_kiosk, then there is at least one station in stations with a kiosk.

    >>> get_nearest_station(43.671134, -79.325164, False, SAMPLE_STATIONS)
    7571
    >>> get_nearest_station(43.674312, -79.299221, True, SAMPLE_STATIONS)
    7486
    """

    min_distance = pow(10, 10)

    if with_kiosk:
        min_station_id = get_nearest_kiosk_station(lat, lon,
                                                   stations, min_distance)

    else:
        for station in stations:
            distance = get_distance(lat, lon, station[LATITUDE],
                                    station[LONGITUDE])

            if distance < min_distance:
                min_distance = distance
                min_station_id = station[ID]

    return min_station_id

def get_nearest_kiosk_station(lat1: float, lon1: float,
                              stations: List['Station'],
                              min_distance: int) -> int:
    """Returns nearest kiosk_station and is a helper function for the
    function "get_nearest_station".

    >>> get_nearest_kiosk_station(43.674312, -79.299221,SAMPLE_STATIONS, 100000)
    7486
    """

    nearest_kiosk_stations = []

    for station in stations:
        if has_kiosk(station):
            nearest_kiosk_stations.append(station)

    for nearest_kiosk_station in nearest_kiosk_stations:
        distance = get_distance(lat1, lon1, nearest_kiosk_station[LATITUDE],
                                nearest_kiosk_station[LONGITUDE])

        if distance < min_distance:
            min_distance = distance
            min_station_id = nearest_kiosk_station[ID]

    return min_station_id

############### HELPER FUNCTION for "get_nearest_station" ################

def rent_bike(station_id: int, stations: List['Station']) -> bool:
    """Update the available bike count and the docks available count for
    the station in stations with id station_id as if a single bike was
    removed, leaving an additional dock available. Return True if and
    only if the rental was successful, i.e. there was at least one
    bike available and the station is renting.

    Precondition: station_id appears in stations.

    >>> stations = copy.deepcopy(SAMPLE_STATIONS)
    >>> rent_bike(7090, stations)
    True
    >>> stations[0][BIKES_AVAILABLE]
    3
    >>> stations[0][DOCKS_AVAILABLE]
    11
    >>> rent_bike(7486, stations)
    False
    >>> stations[1][BIKES_AVAILABLE]
    5
    >>> stations[1][DOCKS_AVAILABLE]
    17
    """

    stn = get_station(station_id, stations)

    if stn[IS_RENTING] and (stn[BIKES_AVAILABLE] >= 1):
        stn[BIKES_AVAILABLE] -= 1
        stn[DOCKS_AVAILABLE] += 1
        return True

    return False

def return_bike(station_id: int, stations: List['Station']) -> bool:
    """Update the available bike count and the docks available count for
    station in stations with id station_id as if a single bike was
    added, making an additional dock unavailable. Return True if and
    only if the return was successful, i.e. there was at least one
    dock available and the station is allowing returns.

    Precondition: station_id appears in stations.

    >>> stations = copy.deepcopy(SAMPLE_STATIONS)
    >>> return_bike(7090, stations)
    True
    >>> stations[0][BIKES_AVAILABLE]
    5
    >>> stations[0][DOCKS_AVAILABLE]
    9
    >>> return_bike(7486, stations)
    False
    >>> stations[1][BIKES_AVAILABLE]
    5
    >>> stations[1][DOCKS_AVAILABLE]
    17
    """

    stn = get_station(station_id, stations)

    if stn[IS_RENTING] and (stn[DOCKS_AVAILABLE] >= 1):
        stn[BIKES_AVAILABLE] += 1
        stn[DOCKS_AVAILABLE] -= 1
        return True

    return False


def balance_all_bikes(stations: List['Station']) -> int:
    """Return the difference between the number of bikes rented and the
    number of bikes returned as a result of the following balancing:

    Calculate the percentage of bikes available across all stations
    and evenly distribute the bikes so that each station has as close
    to the overall percentage of bikes available as possible. Remove a
    bike from a station if and only if the station is renting and
    there is a bike available to rent, and return a bike if and only
    if the station is allowing returns and there is a dock available.

    >>> stations = copy.deepcopy(SAMPLE_STATIONS)
    >>> balance_all_bikes(stations)
    4
    >>> stations == [
    ...  [7090, 'Danforth Ave / Lamb Ave',
    ...   43.681991, -79.329455, 15, 6, 8, True, True],    # return 2
    ...  [7486, 'Gerrard St E / Ted Reeve Dr',
    ...   43.684261, -79.299332, 22, 5, 17, False, False], # no change
    ...  [7571, 'Highfield Rd / Gerrard St E - SMART',
    ...   43.671685, -79.325176, 19, 8, 11, True, True]]   # rent 6
    True
    >>> stations = copy.deepcopy(HANDOUT_STATIONS)
    >>> balance_all_bikes(stations)
    0
    >>> stations == [
    ...  [7000, 'Ft. York / Capreol Crt.', 43.639832, -79.395954, 31, 17,
    ...   14, True, True],
    ...  [7001, 'Lower Jarvis St / The Esplanade', 43.647992, -79.370907,
    ...   15, 8, 7, True, True]]
    True
    """

    target_percent = calculate_target_percentage(stations)
    bike_returning = 0
    bike_renting = 0

    for station in stations:
        target_bikes = round(target_percent * station[CAPACITY])

        while (station[BIKES_AVAILABLE] < target_bikes
               and return_bike(station[ID], stations)):
            bike_returning += 1

        while (station[BIKES_AVAILABLE] > target_bikes
               and rent_bike(station[ID], stations)):
            bike_renting += 1

    return bike_renting - bike_returning


def calculate_target_percentage(stations: List['Station']) -> float:
    """Return the target percentage of available bikes at each station
    from stations, for the purpose of re-balancing.

    >>> target_percent = calculate_target_percentage(FAKE_STATIONS)
    >>> abs(target_percent - 0.625) < EPSILON
    True
    """

    max_bikes = get_total(BIKES_AVAILABLE, stations)
    max_capacity = get_total(CAPACITY, stations)

    final_avg = round(max_bikes / max_capacity, 2)

    return final_avg

def get_station(station_id: int, stations: List['Station']) -> 'Station':
    """Return the stations from stations with id station_id. If there is
    no such station, return the empty list.

    >>> station = [7486, 'Gerrard St E / Ted Reeve Dr', 43.684261, -79.299332,
    ...            22, 5, 17, False, False]
    >>> get_station(7486, SAMPLE_STATIONS) == station
    True
    """

    i = 0

    while station_id != stations[i][ID]:
        i += 1

    return stations[i]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
