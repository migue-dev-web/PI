from flask import Flask, render_template, request, redirect, url_for
import os
from psycopg2.extras import RealDictCursor
import psycopg2

app = Flask(__name__)

def conn():
    con = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT", 5432)
    )
    return con


def create_DB():
    try:
        con = conn()
        cursor = con.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS links (
                    id SERIAL PRIMARY KEY,
                    link VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
""")
        
        con.commit()
        print("Tabla 'links' creada correctamente.")
    except Exception as e:
        print(f"Error al crear la tabla: {e}")
    finally:
        cursor.close()
        con.close()

    return  



@app.route('/')
def home():
    create_DB()  # crea la tabla en caso de que no exista
    return render_template("index.html")

@app.route('/newLink', methods=['GET, POST'])
def addLink():
    if request.method == 'POST':
        con = conn()
        cursor = con.cursor()
        link = request.form['link']
        query = "INSERT INTO links (link) VALUES (%s) RETURNING id"
        cursor.execute(query, (link))
        nuevo_id = cursor.fetchone()[0]
        con.commit()
        cursor.close()
        con.close() 
    return  redirect(url_for('/newcut/' + nuevo_id)) 

@app.route('/newcut/<int:id>')
def newCut(id):
    render_template("newcut.html", id=id)
    return

   


  

@app.route('/link/<int:id>')
def viewLink(id):
   render_template("redir.html", id=id) #link = li
   return



@app.route('/never')
def never():
   return render_template("redirect.html")
if __name__ == '__main__':
    app.run(debug=True)