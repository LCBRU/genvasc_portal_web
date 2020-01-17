# GENVASC GP Portal

The GENVASC study recruits participants through the GP practices and reimburses the
practices for recruits recruited at that practice.  In order to help practices with
their administration for the study, the BRC have create a portal that contains details
of their participants, staff and reimbursements.

## Installation and Running

1. Download the code from github

```bash
git clone https://github.com/LCBRU/genvasc_portal_web.git
```

2. Install the requirements

Go to the `genvasc_portal_web` directory and type the command:

```bash
pip install -r requirements.txt
```

3. Create the development environment:

Copy the file `example.env` to `.env` and edit it with the
correct details.

4. Create the database using

staying in the `genvasc_portal_web` directory and type the command:

```bash
./manage_dev.py version_control
./manage_dev.py upgrade
```

5. Run the application

From the `genvasc_portal_web` directory type the command:

```bash
python app.py
```

6. Start Celery Worker

This application uses Celery to run background tasks.
To start Celery run the following command from the `genvasc_portal_web`
directory:

```
celery -A celery_worker.celery worker
```

7. Start Celery Beat

This application uses Celery to run background tasks.
To start Celery run the following command from the `genvasc_portal_web`
directory:

```
celery -A celery_worker.celery beat
```

# Development

### Testing

To test the application, run the following command from the project folder:

```bash
pytest
```

### Database Schema Amendments

#### Create Migration

To create a migration run the command

```bash
./manage.py script "{Description of change}"
```

You will then need to change the newly-created script created in the
`migrations` directory to make the necessary upgrade and downgrade
changes.

#### Installation

To initialise the database run the commands:

```bash
manage.py version_control
manage.py upgrade
```

#### Upgrade

To upgrade the database to the current version, run the command:

```bash
manage.py upgrade
```