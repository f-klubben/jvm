from __future__ import print_function
from datetime import datetime
from mail_handler import handle_mail
import asyncore
from smtpd import SMTPServer

class KaffeLogger(SMTPServer):
    no = 0
    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=['BODY=8BITMIME', 'SMTPUTF8'], rcpt_options=[]):
        text = data.decode('UTF-8')
        if not handle_mail(text):
            filename = '%s-%d.eml' % (datetime.now().strftime('%Y%m%d%H%M%S'),
                self.no)
            f = open(filename, 'w')
            f.write(text)
            f.close
            print('%s saved.' % filename)
        self.no += 1


def run():
    # start the smtp server on localhost:1025
    ip = '0.0.0.0'
    port = 2525
    foo = KaffeLogger((ip, port), None)
    print(f'Now listening for mails on ip: {ip}, port {port}')
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run()