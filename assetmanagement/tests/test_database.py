from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from assetmanagement.src.database import Asset, Borrower, Database, Loan

ENGINE = 'sqlite:///:memory:'

def test_create_database():
    Database(ENGINE)

def test_add_borrower():
    database = Database(ENGINE)
    session = database.Session()

    borrower = Borrower(name='Amy')
    session.add(borrower)
    query_borrower = session.query(Borrower).filter_by(name='Amy').one()

    assert(repr(borrower) == '<User(name: Amy, is_active: True)>')
    assert(query_borrower == borrower)
    assert(borrower.id == 1)
    assert(borrower.is_active == True)
    assert(borrower.loans == [])

def test_borrower_name_empty():
    database = Database(ENGINE)
    session = database.Session()

    borrower = Borrower(name='')
    session.add(borrower)
    session.commit()

    assert(session.query(Borrower).count() == 1)

def test_borrower_name_chinese():
    database = Database(ENGINE)
    session = database.Session()

    borrower = Borrower(name='美')
    session.add(borrower)
    session.commit()

    assert(repr(borrower) == '<User(name: 美, is_active: True)>')
    assert(borrower.id == 1)
    assert(borrower.is_active == True)
    assert(borrower.loans == [])

def test_borrower_unique():
    database = Database(ENGINE)
    session = database.Session()

    borrower1 = Borrower(name='Amy')
    borrower2 = Borrower(name='Amy')
    session.add(borrower1)
    session.add(borrower2)
    with pytest.raises(IntegrityError):
        session.commit()

def test_add_asset_total_positive():
    database = Database(ENGINE)
    session = database.Session()

    test_quantity = 10
    asset = Asset(name='Pen', total=test_quantity)
    session.add(asset)
    query_asset = session.query(Asset).filter_by(name='Pen').one()

    assert(repr(query_asset) == '<Asset(name: Pen, total: {}, instock: {})>'.\
        format(test_quantity, test_quantity))
    assert(query_asset == asset)
    assert(asset.id == 1)
    assert(asset.total == test_quantity)
    assert(asset.instock == test_quantity)
    assert(asset.loans == [])

def test_add_asset_total_zero():
    database = Database(ENGINE)
    session = database.Session()

    test_quantity = 0
    asset = Asset(name='Pen', total=test_quantity)
    session.add(asset)
    query_asset = session.query(Asset).filter_by(name='Pen').one()

    assert(repr(query_asset) == '<Asset(name: Pen, total: {}, instock: {})>'.\
        format(test_quantity, test_quantity))
    assert(query_asset == asset)
    assert(asset.id == 1)
    assert(asset.total == test_quantity)
    assert(asset.instock == test_quantity)
    assert(asset.loans == [])

def test_add_asset_total_negative():
    database = Database(ENGINE)
    session = database.Session()

    with pytest.raises(IntegrityError):
        asset = Asset(name='Pen', total=-1)
        session.add(asset)
        session.commit()

def test_asset_name_empty():
    database = Database(ENGINE)
    session = database.Session()

    asset = Asset(name='', total=10)
    session.add(asset)
    session.commit()

    assert(session.query(Asset).count() == 1)

def test_asset_unique():
    database = Database(ENGINE)
    session = database.Session()

    asset1 = Asset(name='Pen', total=5)
    asset2 = Asset(name='Pen', total=5)
    session.add(asset1)
    session.add(asset2)
    with pytest.raises(IntegrityError):
        session.commit()

def test_rollback():
    database = Database(ENGINE)
    session = database.Session()

    init_asset = Asset(name='Pencil', total=20)
    session.add(init_asset)
    session.commit()

    try:
        asset = Asset(name='Pen', total=10)
        session.add(asset)
        asset = Asset(name='Marker', total=-1)
        session.add(asset)
        session.commit()
    except IntegrityError:
        session.rollback()
    assert(session.query(Asset).all() == [init_asset])

def setup_for_add_loan(session):
    borrowers = [
        Borrower(name='Amy'),
        Borrower(name='Bob'),
        Borrower(name='Cindy')
    ]
    assets = [
        Asset(name='Pencil', total=10),
        Asset(name='Pen', total=10),
        Asset(name='Marker', total=10)
    ]
    session.add_all(borrowers+assets)
    session.commit()

def test_setup_for_add_loan():
    database = Database(ENGINE)
    session = database.Session()
    setup_for_add_loan(session)

    assert(session.query(Borrower).count() == 3)
    assert(session.query(Asset).count() == 3)

def test_add_loan():
    database = Database(ENGINE)
    session = database.Session()
    setup_for_add_loan(session)

    datedue = datetime.strptime('2020-02-10', '%Y-%m-%d').date()
    loan = Loan(borrower_id=1, asset_id=1, quantity=5, datedue=datedue)
    session.add(loan)

    assert(loan.id == None)
    assert(loan.borrower == None)
    assert(loan.asset == None)
    assert(loan.borrower_id == 1)
    assert(loan.asset_id == 1)
    assert(loan.quantity == 5)
    assert(loan.datedue == datedue)
    assert(loan.is_returned == None)

    borrower = session.query(Borrower).get(1)
    asset = session.query(Asset).get(1)
    session.commit()

    assert(loan.id == 1)
    assert(loan.borrower == borrower)
    assert(loan.asset == asset)
    assert(loan.is_returned == False)
    assert(repr(loan) == ('<Loan(borrower_id: 1, asset_id: 1, quantity: 5, '
        'datedue: 2020-02-10, is_returned: False)>'))
    assert(borrower.loans == [loan])
    assert(asset.loans == [loan])

def setup_for_delete(session):
    setup_for_add_loan(session)
    datedue = datetime.strptime('2020-02-10', '%Y-%m-%d').date()
    loans = [
        Loan(borrower_id=1, asset_id=1, quantity=2, datedue=datedue),
        Loan(borrower_id=1, asset_id=2, quantity=2, datedue=datedue),
        Loan(borrower_id=1, asset_id=3, quantity=2, datedue=datedue),
        Loan(borrower_id=2, asset_id=1, quantity=2, datedue=datedue),
        Loan(borrower_id=2, asset_id=3, quantity=2, datedue=datedue),
        Loan(borrower_id=3, asset_id=1, quantity=2, datedue=datedue),
        Loan(borrower_id=3, asset_id=2, quantity=2, datedue=datedue),
    ]
    session.add_all(loans)
    session.commit()

def test_setup_for_delete():
    database = Database(ENGINE)
    session = database.Session()
    setup_for_delete(session)

    assert(session.query(Loan).count() == 7)
    assert(len(session.query(Borrower).get(1).loans) == 3)
    assert(len(session.query(Asset).get(2).loans) == 2)

def test_delete_borrower_with_loan():
    database = Database(ENGINE)
    session = database.Session()
    setup_for_delete(session)

    borrower = session.query(Borrower).get(1)

    with pytest.raises(IntegrityError):
        session.delete(borrower)
        session.commit()

def test_delete_asset_with_loan():
    database = Database(ENGINE)
    session = database.Session()
    setup_for_delete(session)

    asset = session.query(Asset).get(1)

    with pytest.raises(IntegrityError):
        session.delete(asset)
        session.commit()

def test_delete_loan():
    database = Database(ENGINE)
    session = database.Session()
    setup_for_delete(session)

    for loan in session.query(Loan).filter_by(borrower_id=1).all():
        session.delete(loan)
    session.commit()

    assert(session.query(Loan).filter_by(borrower_id=1).count() == 0)
    assert(session.query(Loan).count() == 4)
    assert(session.query(Borrower).get(1).loans == [])

def test_delete_borrower_without_loan():
    database = Database(ENGINE)
    session = database.Session()
    setup_for_delete(session)

    for loan in session.query(Loan).filter_by(borrower_id=1).all():
        session.delete(loan)

    borrower = session.query(Borrower).get(1)
    session.delete(borrower)
    session.commit()

    assert(session.query(Borrower).count() == 2)

def test_database_get_session():
    database = Database(ENGINE)

    with database.get_session() as session:
        borrower = Borrower(name='Amy')
        session.add(borrower)

    with database.get_session() as session:
        query_borrower = session.query(Borrower).filter_by(name='Amy').one()
        assert(repr(query_borrower) == '<User(name: Amy, is_active: True)>')
        assert(query_borrower.id == 1)
        assert(query_borrower.is_active == True)
        assert(query_borrower.loans == [])

    with pytest.raises(IntegrityError):
        with database.get_session() as session:
            another_borrower = Borrower(name='Bob')
            session.add(another_borrower)
            duplicate_borrower = Borrower(name='Amy')
            session.add(duplicate_borrower)

    with database.get_session() as session:
        assert(session.query(Borrower).count() == 1)
