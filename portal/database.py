import os
import datetime
import time
from portal import db, app
import traceback
from multiprocessing import Lock


dbUpgradeDir = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'db_upgrade'
)
lock = Lock()


def init_db():
    app.logger.info('initialising DB')
    app.logger.info(
        'Connection string: {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))

    wait_for_db()

    with lock:
        db.engine.execute("""
            CREATE TABLE IF NOT EXISTS db_version (
                id INT AUTO_INCREMENT,
                version INT,
                appliedDate DATETIME,
                PRIMARY KEY(id)
            );
            """)

        currentVersion = db.engine.execute(
            "SELECT MAX(version) maxVersion FROM db_version"
        ).fetchall()[0][0] or 0

        app.logger.info('Upgrading DB from version %d' % currentVersion)

        upgradeScripts = [f for f in os.listdir(dbUpgradeDir)
                          if f.split('.')[0].isdigit() and
                          f.split('.')[1] == 'sql' and
                          os.path.isfile(os.path.join(dbUpgradeDir, f)) and
                          int(f.split('.')[0]) > currentVersion]

        upgradeScripts.sort(key=lambda s: int(s.split('.')[0]))

        for f in upgradeScripts:
            app.logger.info('Running DB script %s' % f)

            with open(os.path.join(dbUpgradeDir, f)) as s:
                try:
                    curUpdate = db.engine.raw_connection().cursor()
                    curUpdate.execute(
                        "START TRANSACTION;\n" + s.read() + "\nCOMMIT; ")
                    curUpdate.close()

                    db.engine.execute(
                        "INSERT INTO db_version (version, appliedDate)"
                        "VALUES (%s, %s)",
                        [int(f.split('.')[0]), datetime.datetime.now()])
                except Exception:
                    app.logger.error(traceback.format_exc())
                    db.engine.raw_connection().cursor().execute("ROLLBACK;")
                    raise


def wait_for_db():
    dbfound = False

    while not dbfound:
        try:
            dbfound = True
        except Exception as e:
            app.logger.warning('Could not connect to db: {}'.format(str(e)))

        time.sleep(5)
