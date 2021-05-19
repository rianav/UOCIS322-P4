"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#
def get_hrs_mins(control_dist_km, speed):
    """
    Helper function to get hours and minutes for a
    specified max or min speed
    """
    hrs, mins = divmod((control_dist_km / speed), 1)
    mins = round(mins * 60)
    return hrs, mins

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    if control_dist_km == 0:
        # first control opens at start time
        return brevet_start_time

    hr200, mins200 = get_hrs_mins(200, 34)
    hr400, mins400 = get_hrs_mins(200, 32)
    hr600, mins600 = get_hrs_mins(200, 30)
    hr1000, mins1000 = get_hrs_mins(200, 28)
    if control_dist_km <= 200:
        # max speed = 34
        hr, mins = get_hrs_mins(control_dist_km, 34)
    elif control_dist_km <= 400:
        # max speed = 32
        hr, mins = get_hrs_mins(control_dist_km - 200, 32)
        hr += hr200
        mins += mins200
    elif control_dist_km <= 600:
        # max speed = 30
        hr, mins = get_hrs_mins(control_dist_km - 400, 30)
        hr += hr400 + hr200
        mins += mins400 + mins200
    elif control_dist_km <= 1000:
        # max speed = 28
        hr, mins = get_hrs_mins(control_dist_km - 600, 28)
        hr += hr600 + hr400 + hr200
        mins += mins600 + mins400 + mins200
    else:
        # max speed = 26
        hr, mins = get_hrs_mins(control_dist_km - 1000, 26)
        hr += hr1000 + hr600 + hr400 + hr200
        mins += hr1000 + mins600 + mins400 + mins200

    open_time = brevet_start_time.shift(hours=hr, minutes=mins)

    return open_time


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    if control_dist_km == 0:
        return brevet_start_time.shift(hours=1)
    if control_dist_km >= brevet_dist_km:
        if brevet_dist_km == 200:
            return brevet_start_time.shift(hours=13, minutes=30)
        elif brevet_dist_km == 300:
            return brevet_start_time.shift(hours=20)
        elif brevet_dist_km == 400:
            return brevet_start_time.shift(hours=27)
        elif brevet_dist_km == 600:
            return brevet_start_time.shift(hours=40)
        elif brevet_dist_km == 1000:
            return brevet_start_time.shift(hours=75)
    hr600, mins600 = get_hrs_mins(600, 15)
    hr1000, mins1000 = get_hrs_mins(1000, 11.428)
    if control_dist_km <= 60:
        hr, mins = get_hrs_mins(control_dist_km, 20)
        hr += 1
        return brevet_start_time.shift(hours=hr, minutes=mins)
    elif control_dist_km <= 600:
        # min speed = 15
        # max speed = 30
        hr, mins = get_hrs_mins(control_dist_km, 15)
    elif control_dist_km <= 1000:
        # min speed = 11.428
        # max speed = 28
        hr, mins = get_hrs_mins(control_dist_km - 600, 11.428)
        hr += hr600
        mins += mins600
    else:
        # min speed = 13.333
        # max speed = 26
        hr, mins = get_hrs_mins(control_dist_km - 1000, 13.333)
        hr += hr1000 + hr600
        mins += mins1000 + mins600
    close_time = brevet_start_time.shift(hours=hr, minutes=mins)
    return close_time
