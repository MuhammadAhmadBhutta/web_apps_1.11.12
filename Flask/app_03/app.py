from flask import Flask, render_template, request
from model.recommender import get_recommendations

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    cid1 = request.form['customer_id1'].strip()
    cid2 = request.form['customer_id2'].strip()
    cid3 = request.form['customer_id3'].strip()

    rec1 = get_recommendations(cid1) if cid1 else [{"Product Name": "No ID provided."}]
    rec2 = get_recommendations(cid2) if cid2 else [{"Product Name": "No ID provided."}]
    rec3 = get_recommendations(cid3) if cid3 else [{"Product Name": "No ID provided."}]

    return render_template(
        'recommendations.html',
        customer_id1=cid1, rec1=rec1,
        customer_id2=cid2, rec2=rec2,
        customer_id3=cid3, rec3=rec3
    )

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
