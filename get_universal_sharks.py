from erddapy import ERDDAP
import pandas as pd

def get_every_shark_available():
    print("🦈 Connecting to IOOS ATN Global Database...")
    
    e = ERDDAP(
        server="https://atn.ioos.us/erddap",
        protocol="tabledap",
        response="csv"
    )

    # This is the massive "Tagging of Pacific Predators" archive
    e.dataset_id = "stanford_import_ssm_public"

    # We request the essential columns
    e.variables = [
        "time",
        "latitude",
        "longitude",
        "topp_id",       # Shark ID
        "common_name",   # Species Name
    ]

    # --- THE BRUTE FORCE SETTING ---
    # 1. We go back to year 2000 to catch the Mako/Salmon/Blue shark campaigns.
    # 2. We do NOT filter by name on the server (to avoid server errors).
    e.constraints = {
        "time>=": "2000-01-01T00:00:00Z"
    }

    print("⬇️  Downloading ENTIRE Shark Archive (2000-Present)...")
    print("    (This handles ~20 years of data, please wait 30-60 seconds)")

    try:
        # Download everything
        df = e.to_pandas(
            index_col="time (UTC)",
            parse_dates=True,
        ).dropna()

        # Rename columns standard for your pipeline
        df = df.rename(columns={
            "latitude (degrees_north)": "lat",
            "longitude (degrees_east)": "lon",
            "topp_id": "shark_id",
            "common_name": "species"
        })

        print(f"   📦 Raw Database Rows: {len(df)}")

        # --- PYTHON FILTERING ---
        # We now keep ANYTHING that has 'shark' in the name.
        # This catches "Salmon Shark", "Blue Shark", "White Shark", "Mako Shark", etc.
        print("🔍 Extracting all species...")
        df_sharks = df[df['species'].str.contains("shark|Shark", na=False, case=False)]

        # Statistics
        print("\n✅ SUCCESS! Found the following species:")
        print(df_sharks['species'].value_counts())

        # Save
        output_file = "data/shark_tracks.csv"
        df_sharks.to_csv(output_file)
        print(f"\n💾 Saved {len(df_sharks)} tracks to: {output_file}")
        print("👉 You can now run 'python shark_map.py' to see all colors.")

    except Exception as err:
        print(f"❌ Error: {err}")

if __name__ == "__main__":
    get_every_shark_available()