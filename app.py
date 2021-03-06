import requests
from flask import Flask, render_template, request

from autosummary.document import Document

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index(content=None, warning=None):
    if request.method == 'POST':
        ratio = float(request.form['slider'])/100
        if request.form['url'] and request.form['raw']:
            warning = 'Please insert only one input.'
        else:
            if request.form['url']:
                try:
                    content = Document(url=request.form['url']).summary(ratio=ratio)
                except requests.exceptions.RequestException as e:
                    warning = format(e)
            elif request.form['raw']:
                content = Document(text=request.form['raw']).summary(ratio=ratio)
            else:
                warning = 'Missing input!'
    return render_template('index.html', content=content, warning=warning)


if __name__ == '__main__':
    app.run(debug=True)
