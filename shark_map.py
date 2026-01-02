import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson
import os

def create_shark_map():
    print("🗺️ Generating Interactive Shark Map...")
    
    file_path = "data/shark_tracks.csv"
    if not os.path.exists(file_path):
        print("❌ Data file not found. Run 'get_universal_sharks.py' first.")
        return
        
    df = pd.read_csv(file_path, parse_dates=['time'])
    df = df.dropna(subset=['lat', 'lon'])
    
    # 1. Setup Map
    m = folium.Map(location=[20, -140], zoom_start=3, tiles='CartoDB dark_matter')

    # 2. Define Colors
    species_colors = {
        'White Shark': '#ff6b6b',          # Red
        'Blue Shark': '#54a0ff',           # Blue
        'Salmon Shark': '#ff9f43',         # Orange
        'Shortfin Mako Shark': '#a29bfe',  # Purple
        'Tiger Shark': '#1dd1a1',          # Green
    }
    default_color = '#b2bec3'

    # 3. Create Features
    features = []
    # Sample data if it's too huge (optional: remove .iloc if you want ALL points)
    # df = df.iloc[::5] 
    
    for _, row in df.iterrows():
        sp = row.get('species', 'Shark')
        color = species_colors.get(sp, default_color)
        
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [row['lon'], row['lat']],
            },
            'properties': {
                'time': row['time'].isoformat(),
                'style': {'color': color},
                'icon': 'circle',
                'iconstyle': {
                    'fillColor': color,
                    'fillOpacity': 0.8,
                    'stroke': 'false',
                    'radius': 3
                },
                'popup': f"<b>{sp}</b>"
            }
        }
        features.append(feature)

    # 4. Add Animation
    TimestampedGeoJson(
        {'type': 'FeatureCollection', 'features': features},
        period='P1D',    # 1 Day steps for faster animation over 20 years
        add_last_point=True,
        auto_play=False,
        loop=False,
        max_speed=10,
        loop_button=True,
        date_options='YYYY-MM-DD',
        time_slider_drag_update=True
    ).add_to(m)

    m.save("shark_tracker.html")
    print("✅ Map saved to: shark_tracker.html")

if __name__ == "__main__":
    create_shark_map()