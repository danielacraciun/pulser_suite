authorization_base_url = 'https://www.fitbit.com/oauth2/authorize'
token_url = 'https://api.fitbit.com/oauth2/token'
base_url = 'https://api.fitbit.com/'
FITBIT_URL = "https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1sec/time/{}:00/{}:59.json"

activity_level_mapper = {
    1: "Low (sitting, resting etc.)",
    2: "Medium (walking etc.)",
    3: "High (running, etc.)"
}

hr_mapper = {
    0: "No recent data",
    1: "Good",
    2: "Abnormal"
}