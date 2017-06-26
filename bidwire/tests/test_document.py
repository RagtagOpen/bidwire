import pytest

from document import Document, get_doc_count_per_site
import db

from . import common
from . import factories


class TestDocument():
    def test_validates_url_is_absolute(self):
        with pytest.raises(AssertionError) as exception_info:
            factories.DocumentFactory(url="/some-href")
        assert "absolute" in str(exception_info.value)

    def test_get_doc_count_per_site(self):
	# Make sure the database contains at least one bid for each Site
        [factories.DocumentFactory(site=s.name) for s in Document.Site]
        count_dict = get_doc_count_per_site(self.session)
        for site in Document.Site:
            assert site in count_dict
            assert count_dict[site] > 0

    @classmethod
    def setup_class(self):
        self.session = common.Session()

    @classmethod
    def teardown_class(self):
        common.Session.remove()
