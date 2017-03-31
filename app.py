import requests
from flask import Flask, render_template, request

from autosummary.document import Document

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index(content=None, warning=None):
    if request.method == 'POST':
        if request.form['url'] and request.form['raw']:
            warning = 'Please insert only one input.'
        else:
            if request.form['url']:
                try:
                    content = Document(url=request.form['url']).summary()
                except requests.exceptions.MissingSchema:
                    warning = 'Invalid URL. Did you mean http://{}?'.format(
                        request.form['url'])
            elif request.form['raw']:
                content = Document(text=request.form['raw']).summary()
            else:
                warning = 'Missing input!'
    return render_template('index.html', content=content, warning=warning)


if __name__ == '__main__':
    app.run(debug=True)
