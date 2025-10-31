from pathlib import Path
import sys, os, pandas as pd
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from main import load_network, TicketingSystem
net = load_network()
ts = TicketingSystem(net, tickets_csv=str(BASE/'data'/'tickets.csv'))
# Read stations via pandas for robustness
df = pd.read_csv(BASE/'data'/'stations.csv')
if len(df) >= 4:
    a = df.iloc[0]['station_id']
    b = df.iloc[3]['station_id']
    try:
        t = ts.purchase_ticket(a,b)
        print('Purchased demo ticket:', t.ticket_id, a, '->', b, 'Price:', t.price)
    except Exception as e:
        print('Demo purchase error:', e)
else:
    print('Not enough stations for demo.')