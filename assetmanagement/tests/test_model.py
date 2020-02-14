from datetime import date, datetime, timedelta

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

    model.deactivate_borrower(name='Bob')
    borrower_names = model.get_borrower_names(active_only=True)
    assert(borrower_names == ['Amy', 'Cindy'])

def test_add_asset():
    database, model = setup()

    model.add_asset(name='Pen', quantity=10)

    with database.get_session() as session:
        assert(session.query(Asset).count() == 1)
        asset = session.query(Asset).filter_by(name='Pen').one()
        assert(asset.id == 1)
        assert(asset.total == 10)
        assert(asset.instock == 10)
        assert(asset.loans == [])

def test_add_asset_name_empty():
    database, model = setup()

    model.add_asset(name='', quantity=10)

    with database.get_session() as session:
        assert(session.query(Asset).count() == 1)
        asset = session.query(Asset).filter_by(name='').one()
        assert(asset.id == 1)
        assert(asset.total == 10)
        assert(asset.instock == 10)
        assert(asset.loans == [])

def test_add_asset_quantity_zero():
    database, model = setup()

    model.add_asset(name='Pen', quantity=0)

    with database.get_session() as session:
        assert(session.query(Asset).count() == 1)
        asset = session.query(Asset).filter_by(name='Pen').one()
        assert(asset.id == 1)
        assert(asset.total == 0)
        assert(asset.instock == 0)
        assert(asset.loans == [])

def test_add_asset_quantity_negative():
    database, model = setup()

    with pytest.raises(ValueError):
        model.add_asset(name='Pen', quantity=-1)

    with database.get_session() as session:
        assert(session.query(Asset).count() == 0)

def test_add_asset_exist():
    database, model = setup()

    model.add_asset(name='Pen', quantity=10)
    model.add_asset(name='Pen', quantity=5)

    with database.get_session() as session:
        assert(session.query(Asset).count() == 1)
        asset = session.query(Asset).filter_by(name='Pen').one()
        assert(asset.id == 1)
        assert(asset.total == 15)
        assert(asset.instock == 15)
        assert(asset.loans == [])

def test_remove_asset():
    database, model = setup()

    model.add_asset(name='Pen', quantity=10)
    model.remove_asset(name='Pen', quantity=3)

    with database.get_session() as session:
        assert(session.query(Asset).count() == 1)
        asset = session.query(Asset).filter_by(name='Pen').one()
        assert(asset.id == 1)
        assert(asset.total == 7)
        assert(asset.instock == 7)
        assert(asset.loans == [])

def test_remove_asset_all():
    database, model = setup()

    model.add_asset(name='Pen', quantity=10)
    model.remove_asset(name='Pen')

    with database.get_session() as session:
        assert(session.query(Asset).count() == 1)
        asset = session.query(Asset).filter_by(name='Pen').one()
        assert(asset.id == 1)
        assert(asset.total == 0)
        assert(asset.instock == 0)
        assert(asset.loans == [])

def test_remove_asset_quantity_zero():
    database, model = setup()

    model.add_asset(name='Pen', quantity=10)
    model.remove_asset(name='Pen', quantity=0)

    with database.get_session() as session:
        assert(session.query(Asset).count() == 1)
        asset = session.query(Asset).filter_by(name='Pen').one()
        assert(asset.id == 1)
        assert(asset.total == 10)
        assert(asset.instock == 10)
        assert(asset.loans == [])

def test_remove_asset_quantity_negative():
    database, model = setup()

    model.add_asset(name='Pen', quantity=10)
    with pytest.raises(ValueError):
        model.remove_asset(name='Pen', quantity=-1)

    with database.get_session() as session:
        assert(session.query(Asset).count() == 1)
        asset = session.query(Asset).filter_by(name='Pen').one()
        assert(asset.id == 1)
        assert(asset.total == 10)
        assert(asset.instock == 10)
        assert(asset.loans == [])

def test_remove_asset_nonexist():
    _, model = setup()

    with pytest.raises(NoResultFound):
        model.remove_asset(name='Pen', quantity=5)

def test_remove_asset_too_much():
    database, model = setup()

    model.add_asset(name='Pen', quantity=10)
    with pytest.raises(IntegrityError):
        model.remove_asset(name='Pen', quantity=11)

    with database.get_session() as session:
        assert(session.query(Asset).count() == 1)
        asset = session.query(Asset).filter_by(name='Pen').one()
        assert(asset.id == 1)
        assert(asset.total == 10)
        assert(asset.instock == 10)
        assert(asset.loans == [])

def test_modify_asset_instock():
    database, model = setup()

    model.add_asset(name='Pen', quantity=10)
    model.modify_asset_instock(name='Pen', delta=-5)

    with database.get_session() as session:
        assert(session.query(Asset).count() == 1)
        asset = session.query(Asset).filter_by(name='Pen').one()
        assert(asset.id == 1)
        assert(asset.total == 10)
        assert(asset.instock == 5)
        assert(asset.loans == [])

    model.modify_asset_instock(name='Pen', delta=3)

    with database.get_session() as session:
        assert(session.query(Asset).count() == 1)
        asset = session.query(Asset).filter_by(name='Pen').one()
        assert(asset.id == 1)
        assert(asset.total == 10)
        assert(asset.instock == 8)
        assert(asset.loans == [])

    model.modify_asset_instock(name='Pen', delta=0)

    with database.get_session() as session:
        assert(session.query(Asset).count() == 1)
        asset = session.query(Asset).filter_by(name='Pen').one()
        assert(asset.id == 1)
        assert(asset.total == 10)
        assert(asset.instock == 8)
        assert(asset.loans == [])


def test_modify_asset_instock_nonexist():
    _, model = setup()

    with pytest.raises(NoResultFound):
        model.modify_asset_instock(name='Pen', delta=5)

def test_modify_asset_instock_add_too_much():
    database, model = setup()

    model.add_asset(name='Pen', quantity=10)
    with pytest.raises(IntegrityError):
        model.modify_asset_instock(name='Pen', delta=1)

    with database.get_session() as session:
        assert(session.query(Asset).count() == 1)
        asset = session.query(Asset).filter_by(name='Pen').one()
        assert(asset.id == 1)
        assert(asset.total == 10)
        assert(asset.instock == 10)
        assert(asset.loans == [])

def test_modify_asset_instock_remove_too_much():
    database, model = setup()

    model.add_asset(name='Pen', quantity=10)
    with pytest.raises(IntegrityError):
        model.modify_asset_instock(name='Pen', delta=-11)

    with database.get_session() as session:
        assert(session.query(Asset).count() == 1)
        asset = session.query(Asset).filter_by(name='Pen').one()
        assert(asset.id == 1)
        assert(asset.total == 10)
        assert(asset.instock == 10)
        assert(asset.loans == [])

def setup_pre_add_assets(database):
    assets = [
        Asset(name='Pen', total=10),
        Asset(name='Marker', total=5)
    ]

    with database.get_session() as session:
        session.add_all(assets)

def test_get_assets():
    database, model = setup()
    setup_pre_add_assets(database)

    assets = model.get_assets()
    assert(assets == [('Marker', 5, 5), ('Pen', 10, 10)])

def test_get_assets_empty_table():
    _, model = setup()
    assets = model.get_assets()
    assert(not assets)

def test_get_active_assets():
    database, model = setup()
    setup_pre_add_assets(database)

    model.remove_asset(name='Pen')
    assets = model.get_assets(active_only=True)
    assert(assets == [('Marker', 5, 5)])

def test_get_instock_assets():
    database, model = setup()
    setup_pre_add_assets(database)

    model.modify_asset_instock(name='Pen', delta=-7)
    model.modify_asset_instock(name='Marker', delta=-5)
    assets = model.get_assets(instock_only=True)
    assert(assets == [('Pen', 10, 3)])

def setup_for_loan(database):
    setup_pre_add_borrowers(database)
    setup_pre_add_assets(database)

TODAY = date.today()
PREV_DAY = TODAY - timedelta(days=1)
NEXT_DAY = TODAY + timedelta(days=1)

def test_borrow_asset():
    database, model = setup()
    setup_for_loan(database)

    model.borrow_asset(
        borrower_name='Amy',
        asset_name='Pen',
        quantity=2,
        datedue=NEXT_DAY
    )

    with database.get_session() as session:
        assert(session.query(Loan).count() == 1)
        loan = session.query(Loan).one()
        assert(loan.id == 1)
        assert(loan.borrower_id == 1)
        assert(loan.asset_id == 1)
        assert(loan.quantity == 2)
        assert(loan.datedue == NEXT_DAY)
        assert(loan.is_returned == False)
        borrower = loan.borrower
        assert(borrower.id == 1)
        assert(borrower.name == 'Amy')
        assert(borrower.loans == [loan])
        asset = loan.asset
        assert(asset.id == 1)
        assert(asset.name == 'Pen')
        assert(asset.total == 10)
        assert(asset.instock == 8)
        assert(asset.loans == [loan])

def test_borrow_asset_quantity_not_positive():
    database, model = setup()
    setup_for_loan(database)

    with pytest.raises(ValueError):
        model.borrow_asset(
            borrower_name='Amy',
            asset_name='Pen',
            quantity=0,
            datedue=NEXT_DAY
        )

    with pytest.raises(ValueError):
        model.borrow_asset(
            borrower_name='Amy',
            asset_name='Pen',
            quantity=-1,
            datedue=NEXT_DAY
        )

def test_borrow_asset_no_result():
    database, model = setup()
    setup_for_loan(database)

    with pytest.raises(NoResultFound):
        model.borrow_asset(
            borrower_name='Dio',
            asset_name='Pen',
            quantity=2,
            datedue=NEXT_DAY
        )

    with pytest.raises(NoResultFound):
        model.borrow_asset(
            borrower_name='Amy',
            asset_name='Pencil',
            quantity=2,
            datedue=NEXT_DAY
        )

def test_borrow_asset_not_enough():
    database, model = setup()
    setup_for_loan(database)

    with pytest.raises(IntegrityError):
        model.borrow_asset(
            borrower_name='Amy',
            asset_name='Pen',
            quantity=11,
            datedue=NEXT_DAY
        )

    with database.get_session() as session:
        assert(session.query(Loan).count() == 0)

def setup_for_return(model):
    model.borrow_asset(
        borrower_name='Amy',
        asset_name='Pen',
        quantity=3,
        datedue=NEXT_DAY
    )
    model.borrow_asset(
        borrower_name='Amy',
        asset_name='Marker',
        quantity=1,
        datedue=NEXT_DAY
    )
    model.borrow_asset(
        borrower_name='Amy',
        asset_name='Pen',
        quantity=5,
        datedue=NEXT_DAY
    )
    model.borrow_asset(
        borrower_name='Bob',
        asset_name='Marker',
        quantity=2,
        datedue=NEXT_DAY
    )

def test_return_asset_1():
    database, model = setup()
    setup_for_loan(database)
    setup_for_return(model)

    model.return_asset(borrower_name='Amy', asset_name='Pen')
    with database.get_session() as session:
        returned_loans_count = (
            session.query(Loan)
            .filter_by(is_returned=True)
            .count()
        )
        assert(returned_loans_count == 2)
        borrower = session.query(Borrower).filter_by(name='Amy').one()
        asset = session.query(Asset).filter_by(name='Pen').one()
        loans = (
            session.query(Loan)
            .filter_by(borrower_id=borrower.id, asset_id=asset.id)
            .all()
        )
        for loan in loans:
            assert(loan.is_returned == True)
        assert(asset.total == 10)
        assert(asset.instock == 10)

def test_return_asset_2():
    database, model = setup()
    setup_for_loan(database)
    setup_for_return(model)

    model.return_asset(borrower_name='Bob', asset_name='Marker')
    with database.get_session() as session:
        returned_loans_count = (
            session.query(Loan)
            .filter_by(is_returned=True)
            .count()
        )
        assert(returned_loans_count == 1)
        borrower = session.query(Borrower).filter_by(name='Bob').one()
        asset = session.query(Asset).filter_by(name='Marker').one()
        loans = (
            session.query(Loan)
            .filter_by(borrower_id=borrower.id, asset_id=asset.id)
            .all()
        )
        for loan in loans:
            assert(loan.is_returned == True)
        assert(asset.total == 5)
        assert(asset.instock == 4)

def test_return_asset_no_result():
    database, model = setup()
    setup_for_loan(database)
    setup_for_return(model)

    with pytest.raises(NoResultFound):
        model.return_asset(borrower_name='Dio', asset_name='Pen')

    with pytest.raises(NoResultFound):
        model.return_asset(borrower_name='Amy', asset_name='Pencil')

    with pytest.raises(NoResultFound):
        model.return_asset(borrower_name='Bob', asset_name='Pen')

    with database.get_session() as session:
        returned_loans_count = (
            session.query(Loan)
            .filter_by(is_returned=True)
            .count()
        )
        assert(returned_loans_count == 0)

def test_borrow_return_borrow_return():
    database, model = setup()

    model.add_borrower(name='Amy')
    model.add_asset(name='Pen', quantity=10)
    model.borrow_asset(
        borrower_name='Amy',
        asset_name='Pen',
        quantity=3,
        datedue=NEXT_DAY
    )
    model.return_asset(borrower_name='Amy', asset_name='Pen')
    model.borrow_asset(
        borrower_name='Amy',
        asset_name='Pen',
        quantity=5,
        datedue=NEXT_DAY
    )
    with database.get_session() as session:
        asset_instock = (
            session.query(Asset.instock)
            .filter_by(name='Pen')
            .one()
        )
        assert(asset_instock == (5, ))
    model.return_asset(borrower_name='Amy', asset_name='Pen')
    with database.get_session() as session:
        asset_instock = (
            session.query(Asset.instock)
            .filter_by(name='Pen')
            .one()
        )
        assert(asset_instock == (10, ))

def setup_pre_borrow_return(model):
    model.borrow_asset(
        borrower_name='Amy',
        asset_name='Pen',
        quantity=3,
        datedue=PREV_DAY
    )
    model.borrow_asset(
        borrower_name='Bob',
        asset_name='Pen',
        quantity=2,
        datedue=PREV_DAY
    )
    model.borrow_asset(
        borrower_name='Bob',
        asset_name='Marker',
        quantity=2,
        datedue=PREV_DAY
    )
    model.borrow_asset(
        borrower_name='Cindy',
        asset_name='Pen',
        quantity=4,
        datedue=NEXT_DAY
    )
    model.borrow_asset(
        borrower_name='Cindy',
        asset_name='Marker',
        quantity=1,
        datedue=NEXT_DAY
    )
    model.return_asset(borrower_name='Amy', asset_name='Pen')
    model.borrow_asset(
        borrower_name='Amy',
        asset_name='Pen',
        quantity=3,
        datedue=NEXT_DAY
    )

def test_get_loans():
    database, model = setup()
    setup_for_loan(database)
    setup_pre_borrow_return(model)
    loans_all = model.get_loans()
    assert(len(loans_all) == 6)
    loans_active = model.get_loans(active_only=True)
    assert(len(loans_active) == 5)
    loans_overdue = model.get_loans(overdue_only=True)
    assert(len(loans_overdue) == 2)
    loans_cindy = model.get_loans(borrower_name='Cindy')
    assert(len(loans_cindy) == 2)
    loans_marker = model.get_loans(asset_name='Marker')
    assert(len(loans_marker) == 2)
    loans_pen_overdue = model.get_loans(asset_name='Pen', overdue_only=True)
    assert(len(loans_pen_overdue) == 1)
