from unittest.mock import Mock
import pytest
import sqlalchemy
import sendgrid

import db
from bid import Bid
from debug_email import DebugEmail

from . import common
from . import factories


class TestDebugEmail:
    def test_send_debug_email(self):
        # Make a few bids and also stick them in the database
        bids_dict = {
            Bid.Site.COMMBUYS: [factories.BidFactory() for i in range(3)],
            Bid.Site.CITYOFBOSTON: [factories.BidFactory() for i in
                                    range(2)]
        }

        mock_sg = Mock()
        de = DebugEmail(mock_sg, db_session=self.session)
        recipient_email = "seekret.email@resist.now"
        config_used = {
            Bid.Site.COMMBUYS: {'recipients': [recipient_email]},
            Bid.Site.CITYOFBOSTON: {'recipients': [recipient_email]}
        }
        de.send(bids_dict, config_used, 90)

        # Verify that Sendgrid was called with correct-looking content
        _, kwargs = mock_sg.client.mail.send.post.call_args
        assert 'request_body' in kwargs
        request_body = kwargs['request_body']
        actual_content = request_body['content'][0]['value']
        # The plain-text recipient email is not in the body
        assert recipient_email not in actual_content
        # The elapsed time is correctly converted to mins and secs
        assert '1m 30sec' in actual_content

    @classmethod
    def setup_class(self):
        common.Session.configure(bind=db.engine)
        self.session = common.Session()

    @classmethod
    def teardown_class(self):
        common.Session.remove()
