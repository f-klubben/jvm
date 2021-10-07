import re
from datetime import datetime

# Handles the "DispensedDrinkEvent"
# Each mail contains the 10 last DispensedDrinkEvent
def handle_dispensed(mail, subject, mail_date):
  # Parses a string like 06/10/2021 08:47:43:177  DispensedDrinkEvent  "Filter coffee" "succes" 
  matches = re.findall(r"(\d+\/\d+\/\d+\s\d+:\d+:\d+:\d+)\s+DispensedDrinkEvent\s+\"(.+?)\"\s+\"(.+?)\"", mail)
  for m in matches:
    dispensed_date = datetime.strptime(m[0], '%d/%m/%Y %H:%M:%S:%f')
    dispensed_product = m[1]
    dispensed_status = m[2]
    print(f'Dispensed {dispensed_status} - {dispensed_product} at {dispensed_date}')

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