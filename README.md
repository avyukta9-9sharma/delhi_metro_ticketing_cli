# Delhi Metro Ticketing CLI

This project uses `stations.csv` and `lines.csv` files (placed in `data/`) to build a simplified Delhi Metro ticket purchasing command line app that allows users to purchase tickets to travel from one metro station to another. A colored schematic map is also displayed.

## Functionality

1. Users can see a list of all the metro stations available.
2. Users can purchase a ticket from one metro station to another.
3. Users can see their purchased tickets.
4. Each ticket has a unique ID associated with it.
5. The price of a ticket is based on how many stations the user will cross on the shortest path to their destination.
6. There can be multiple metro lines, and some stations are expected to act as crossroads between 2 or more lines, which allows passengers to change lines.
7. Users can purchase tickets to travel between stations on different lines.
8. You must provide a list of instructions to assist the user in case there is a line change between the origin and the destination.
9. Make multiple CSV files to store data for each different class. You can populate the actual objects in these files at the start of the program or as and when it is required.
10. Create a graphical view of the map showing all stations and their connections. You may use Matplotlib or any similar Python graph visualization library.

Fare per station crossed = ₹7

## Files
- main.py : interactive CLI program (uses data/stations.csv and data/lines.csv)
- metro_map.py : generates colored schematic `delhi_metro_map_colored.png`
- data/stations.csv : list of major Delhi Metro Stations
- data/lines.csv : list of major Delhi Metro Lines
- data/tickets.csv : where purchased tickets are stored
- demo_run.py : simple script that purchases demo tickets programmatically

## Run
1. Install dependencies:
   pip install -r requirements.txt
2. Run CLI:
   python main.py
3. Generate colored map:
   python metro_map.py
