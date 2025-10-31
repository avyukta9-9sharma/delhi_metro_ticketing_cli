#!/usr/bin/env python3
"""main.py - Delhi Metro Ticketing CLI (uses data/stations.csv and data/lines.csv)
Fare per station crossed = 7
"""
import csv, uuid, os, sys
from collections import deque

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATIONS_CSV = os.path.join(DATA_DIR, "stations.csv")
LINES_CSV = os.path.join(DATA_DIR, "lines.csv")
TICKETS_CSV = os.path.join(DATA_DIR, "tickets.csv")

FARE_PER_STATION = 7

class Station:
    def __init__(self, station_id, name, lines=None):
        self.id = station_id
        self.name = name
        self.lines = set([x.strip() for x in lines.split(',') if x.strip()]) if isinstance(lines, str) else set()

    def to_dict(self):
        return {"station_id": self.id, "station_name": self.name, "lines": ",".join(sorted(self.lines))}

class Line:
    def __init__(self, line_id, name, station_ids=None):
        self.id = line_id
        self.name = name
        self.station_ids = [x.strip() for x in station_ids.split(',') if x.strip()] if isinstance(station_ids, str) else list(station_ids or [])

    def to_dict(self):
        return {"line_id": self.id, "line_name": self.name, "station_ids": ",".join(self.station_ids)}

class Ticket:
    def __init__(self, ticket_id, origin_id, dest_id, path_station_ids, price, instructions):
        self.ticket_id = ticket_id
        self.origin_id = origin_id
        self.dest_id = dest_id
        self.path_station_ids = path_station_ids
        self.price = price
        self.instructions = instructions

    def to_dict(self):
        return {
            "ticket_id": self.ticket_id,
            "origin_id": self.origin_id,
            "dest_id": self.dest_id,
            "path_station_ids": "|".join(self.path_station_ids),
            "price": str(self.price),
            "instructions": self.instructions
        }

class MetroNetwork:
    def __init__(self):
        self.stations = {}
        self.lines = {}
        self.adj = {}

    def add_station(self, s: Station):
        self.stations[s.id] = s
        self.adj.setdefault(s.id, set())

    def add_line(self, l: Line):
        self.lines[l.id] = l
        ids = l.station_ids
        for i in range(len(ids)-1):
            a, b = ids[i], ids[i+1]
            self.adj.setdefault(a, set()).add(b)
            self.adj.setdefault(b, set()).add(a)
        for sid in ids:
            if sid in self.stations:
                self.stations[sid].lines.add(l.name)

    def shortest_path(self, origin, dest):
        if origin not in self.stations or dest not in self.stations:
            return None
        q = deque([origin])
        prev = {origin: None}
        while q:
            cur = q.popleft()
            if cur == dest:
                break
            for nb in sorted(self.adj.get(cur, [])):
                if nb not in prev:
                    prev[nb] = cur
                    q.append(nb)
        if dest not in prev:
            return None
        path = []
        cur = dest
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return path

    def instructions_for_path(self, path):
        if not path:
            return ""
        def common_lines(a,b):
            return self.stations[a].lines.intersection(self.stations[b].lines)
        steps = []
        cur_line = None
        for i in range(len(path)-1):
            a, b = path[i], path[i+1]
            c = common_lines(a,b)
            chosen = None
            if c:
                if cur_line and cur_line in c:
                    chosen = cur_line
                else:
                    chosen = sorted(c)[0]
            steps.append((a,b,chosen))
            cur_line = chosen
        if not steps:
            return "You are already at your destination."
        inst = []
        start = self.stations[path[0]].name
        cur_line = steps[0][2] or "unknown line"
        inst.append(f"Start at {start} on {cur_line}.")
        for i,(a,b,line_name) in enumerate(steps):
            if i>0 and line_name != cur_line:
                inst.append(f"Change from {cur_line} to {line_name} at {self.stations[a].name}.")
                cur_line = line_name
        inst.append(f"Arrive at {self.stations[path[-1]].name}.")
        return " ".join(inst)

def _normalize_row_keys(row):
    return {k.lstrip('\ufeff').strip(): v for k, v in row.items()}

def load_network():
    net = MetroNetwork()
    if not os.path.exists(STATIONS_CSV) or not os.path.exists(LINES_CSV):
        raise FileNotFoundError("stations.csv or lines.csv missing in data/")
    with open(STATIONS_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            r2 = _normalize_row_keys(r)
            s = Station(r2.get('station_id'), r2.get('station_name'), r2.get('lines',''))
            net.add_station(s)
    with open(LINES_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            r2 = _normalize_row_keys(r)
            l = Line(r2.get('line_id'), r2.get('line_name'), r2.get('station_ids',''))
            net.add_line(l)
    return net

class TicketingSystem:
    def __init__(self, net, tickets_csv=TICKETS_CSV):
        self.net = net
        self.tickets_csv = tickets_csv
        self.tickets = []
        if os.path.exists(self.tickets_csv):
            with open(self.tickets_csv, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    r2 = _normalize_row_keys(r)
                    path = r2.get('path_station_ids','').split('|') if r2.get('path_station_ids') else []
                    self.tickets.append(Ticket(r2.get('ticket_id'), r2.get('origin_id'), r2.get('dest_id'), path, float(r2.get('price',0)), r2.get('instructions','')))

    def list_stations(self):
        for s in sorted(self.net.stations.values(), key=lambda x: x.name):
            print(f"{s.id} - {s.name} (Lines: {', '.join(sorted(s.lines))})")

    def purchase_ticket(self, origin, dest):
        path = self.net.shortest_path(origin, dest)
        if path is None:
            raise ValueError("No path between stations.")
        stations_crossed = max(0, len(path)-1)
        price = stations_crossed * FARE_PER_STATION
        instructions = self.net.instructions_for_path(path)
        tid = str(uuid.uuid4())
        ticket = Ticket(tid, origin, dest, path, price, instructions)
        self.tickets.append(ticket)
        self._save_ticket(ticket)
        return ticket

    def _save_ticket(self, ticket):
        file_exists = os.path.exists(self.tickets_csv)
        with open(self.tickets_csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['ticket_id','origin_id','dest_id','path_station_ids','price','instructions'])
            if not file_exists:
                writer.writeheader()
            writer.writerow(ticket.to_dict())

    def show_tickets(self):
        if not self.tickets:
            print("No tickets purchased yet.")
            return
        for t in self.tickets:
            origin = self.net.stations[t.origin_id].name
            dest = self.net.stations[t.dest_id].name
            print(f"Ticket ID: {t.ticket_id}\n From: {origin} -> To: {dest}\n Stations crossed: {len(t.path_station_ids)-1}\n Price: {t.price}\n Instructions: {t.instructions}\n")

def interactive():
    print("Loading Delhi Metro network (simplified)...")
    net = load_network()
    ts = TicketingSystem(net)
    print("Welcome to Delhi Metro Ticketing CLI")
    while True:
        print("\n1. List stations\n2. Purchase ticket\n3. Show purchased tickets\n4. Exit")
        c = input("Enter choice: ").strip()
        if c == '1':
            ts.list_stations()
        elif c == '2':
            o = input("Origin station id: ").strip()
            d = input("Destination station id: ").strip()
            try:
                t = ts.purchase_ticket(o,d)
                print(f"Ticket purchased! ID: {t.ticket_id}, Price: {t.price}")
                print("Instructions:", t.instructions)
            except Exception as e:
                print("Error:", e)
        elif c == '3':
            ts.show_tickets()
        elif c == '4':
            print("Goodbye!"); break
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    interactive()
