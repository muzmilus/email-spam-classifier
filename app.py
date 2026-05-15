from flask import Flask, render_template, request
import pickle
from pathlib import Path

app = Flask(__name__)

#========================loading the save files==================================================
BASE_DIR = Path(__file__).resolve().parent
model = pickle.load(open(BASE_DIR / 'logistic_regression.pkl', 'rb'))
feature_extraction = pickle.load(open(BASE_DIR / 'feature_extraction.pkl', 'rb'))


def predict_mail(input_text):
    input_user_mail  = [input_text]
    input_data_features = feature_extraction.transform(input_user_mail)
    prediction = int(model.predict(input_data_features)[0])

    confidence = 0.0
    if hasattr(model, 'predict_proba'):
        probabilities = model.predict_proba(input_data_features)[0]
        confidence = round(float(max(probabilities) * 100), 2)

    return prediction, confidence


@app.route('/', methods=['GET', 'POST'])
def analyze_mail():
    if request.method == 'POST':
        mail = request.form.get('mail', '')
        predicted_mail, confidence = predict_mail(input_text=mail)
        return render_template(
            'index.html',
            classify=predicted_mail,
            confidence=confidence,
            mail_text=mail
        )

    return render_template('index.html', mail_text='')

if __name__ == '__main__':
    app.run(debug=True)
