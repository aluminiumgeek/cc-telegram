import os


def main(bot, *args, **kwargs):
    """
    uptime
    Show system uptime
    """

    try:
        f = open("/proc/uptime")
        contents = f.read().split()
    except:
        return "Cannot open uptime file: /proc/uptime"
    finally:
        f.close()

    total_seconds = float(contents[0])

    # Helper vars:
    MINUTE = 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24

    # Get the days, hours, etc:
    days = int(total_seconds / DAY)
    hours = int((total_seconds % DAY ) / HOUR)
    minutes = int((total_seconds % HOUR ) / MINUTE)
    seconds = int(total_seconds % MINUTE)

    # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
    result = ''
    if days > 0:
        result += '{} {}, '.format(days, days == 1 and "day" or "days")
    if result or hours > 0:
        result += '{} {}, '.format(hours, hours == 1 and "hour" or "hours")
    if result or minutes > 0:
        result += '{} {}, '.format(minutes, minutes == 1 and "minute" or "minutes")
    result += '{} {}'.format(seconds, seconds == 1 and "second" or "seconds")

    return result
