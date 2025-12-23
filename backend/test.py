from parser import parse_log
from features import extract_features
from detector import detect_anomalies

df = parse_log()
df = extract_features(df)
df = detect_anomalies(df)
print(df)
