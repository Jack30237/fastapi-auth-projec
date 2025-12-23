import pandas as pd
import re

def parse_log(file_path="./logs/auth.log"):
    data = []
    with open(file_path) as f:
        for line in f:
            match = re.match(r'(\S+ \S+) (\S+) user=(\S+) ip=(\S+)', line)
            if match:
                timestamp, status, user, ip = match.groups()
                data.append({
                    "timestamp": timestamp,
                    "status": status,
                    "user": user,
                    "ip": ip
                })
    df = pd.DataFrame(data)
    return df

