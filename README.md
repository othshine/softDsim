# softDsim

IT Project Management Simulation Web Application

## Abstract

Die SoftDSim ist eine Django-basierte Web-Anwendung zur Simulation von Projektmanagement-Szenarios für den Einsatz im Modul Project Management an der [Frankfurt University of Applied Sciences](https://www.frankfurt-university.de/). Dozenten  können innerhalb der Web-Anwendung Szenarios mit belieben Inhalten definieren, welche dann von Studierenden simuliert werden. Die Studierenden nehmen dabei die Rolle eines Projektmanagers ein und müssen verschiedene Entscheidungen treffen. Beispielhaft genannte Entscheidungen sind *Projektmanagementmethode*, *Anzahl und Erfahrungsniveau der Teammitglieder* oder *Anzahl der Meetings*. Alle Simulationen werden in einer gemeinsamen Datenbank gespeichert. Diese kann vom Dozenten eingesehen werden, sodass die Leistungen der Studierenden evaluiert werden kann.

## Wie werde ich Collaborator

Die Weiterentwiccklung des SofDsim Projekts ist Bestandteil des Mouduls Projekt im 7. Semster der Studiengänge EBIS und IBIS im Sommersemster 2022. Wenn du in diesem Modul eingeschreiben bist und in der SofDsim Projektgruppe (Trost) bist, dann benötigst du Collaborator Zugang zum Projekt. Dazu benötigst du einen GitHub-Account. Sende dann deinen Usernamen an [anton.roeser@stud.fra-uas.de](anton.roeser@stud.fra-uas.de) um als Collaborator zum Projekt hinzugefügt zu werden.

## Aufsetzen des Projekts

### Projekt clonen

[Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) das Projekt. Dazu muss [git](https://git-scm.com/downloads) auf deiem System installiert sein.

### Python installieren

Eine Installation von [Python 3](https://www.python.org/downloads/) ist notwendig. Falls auf dem System verschiedene Python Projekte vorhanden sind, ist es sinnvoll für das *SoftDSim* Projekt ein eigenes Python Environment (siehe [venv](https://docs.python.org/3/library/venv.html), [conda](https://docs.conda.io/en/latest/)
oder [virtualenv](https://pypi.org/project/virtualenv/)) anzulegen.

### Requirements installieren

Die nötigen Pythonabhängigkeiten bzw. zu installierende Bibliotheken befinden sich als `requirements.txt` im *root* Verzeichnis des Projekts.

Die Installation aller benötigter Bibliotheken geschieht mittels `pip` über den Befehl:

```bash
pip install -r requirements.txt
```

### Datenbank mongoDB

Die Datenbank, die von der Webanwendung genutzt wird, ist die dokumentenorientierte Datenbank [mongoDB](https://www.mongodb.com/). Die Datenbank läuft nicht zwingender Weise auf demselben Server wie das Backend, sondern ist extern angebunden. Für die Entwicklung ist es erforderlich, dass Entwickler eine eigene Datenbank anbinden. Es gibt mehrere Möglichkeiten, diese zu tun.

#### Docker

Eine Möglichkeit ist es, die Datenbank lokal über Docker zu hosten. Um eine lokale mongoDB zu erstellen, müssen Docker und idealerweise docker-compose installiert sein. Die compose Datei liegt im Verzeichnis *database/*. Mit dem Befehl

```bash
docker-compose up
```

wird die Datenbank gestartet. Um die Datenbank im Hintergrund zu startet, kann das Flag `-d` gesetzt werden, und um vom *root* aus zu startet kann mit `-f` ein Pfad zur Datei angegeben werden. Der Befehl zum starten der Datenbank mit docker-compose im Hingtergrund vom *root* des Projekts lautet demnach:

```bash
docker-compose -f database/docker-compose.yml up -d
```

#### Weitere Möglichkeiten

Die Dokumentation enthält weiter Möglichkeiten eine MongoDB zu hosten, z.B. die [Community-Edition](https://docs.mongodb.com/manual/administration/install-community/) von *mongoDB* direkt auf dem lokalen System zu installieren oder über [MongoDB Atlas](https://www.mongodb.com/de-de/cloud/atlas/register) eine Cloud Datenbank zu hosten.

### Projekt Konfiguration

Die Environment Variablen enthalten wichtige Informationen über die lokale Konfiguration. Sie werden in der Datei `.env` im *root* Verzeichnis des Projekts definiert. Zu setzen sind:

- `SECRET_KEY` Dies ist der Schlüssel, den Django zu Verschlüsselung nutzt. Dieser kann frei definiert werden und kann z. B. mit [djecrety.ir](https://djecrety.ir/) generiert werden.
- `DATABASE_NAME` Der Name der Datenbank, die Django in der mongoDB erstellt (beliebig).
- `DATABASE_HOST` Den Host der Datenbank. Dieser ist essenziell und hängt von der Konfiguration der Datenbank ab. Wird zur Entwicklung wir die Datenbank auf dem localhost gehostet (zb mit Docker), dann ist der Host `127.0.0.1`. Bei einer Cloud gehosteten Datenbank kann der Host über das Cloud-Dashboard eingesehen werden.
- `DATABASE_PORT` Der Port, auf dem die Datenbank läuft. MongoDB sollte i.d.R. auf dem Port `27017` laufen. Läuft die DB auf eine Cloud-Datenbank, dessen URI keinen Port enthält, dann muss diese Variable weggelassen werden.
- `DATABASE_USER` Der Username des Datenbank-Users. Bei der Nutztung von der docker-compose Datei ist dies der dort unter `MONGO_INITDB_ROOT_USERNAME` angegebene Name (deafult ist `demo`). Bei einer Cloud Datenbank muss auf Atlas ein User erzeugt werden und der name dann hier eingetragen werden.
- `DATABASE_PASS` Das Passwort des Datenbank-Users. Bei der Nutztung von der docker-compose Datei ist dies der dort unter `MONGO_INITDB_ROOT_PASSWORD` angegebene Passwort (deafult ist `passdemo`)`
- `CLOUD_DB` Diese Variable ist auf `True` zu setzten, wenn eine Cloud-Datenbank genutzt wird, wird eine lokale Datenbank genutzt, kann die Variable weggelassen werden.

Dies Wäre eine beispeilhafte `env.` Datei wenn die MongoDB mit docker-compose erzeugt wurde.
```env
DATABASE_NAME=softdsim
DATABASE_HOST=127.0.0.1
DATABASE_PORT=27017
DATABASE_USER=demo
DATABASE_PASS=mypassword
SECRET_KEY=ea2n+r$^@4px1c4gqim+l^m=@ew04hc-lupx^c&p(fy48)ma=0
```

Dies Wäre eine beispeilhafte `env.` Datei wenn die MongoDB auf mongo Atlas gehostet wird.
```env
DATABASE_NAME=softdsim
DATABASE_HOST=cluster0.wfz0m.mongodb.net
DATABASE_USER=softdsimclient
DATABASE_PASS=86umIR15Qjqwx5eN
CLOUD_DB=True
SECRET_KEY=ea2n+r$^@4px1c4gqim+l^m=@ew04hc-lupx^c&p(fy48)ma=0
```

### Erstes Starten der Webanwendung

Zum Starten der Anwendung wird der Befehl

```bash
python manage.py runserver
```

> Achtung: In dieser Readme werden alle python Aufrufe mit dem Befehl `python` beschreiben. Ja nach der Python Konfiguration auf deinem System muss dies nicht so sein, häufig verwenden MacOS oder Linux Systeme den Alias `python3`

Dann wird die Webanwendung lokal gehostet und ist unter http://127.0.0.1:8000/ zu erreichen.

Die Adresse kann im Browser geöffnet werden, dort wird nun die Login-Seite angezeigt. Um einen ersten (Super-)Nutzer zu erstellen, muss zurück in das Terminal (Eingabeaufforderung) gewechselt werden. Vor dem ersten Gebrauch muss die Datenbank, für die Speicherung von Nutzern, initialisiert werden. Dies geschieht über die zwei Befehle:

```bash
python manage.py makemigrations
python manage.py migrate
```

Danach kann ein Superuser (Nutzer mit Admin-Rechten) mit dem Befehl

```bash
python manage.py createsuperuser
```

erstellt werden. Der definierten Username und das Passwort können zur Anmeldung auf der Loginseite der Webapplikation genutzt werden.

Sollte es zu Problemen kommen kann dies mehrere Gründe haben: Datenbank läuft nicht richtig, Requirements nicht installiert bzw. falsches Python Environemt zur Ausführung genutzt oder die Konfiguration stimmt nicht. Bei Problemen einfach nachfragen. Fragen werden idealerweise direkt in unserem [GitHub Disskussionsforum](https://github.com/antonroesler/softDsim/discussions) gestellt.

## Entwicklungsworkflow

Für jedes geplante Feature, für jeden Bug, jede Idee etc. wird ein Issue angelegt und idealerweise direkt dem zugehörigen Projekt-Board zugwiesen. Die Liste der Issues ist das Backlog. Issues sollten möglichst kleinteilig geplant werden sodass ein Issue in kurzer Zeit (wenige Stunden bis 2 Tage) erledigbar ist. Sobald mit der Bearbeitung eines Issues begonnen wird, muss dieser im Projekt Board in die Spalte *In Progress* verschoben werden und diejenige Person als Assignee eingetragen werden.

### Branches

Jedes Feature wird in einem eigenen Branch bearbeitet. Das Namensschema ist wie folgt:

```
type/issuenr-kurze-beschreibung
```

wobei ```issuenr``` die Ticketnummer des Issues ist und ```type``` eines von ```feature``` (Implementierung eines neuen Features), ```fix``` (Beheben eines Bugs/Fehlers), ```refactor``` (Umschreiben des Codes ohne neue Funktionalität) oder ```task``` (Alle anderen Arbeiten) ist.  Beispiel:

```
feature/127-Adding-api-delete-endpoint
```

Wäre der passende Branchname für die Implementierung eines Features, dessen Issue die Ticketnummer 127 hat und dessen Inhalt das Hinzufügen eines API Endpoints zum Löschen von Elementen ist.

### Commits

Die Commit-Messages in einen Branch müssen ebenfalls die Issue-Nummer enthalten und haben folgendes Schema:

```
type: #issuenr Kurze Beschreibung

Und optional eine längere Erklärung nach einer Leerzeile.
```

Wichtig ist das Symbol ```#```, da dann der Commit automatisch durch GitHub zum Issue zugeteilt wird.

### Pull Requests

Sobald ein Issue gelöst wurde, wird ein Pull Request zum Mergen des Branches in den *develop* Branch erstellt. Der PR muss dann mindestens ein Approval bekommen und die Tests bestehen, um dann gemergt zu werden.

### Weitere Infos

Die Dokumentation enthält eine ausführlichere Beschreibung über den Workflow.

Außerdem gilt auch hier: Bei Fragen gerne unser [GitHub Disskussionsforum](https://github.com/antonroesler/softDsim/discussions) nutzen.  
