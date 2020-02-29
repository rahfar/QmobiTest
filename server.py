from http.server import BaseHTTPRequestHandler, HTTPServer
from value_converter import convert_usd_to_rub
import settings
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
logger.addHandler(settings.stream_handler)


def main():
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path == '/api':
                # try to read incoming data
                try:
                    content_length = int(self.headers.get('Content-Length'))
                    data = self.rfile.read(content_length)
                    usd_amount = json.loads(data).get('usd_amount')
                except:
                    logger.exception('EXCEPTION')
                    self.send_response(404, message='Incorrect data')
                    self.end_headers()
                    return

                # try to count exchange
                try:
                    rub_amount, exchange_rate = convert_usd_to_rub(usd_amount)
                    resp_json = {
                        "rub_amount": rub_amount,
                        "usd_amount": usd_amount,
                        "exchange_rate": exchange_rate
                    }
                    logger.debug(resp_json)
                except:
                    logger.exception('EXCEPTION')
                    self.send_response(500, message='Internal error')
                    self.end_headers()
                    return

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(resp_json).encode('utf-8'))
            else:
                self.send_response(404, message='Incorrect URL')
                self.end_headers()
            return

        def log_message(self, format, *args):
            logger.info("%s - %s" %
                        (self.address_string(),
                         format % args))

    try:
        server = HTTPServer(('', settings.PORT_NUMBER), Handler)
        logger.info(f'Started http server on port {settings.PORT_NUMBER}')
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()


if __name__ == '__main__':
    main()
