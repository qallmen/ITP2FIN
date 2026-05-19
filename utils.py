from geopy.distance import geodesic

def calculate_nearest_places(user_lat, user_lon, all_places, limit=3):
    user_pos = (user_lat, user_lon)
    processed_list = []

    for p in all_places:
        item = dict(p)
        place_pos = (item['lat'], item['lon'])
        item['distance'] = geodesic(user_pos, place_pos).kilometers
        processed_list.append(item)

    return sorted(processed_list, key=lambda x: x['distance'])[:limit]

def format_feedback(reviews, fallback_text):
    if not reviews:
        return fallback_text
    return "\n".join([f"• {r}" for r in reviews])