from flask import Flask, render_template, request

from autosummary.document import Document

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index(content=None):
    if request.method == 'POST':
        doc = Document(url=request.form['url'])
        content = doc.summary()
    return render_template('index.html', content=content)


if __name__ == '__main__':
    app.run(debug=True)
