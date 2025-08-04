import sqlite3
import os

def run_query(query):
    db_path = os.path.join(os.path.dirname(__file__), '..', 'sql', 'market_pulse.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            # Get column names
            column_names = [description[0] for description in cursor.description]
            
            print(f"\n{'='*60}")
            print(f"Query: {query}")
            print(f"{'='*60}")
            
            if results:
                # Print header
                print(" | ".join(column_names))
                print("-" * 60)
                
                # Print rows
                for row in results:
                    print(" | ".join(str(val) for val in row))
                
                print(f"\nRows returned: {len(results)}")
            else:
                print("No results found.")
        else:
            conn.commit()
            print(f"Query executed successfully: {cursor.rowcount} rows affected")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("Database Query Tool")
    print("Enter SQL queries (or 'quit' to exit)")
    
    # Quick status check
    print("\n📊 DATABASE STATUS:")
    run_query("SELECT * from news_articles LIMIT 5")
    run_query("SELECT * from stock_prices LIMIT 5")
    run_query("SELECT * from sentiment_price_effect LIMIT 5")

    while True:
        query = input("\n🔍 SQL> ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            break
        
        if query:
            run_query(query)