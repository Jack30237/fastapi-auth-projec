def extract_features(df):
    # 計算同 IP 失敗次數
    ip_fail_count = df[df['status']=="FAIL"].groupby('ip').size()
    df['ip_fail_count'] = df['ip'].map(ip_fail_count).fillna(0)
    # 計算同帳號失敗次數
    user_fail_count = df[df['status']=="FAIL"].groupby('user').size()
    df['user_fail_count'] = df['user'].map(user_fail_count).fillna(0)
    # 可加更多特徵
    return df
