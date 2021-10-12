from mail_handler import handle_mail
from os import listdir
from os.path import join, isfile

DIR = 'test_mails'

files = [str(join(DIR, f)) for f in listdir(DIR) if f.endswith('.eml') and isfile(join(DIR, f))]


for f in sorted(files):
    with open(f, 'r') as e:
        if handle_mail(e.read()):
            # print(f'SUCCESS: correctly parse file: "{f}"')
            pass
        else:
            print(f'FAILURE: failed to parse file: "{f}"')
