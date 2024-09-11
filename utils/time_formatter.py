def convert_to_iso(timestamp):
    year = timestamp[:4]
    month = timestamp[4:6]
    day = timestamp[6:8]
    hour = timestamp[8:10]
    minute = timestamp[10:12]
    second = timestamp[12:14]
    
    return f"{year}-{month}-{day}T{hour}:{minute}:{second}"