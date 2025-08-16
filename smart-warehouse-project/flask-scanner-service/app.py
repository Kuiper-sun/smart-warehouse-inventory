from flask import Flask, request, jsonify
from datetime import datetime
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    """Establishes a connection to the database using environment variables."""
    conn = psycopg2.connect(
        dbname=os.environ.get("DB_DATABASE"),
        user=os.environ.get("DB_USERNAME"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT", "5432")
    )
    return conn

@app.route('/rfid-scan', methods=['POST'])
def scan_barcode():
    """Handles incoming scan data and inserts it into the database."""
    data = request.json
    if not all(k in data for k in ['sku', 'product_name', 'quantity', 'status']):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO inventory (sku, product_name, quantity, last_scanned, status)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (data['sku'], data['product_name'], data['quantity'], datetime.now(), data['status'])
            )
        conn.commit()
        return jsonify({"message": "Scan recorded successfully"}), 201
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({"error": "Database operation failed"}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 
