from flask import Flask, Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import safe_join
import magic
from io import BytesIO
from os import remove, rename
from os.path import isfile
from random import choice
from string import ascii_uppercase, ascii_lowercase

bp = Blueprint('blck', __name__, template_folder='templates')


@bp.route("/health", methods=['GET'])
def health_check():
    return jsonify({'status': 'Healthy'}), 200


@bp.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', root='/')

    if 'c' not in request.files or not request.files['c'].filename:
        abort(400, "No file selected")

    upload_url = short(request.files['c'])
    return redirect(url_for('blck.display_url', file_url=upload_url))


@bp.route("/url", methods=['GET'])
def display_url():
    file_url = request.args.get('file_url')
    if not file_url:
        abort(400, "File URL is missing")
    return f"<p>Your file is available at: <a href='{file_url}'>{file_url}</a></p>"


@bp.route("/<urlshort>")
def urlget(urlshort):
    fp = safe_join('files', urlshort)
    if not isfile(fp):
        abort(404)

    r = BytesIO()
    mime = magic.from_file(fp, mime=True)
    with open(fp, 'rb') as fo:
        r.write(fo.read())
    r.seek(0)
    remove(fp)
    return send_file(r, mimetype=mime)


def short(c):
    if not c:
        abort(400)

    s = genid()
    f = c
    f.save(safe_join('files', s))

    mimetype = f.mimetype
    if not mimetype:
        mimetype = magic.from_file(safe_join('files', s), mime=True)

    if mimetype:
        t, s = s, '.'.join([s, mimetype.split('/')[1]])
        rename(safe_join('files', t), safe_join('files', s))

    if request.headers.get('X-Forwarded-Proto') == 'https':
        return ''.join([
            request.url_root.replace('http://', 'https://'),
            '/', s
        ])
    return ''.join([request.url_root, '/', s])


def genid(size=4, chars=ascii_uppercase + ascii_lowercase):
    return ''.join(choice(chars) for i in range(size))


app = Flask(__name__)
app.config['PREFERRED_URL_SCHEME'] = 'https'

app.register_blueprint(bp, url_prefix='/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
