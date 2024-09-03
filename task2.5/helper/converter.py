import datetime
import bisect

def convertToDatetime(epoch_time: int, timezone: int) -> str:
    dt = datetime.datetime.fromtimestamp(epoch_time, datetime.timezone(datetime.timedelta(hours=timezone)))
    seconds_into_day = dt.hour * 3600 + dt.minute * 60 + dt.second
    return seconds_into_day

def smallest_larger_than_x(weights, time_start):
    time_list = [weight[1] for weight in weights]
    
    # Find the insertion point for time_start in the list of times
    index = bisect.bisect_right(time_list, time_start)
    
    # If the index is equal to the length of the list, there is no element larger than time_start
    if index == len(weights):
        return None
    
    # Return the tuple at the insertion point
    return weights[index]

print(convertToDatetime(1725353142, 7)) # 0