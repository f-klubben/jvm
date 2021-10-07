from mail_handler import handle_mail

files = [
  'test_mails/20210925051638-22.eml'
]

for f in files:
  with open(f, 'r') as e:
    if handle_mail(e.read()):
      print(f'SUCCESS: correctly parse file: "{f}"')
    else:
      print(f'FAILURE: failed to parse file: "{f}"')