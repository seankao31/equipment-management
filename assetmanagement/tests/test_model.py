import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from assetmanagement.src.database import Asset, Borrower, Database, Loan
from assetmanagement.src.model import Model

ENGINE = 'sqlite:///:memory:'

def setup():
    database = Database(ENGINE)
    model = Model(database)
    return database, model

def test_create_model():
    setup()

def test_add_borrower():
    database, model = setup()

    model.add_borrower(name='Amy')

    with database.get_session() as session:
        assert(session.query(Borrower).count() == 1)
        borrower = session.query(Borrower).filter_by(name='Amy').one()
        assert(borrower.id == 1)
        assert(borrower.is_active == True)
        assert(borrower.loans == [])

def test_add_borrower_name_empty():
    database, model = setup()

    model.add_borrower(name='')

    with database.get_session() as session:
        assert(session.query(Borrower).count() == 1)
        borrower = session.query(Borrower).filter_by(name='').one()
        assert(borrower.id == 1)
        assert(borrower.is_active == True)
        assert(borrower.loans == [])

def test_add_duplicate_borrower():
    database, model = setup()

    model.add_borrower(name='Amy')
    with pytest.raises(IntegrityError):
        model.add_borrower(name='Amy')

    with database.get_session() as session:
        assert(session.query(Borrower).count() == 1)

def test_deactivate_borrower():
    database, model = setup()

    model.add_borrower(name='Amy')
    model.deactivate_borrower(name='Amy')

    with database.get_session() as session:
        assert(session.query(Borrower.is_active).filter_by(name='Amy').one()
            == (False,))

def test_deactivate_inactive_borrower():
    database, model = setup()

    model.add_borrower(name='Amy')
    model.deactivate_borrower(name='Amy')
    model.deactivate_borrower(name='Amy')

    with database.get_session() as session:
        assert(session.query(Borrower.is_active).filter_by(name='Amy').one()
            == (False,))

def test_deactivate_nonexistent_borrower():
    _, model = setup()

    with pytest.raises(NoResultFound):
        model.deactivate_borrower(name='Amy')


def setup_pre_add_borrowers(database):
    borrowers = [
        Borrower(name='Amy'),
        Borrower(name='Bob'),
        Borrower(name='Cindy'),
    ]
    with database.get_session() as session:
        session.add_all(borrowers)

def test_get_borrower_names():
    database, model = setup()
    setup_pre_add_borrowers(database)

    borrower_names = model.get_borrower_names()
    assert(borrower_names == ['Amy', 'Bob', 'Cindy'])

def test_get_borrower_names_empty_table():
    _, model = setup()
    borrower_names = model.get_borrower_names()
    assert(not borrower_names)

def test_get_active_borrower_names():
    database, model = setup()
    setup_pre_add_borrowers(database)

    model.deactivate_borrower('Bob')
    borrower_names = model.get_borrower_names(active_only=True)
    assert(borrower_names == ['Amy', 'Cindy'])
