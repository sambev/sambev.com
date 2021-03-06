# This is just a default settings file that the repo tracks so you can have a
# good example of what it should look like.  Make your own real settings.py
# in this same directory (git will ignore it)
SETTINGS = {
    'dev': {
        'DB_URI': 'mongodb://localhost:27017',
        'DB_NAME': 'reports',
        'REPORT_COLLECTION': 'snapshots',
        'SLEEP_COLLECTION': 'sleepapp',
        'DEBUG': True,
        'SECRET_KEY': 'make this super secret'
    },

    'test': {
        'DB_URI': 'mongodb://localhost:27017',
        'DB_NAME': 'reports_test',
        'REPORT_COLLECTION': 'snapshots',
        'SLEEP_COLLECTION': 'sleepapp',
        'DEBUG': True
    },

    'production': {
        # NEVER EVER TRACK PRODUCTION SETTINGS
        # DO NOT FILL THIS OUT SEE TOP COMMENT
    }
}
