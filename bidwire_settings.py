import os

POSTGRES_ENDPOINT = os.environ.get('POSTGRES_ENDPOINT', 'localhost')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')


def get_recipients_list():
    # The env variable should contain a comma-separated recipient list.
    recipients_str = os.environ.get('EMAIL_RECIPIENTS',
                                    'bidwire-logs@googlegroups.com')
    # Split into array of strings and strip whitespace.
    return [r.strip() for r in recipients_str.split(',')]


# List of e-mail recipients. Array of e-mail addresses.
EMAIL_RECIPIENTS = get_recipients_list()
