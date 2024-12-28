#!/usr/bin/env python3
# copyleft (c) 2017-2021 parazyd <parazyd@dyne.org>
# see LICENSE file for copyright and license details.

import logging
from io import BytesIO
from os import remove, rename
from os.path import isfile
from random import choice
from string import ascii_uppercase, ascii_lowercase

from flask import Flask, Blueprint, render_template, request, send_file, abort
from werkzeug.utils import safe_join  # Updated import for Flask 3.x
import magic

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all logs (INFO, DEBUG, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler('app.log', mode='a')  # Output to file
    ]
)

bp = Blueprint('blck', __name__, template_folder='templates')


@bp.route("/", methods=['GET', 'POST'])
def index():
    app.logger.debug('Handling index route')
    if request.method == 'GET':
        return render_template('index.html', root=args.r)
    return short(request.files)


@bp.route("<urlshort>")
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
    if not c or not c['c']:
        app.logger.error('No file provided or file is empty.')
        return abort(400)

    s = genid()
    f = c['c']
    f.save(safe_join('files', s))

    mimetype = f.mimetype
    if not mimetype:
        mimetype = magic.from_file(safe_join('files', s), mime=True)

    if mimetype:
        t, s = s, '.'.join([s, mimetype.split('/')[1]])
        rename(safe_join('files', t), safe_join('files', s))

    # Log protocol used for the request
    if request.headers.get('X-Forwarded-Proto') == 'https':
        app.logger.debug('Request is using HTTPS')
        return ''.join([
            request.url_root.replace('http://', 'https://'),
            args.r.lstrip('/'), s, '\n'
        ])
    app.logger.debug('Request is using HTTP')
    return ''.join([request.url_root + args.r.lstrip('/'), s, '\n'])


def genid(size=4, chars=ascii_uppercase + ascii_lowercase):
    return ''.join(choice(chars) for i in range(size))


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-r', default='/', help='application root')
    parser.add_argument('-l', default='localhost', help='listen host')
    parser.add_argument('-p', default=13321, help='listen port')
    parser.add_argument('-d', default=False, action='store_true', help='debug')
    args = parser.parse_args()

    # Configure Flask app
    app = Flask(__name__)
    app.register_blueprint(bp, url_prefix=args.r)

    # Run the app
    if args.d:
        app.logger.setLevel(logging.DEBUG)
        app.run(host='0.0.0.0', port=args.p, threaded=True, debug=args.d)
    else:
        app.logger.setLevel(logging.INFO)
        from bjoern import run
        run(app, args.l, int(args.p))

    app.logger.info('Application started.')
