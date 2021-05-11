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
    if control_dist_km <= 200:
        # min speed = 15
        # max speed = 34
        hr, mins = divmod((control_dist_km / 34), 1) # separate int and decimal
        mins = round(mins * 60)
    elif control_dist_km <= 400:
        # min speed = 15
        # max speed = 32
        hr, mins = divmod((control_dist_km / 32), 1)
        mins = round(mins * 60)
    elif control_dist_km <= 600:
        # min speed = 15
        # max speed = 30
        hr, mins = divmod((control_dist_km / 30), 1)
        mins = round(mins * 60)
    elif control_dist_km <= 1000:
        # min speed = 11.428
        # max speed = 28
        hr, mins = divmod((control_dist_km / 28), 1)
        mins = round(mins * 60)
    else:
        # min speed = 13.333
        # max speed = 26
        hr, mins = divmod((control_dist_km / 26), 1)
        mins = round(mins * 60)
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
    if control_dist_km <= 600:
        # min speed = 15
        # max speed = 30
        hr, mins = divmod((control_dist_km / 15), 1)
        mins = round(mins * 60)
    elif control_dist_km <= 1000:
        # min speed = 11.428
        # max speed = 28
        hr, mins = divmod((control_dist_km / 11.428), 1)
        mins = round(mins * 60)
    else:
        # min speed = 13.333
        # max speed = 26
        hr, mins = divmod((control_dist_km / 13.333), 1)
        mins = round(mins * 60)
    close_time = brevet_start_time.shift(hours=hr, minutes=mins)
    return close_time
