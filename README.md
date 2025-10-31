# Delhi Metro Ticketing CLI

This project uses `stations.csv` and `lines.csv` files (placed in `data/`) to build a simplified Delhi Metro ticketing CLI and a colored schematic map.

Fare per station crossed = ₹7

## Files
- main.py : interactive CLI program (uses data/stations.csv and data/lines.csv)
- metro_map.py : generates colored schematic `delhi_metro_map_colored.png`
- data/stations.csv : List of major Delhi Metro Stations
- data/lines.csv : List of major Delhi Metro Lines
- data/tickets.csv : where purchased tickets are stored
- demo_run.py : simple script that purchases demo tickets programmatically

## Run
1. (Optional) Install dependencies:
   pip install -r requirements.txt
2. Run CLI:
   python main.py
3. Generate colored map:
   python metro_map.py
