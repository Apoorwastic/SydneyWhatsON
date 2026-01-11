user_preferences = {}

def save_preference(user_id, preference):
    user_preferences[user_id] = preference

def get_preference(user_id):
    return user_preferences.get(user_id)
