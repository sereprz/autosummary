from flask import Flask, render_template, request

from autosummary.document import Document

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index(content=None, warning=False):
    if request.method == 'POST':
        if request.form['url']:
            doc = Document(url=request.form['url'])
            content = doc.summary()
        else:
            warning = True
    return render_template('index.html', content=content, warning=str(warning))


if __name__ == '__main__':
    app.run(debug=True)
