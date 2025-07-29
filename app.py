from flask import Flask, render_template

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def home():
    return render_template('home.html')

  
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True, use_reloader=True)

