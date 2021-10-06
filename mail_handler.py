import re

def handle_mail(mail, subject, mail_date):
  print('TODO: handle_mail')
  pass

def handle_dispensed(mail, subject, mail_date):
  print('TODO: handle_dispensed')
  pass

def handle_driptray(mail, subject, mail_date):
  print('TODO: handle_driptray')
  pass

def handle_status(mail, subject, mail_date):
  print('TODO: handle_status')
  pass

def handle_cleaning(mail, subject, mail_date):
  print('TODO: handle_cleaning')
  pass


def handle_mail(mail) -> bool:
  subject = None
  print(mail)
  subject_match = re.search('Subject: (.*)', mail)
  if subject_match:
    subject = subject_match.group(1)
    print(subject)

  mail_date_match = re.search('Date: (.*)', mail)
  if mail_date_match:
    mail_date = mail_date_match.group(1)
  
  if not subject:
    return False

  if subject.endswith('DispensedDrinkEvent'):
    handle_dispensed(mail, subject, mail_date)
  elif subject.endswith('Drypbakke mangler'):
    handle_driptray(mail, subject, mail_date)
  elif subject.endswith('EVADTS status'):
    handle_status(mail, subject, mail_date)
  elif subject.endswith('Rengørrings begivenhed'):
    handle_cleaning(mail, subject, mail_date)
  else:
    return False

  return True