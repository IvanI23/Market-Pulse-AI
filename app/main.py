import sqlite3

def display_table_contents():
    conn = sqlite3.connect('sql/market_pulse.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    for table in tables:
        print(f"{table}:")
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        print()
    
    conn.close()

if __name__ == "__main__":
    display_table_contents()