# vr_frontend

Valureach Anmerkungen:
Die Zugangsdaten zur Datenbank und Mail Server sind im Code enthalten diese Daten
herauslöschen bevor etwas ins öffentlich zugängliche Git Repository gepusht wird.
Fürs weitere entwickeln diese Zugangdaten in die Dateien config.py und gmail_mail_sender.py
einfügen.

*Code Aktualisierungen durchführen:
*Aktualisierten Code ins Git Repository laden.
*Git Repository am Server aktualisieren.
*Wenn Änderungen am DB Model vorgenommen worden sind:
*python manage.py db migrate → migriert die Models
*python manage.py db upgrade → lädt die Änderungen in die Datenbank
*Gunicorn erkennt die Änderungen sofort (das hat mich auch überrascht :) )
*Somit sollte der Server damit upgedatet sein.
*Falls die Änderungen doch nicht Sichtbar sind:
*sudo supervisorctl
*- hier werden die laufenden Prozesse die von supervisor überwacht werden aufgelistet
*- restart vr_frontend
*→ exit
*anschließend sudo service nginx reload
