# JVM

Statistics collector and generator for Wittenborg-91XX coffee-machine.


`Jinja2` required for running. [Black](https://github.com/psf/black) for formatting the code.

Get started:
```bash
python3 server.py
```

Run tests
```bash
python3 test.py
```

### Styling
The project uses [Black](https://github.com/psf/black) for formatting the code.
```bash
black --target-version py36 --line-length 120 --skip-string-normalization *.py
```

## Systemd service
See [coffee.service](coffee.service) for in-use service. Service runs `server.py` to periodically handle mails and generate statistics. 
Generated html is symlinked to `/var/www/coffee`, which Apache exposes with SSL-cert stapling.

### Technical details

#### Intercepting mails
The project acts as a SMTP server for the coffemachine using the [smtplib](https://docs.python.org/3/library/smtplib.html). The coffeemachine sends a lot of mails to the server.
This project then handles each of these mails.

For capturing SMTP mails for later test use:
```bash
python3 server.py capture
```
Emails are then saved under `logged_mails/`

#### Updating estimates
The coffeemachine has an internal counter for keeping track of the ingredients in the machine. The levels are being sent out using mails, but it only sends for 3 thresholds: Full, Empty and User Threshold.
This complicates the collection of metrics to use in statistics.
As such, the project creates estimates based on 2 other mails:
* `DrinkDispensedEvent`: A mail sent every time a drink is dispensed. Each of these events has a cost associated with them in the `Product`-table.
* `MenuParameter`: A mail sent every time a menu parameter has been changed. Whenever the coffeemachine has had X amount added to it, this mail will reflect it.

#### Generation of statistics
Inside [generator](generator) there is a script which queries the database and creates a HTML report page.
