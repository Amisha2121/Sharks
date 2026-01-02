from erddapy import ERDDAP
import pandas as pd

def fetch_all_sharks_final():
    print("🦈 Connecting to IOOS ATN...")
    
    e = ERDDAP(
        server="https://atn.ioos.us/erddap",
        protocol="tabledap",
        response="csv"
    )

    e.dataset_id = "stanford_import_ssm_public"

    # 1. Select variables (Removed 'year' which caused the crash)
    e.variables = [
        "time",
        "latitude",
        "longitude",
        "topp_id",       # Unique Shark ID
        "common_name",   # Species Name
    ]

    # 2. FILTER BY TIME (The Fix)
    # Instead of "year", we use the standard ISO timestamp format
    e.constraints = {
        "time>=": "2010-01-01T00:00:00Z"
    }

    print(f"⬇️  Downloading data (Since 2010)...")

    try:
        # 3. Download
        df = e.to_pandas(
            index_col="time (UTC)",
            parse_dates=True,
        ).dropna()
        
        # Rename columns
        df = df.rename(columns={
            "latitude (degrees_north)": "lat",
            "longitude (degrees_east)": "lon",
            "topp_id": "shark_id",
            "common_name": "species"
        })

        print(f"   Raw records fetched: {len(df)}")

        # 4. FILTER FOR SHARKS (Python Side)
        # Keeps only rows where the species name has 'shark' in it
        print("🔍 Filtering for sharks...")
        df_sharks = df[df['species'].str.contains("shark|Shark", na=False)]

        # 5. Save
        output_file = "data/shark_tracks.csv"
        df_sharks.to_csv(output_file)
        
        print(f"\n✅ SUCCESS! Saved {len(df_sharks)} shark tracking points.")
        print(f"🦈 Species: {df_sharks['species'].unique()}")
        print(f"💾 Saved to: {output_file}")
        
    except Exception as err:
        print(f"❌ Error: {err}")

if __name__ == "__main__":
    fetch_all_sharks_final()