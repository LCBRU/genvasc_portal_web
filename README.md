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

3. Create the database using

Create an empty database and database user:

4. Create the development environment:

Copy the file `example.dev.env` to `dev.env` and edit it with the
correct details.

4. Run the application

From the `genvasc_portal_web` directory type the command:

```bash
./dev.sh
```
