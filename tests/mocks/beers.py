import pytest
from app import models, helpers


@pytest.yield_fixture(scope='function')
def mock_beer():
    """Returns a function (clojure) to create a mock.
    """

    beer = None

    def make_mock_beer(name=None, password=None, role=None):
        """The real mock. Creates a object beers.models.Beer .All parameters
        are optionals, by default uses the beer name 'Samuel Adams',

        :username: a string object.
        :password: a string object
        :role: a string object
        :returns: an users.models.User object

        """

        # nonlocal user

        beer = models.Beer(
            name=name or 'Samuel Adams',
            active=True
        ).save()

        return beer

    yield make_mock_beer

    beer.delete() if beer else None
