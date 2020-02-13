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
