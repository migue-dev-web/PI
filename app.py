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
    if request.method == 'POST':
        link = request.form('link')
        try:
            con = conn()
            cursor = con.cursor()
            cursor.execute("INSERT INTO links (link) VALUES (%s) RETURNING id ", (link,))
            link_id = cursor.fetchone()['id']
            con.commit()
            print("Link agregado correctamente.")
        except Exception as e:
            print(f"Error al agregar el link: {e}")
        finally:
            cursor.close()
            con.close()
            return render_template("newcut.html", link_id=link_id)
    
    return render_template("newcut.html")

@app.route('/link/<int:idL>')
def links(idL):
    try:
        con = conn()
        cursor = con.cursor()
        cursor.execute("SELECT link FROM links WHERE id = %s", (idL,))
        cutl = cursor.fetchone()
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
    finally:
        cursor.close()
        con.close()
    return render_template("redir.html", cutl=cutl )

@app.route('/never')
def never():
   return render_template("redirect.html")
if __name__ == '__main__':
    app.run(debug=True)