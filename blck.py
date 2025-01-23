import logging
from io import BytesIO
from os import remove, rename
from os.path import isfile
from random import choice
from string import ascii_uppercase, ascii_lowercase
import sys

from flask import Flask, Blueprint, render_template, request, send_file, abort, jsonify, redirect, url_for
from werkzeug.utils import safe_join
import magic

debug_mode = '-d' in sys.argv

log_level = logging.DEBUG if debug_mode else logging.INFO

logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

if debug_mode:
    logging.getLogger().addHandler(logging.FileHandler('blck.log', mode='a'))

bp = Blueprint('blck', __name__, template_folder='templates')


@bp.route("/health", methods=['GET'])
def health_check():
    app.logger.debug('Health check called')
    return jsonify({'status': 'Healthy'}), 200


@bp.route("/", methods=['GET', 'POST'])
def index():
    app.logger.debug('Handling index route')
    if request.method == 'GET':
        return render_template('index.html', root='/')

    if 'c' not in request.files or not request.files['c'].filename:
        app.logger.error('No file selected or file is empty.')
        abort(400, "No file selected")

    upload_url = short(request.files['c'])
    app.logger.debug(f'File uploaded successfully, redirecting to {upload_url}')
    return redirect(url_for('blck.display_url', file_url=upload_url))


@bp.route("/url", methods=['GET'])
def display_url():
    file_url = request.args.get('file_url')
    if not file_url:
        app.logger.error('File URL is missing in request.')
        abort(400, "File URL is missing")
    app.logger.debug(f'Displaying URL: {file_url}')
    return f"<p>Your file is available at: <a href='{file_url}'>{file_url}</a></p>"


@bp.route("/<urlshort>")
def urlget(urlshort):
    app.logger.debug(f"Fetching URL: {urlshort}")
    fp = safe_join('files', urlshort)
    if not isfile(fp):
        app.logger.error(f"File {urlshort} not found.")
        abort(404)

    r = BytesIO()
    mime = magic.from_file(fp, mime=True)
    with open(fp, 'rb') as fo:
        r.write(fo.read())
    r.seek(0)
    remove(fp)
    app.logger.debug(f"Serving file {urlshort} with MIME type {mime}.")
    return send_file(r, mimetype=mime)


def short(c):
    app.logger.debug('Shortening file upload')
    if not c:
        app.logger.error('No file provided.')
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
        app.logger.debug('Request is using HTTPS')
        return ''.join([
            request.url_root.replace('http://', 'https://'),
            s
        ])
    app.logger.debug('Request is using HTTP')
    return ''.join([request.url_root, s])


def genid(size=4, chars=ascii_uppercase + ascii_lowercase):
    return ''.join(choice(chars) for i in range(size))


app = Flask(__name__)
app.config['PREFERRED_URL_SCHEME'] = 'https'
app.register_blueprint(bp, url_prefix='/')

if __name__ == '__main__':
    app.logger.info('Application started.')
    app.run(host='0.0.0.0', port=8080, debug=debug_mode)
