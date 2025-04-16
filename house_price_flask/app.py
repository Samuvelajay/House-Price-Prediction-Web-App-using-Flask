from flask import Flask, render_template, request  # ✅ Fix: Flasklash → Flask
import pickle
import numpy as np

app = Flask(__name__)  # ✅ Fix: _name_ → __name__

# Load model and column names
model = pickle.load(open('model.pkl', 'rb'))
columns = pickle.load(open('columns.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])  # ✅ Fix: method → methods (capitalized)
def predict():
    area = request.form['area']
    sqft = float(request.form['sqft'])
    bedroom = float(request.form['bedroom'])

    bathroom = float(request.form['bathroom'])  # ✅ Fix: spelling mistake & remove "-="
    room = float(request.form['room'])

    x_input = np.zeros(len(columns))
    x_input[columns.index('INT_SQFT')] = sqft
    x_input[columns.index('N_BEDROOM')] = bedroom
    x_input[columns.index('N_BATHROOM')] = bathroom
    x_input[columns.index('N_ROOM')] = room

    area_col = f'AREA_{area}'
    if area_col in columns:
        x_input[columns.index(area_col)] = 1

    predicted_price = model.predict([x_input])[0]
    return render_template('index.html', predicted_text=f"Predicted Price: ₹{predicted_price:,.2f}")

# ✅ Fix: "__main__" must be spelled exactly like this
if __name__ == "__main__":
    app.run(debug=True)
