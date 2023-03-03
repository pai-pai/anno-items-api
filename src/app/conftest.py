import pytest

from mongomock import MongoClient

from app import create_app


class PyMongoMock(MongoClient):
    def init_app(self, app):
        return super().__init__()


@pytest.fixture(scope="session")
def monkeysession():
    with pytest.MonkeyPatch.context() as mp:
        yield mp


@pytest.fixture(scope="session")
def mocked_mongo(monkeysession):
    monkeysession.setattr("app.database.mongo", PyMongoMock())


#@pytest.fixture(scope="session")
#def mocked_mongo(monkeypatch):
#    monkeypatch.setattr("app.database.mongo", PyMongoMock())
#    from app.database import mongo
#    yield mongo


@pytest.fixture(scope="session")
def client(mocked_mongo):
    flask_app = create_app("mongodb://localhost:27017/test")
    with flask_app.test_client() as test_client:
        with flask_app.app_context():
            yield test_client


@pytest.fixture(scope="session")
def mongo(mocked_mongo):
    from app.database import mongo
    yield mongo
