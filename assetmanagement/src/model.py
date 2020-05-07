import os
from datetime import date
from hashlib import pbkdf2_hmac

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database import (Asset, Borrower, Database, Loan,
                                          Passcode)
from observable import observable_method


class ModelError(Exception):
    pass

class Model:
    def __init__(self, database=Database()):
        self.database = database

    def new_passcode(self, passcode):
        salt = os.urandom(32)
        key = pbkdf2_hmac(
            'sha256',
            passcode.encode('utf-8'),
            salt,
            100000,
            dklen=128
        )

        with self.database.get_session() as session:
            passcode_entry = Passcode(salt=salt, key=key)
            session.add(passcode_entry)

    def exist_passcode(self):
        with self.database.get_session() as session:
            entry = session.query(Passcode.salt, Passcode.key).one_or_none()
        return entry is not None

    def confirm_passcode(self, passcode):
        with self.database.get_session() as session:
            salt, key = session.query(Passcode.salt, Passcode.key).one()
            computed_key = pbkdf2_hmac(
                'sha256',
                passcode.encode('utf-8'),
                salt,
                100000,
                dklen=128
            )
        return key == computed_key

    @observable_method()
    def add_borrower(self, name):
        '''Add borrower by name.

        Arguments:
            name (str): the name of the borrower to add.

        Returns:
            None

        Raises:
            IntegrityError: if name is duplicate.
        '''

        with self.database.get_session() as session:
            borrower = (
                session.query(Borrower)
                .filter_by(name=name, is_active=False)
                .one_or_none()
            )
            if borrower:
                borrower.is_active = True
            else:
                borrower = Borrower(name=name)
                session.add(borrower)

    @observable_method()
    def deactivate_borrower(self, name):
        '''
        Deactivate borrower by name.
        Doesn't check if the borrower is already inactive.

        Arguments:
            name (str): the name of the borrower to deactivate.

        Returns:
            None

        Raises:
            NoResultFound: if no borrower with the name exists.
            ModelError: if borrower still has active loan.
        '''

        with self.database.get_session() as session:
            borrower = (
                session.query(Borrower)
                .filter_by(name=name)
                .one()
            )
            active_loan = (
                session.query(Loan.id)
                .filter_by(borrower_id=borrower.id, is_returned=False)
                .first()
            )
            has_active_loan = active_loan is not None
            if has_active_loan:
                raise ModelError
            borrower.is_active = False

    def get_borrower_names(self, active_only=False):
        '''Get list of all borrower names sorted by name.

        Arguments:
            active_only (bool): True if want only active borrowers.

        Returns:
            list of str: borrower names.
        '''

        with self.database.get_session() as session:
            query = session.query(Borrower.name)
            if active_only:
                query = query.filter_by(is_active=True)
            query = query.order_by(Borrower.name)
            borrower_names = query.all()
        return [name for (name,) in borrower_names]

    @observable_method()
    def add_asset(self, name, quantity):
        '''
        Add quantity to asset with name.
        If it already exist, increase its total by quantity.

        Arguments:
            name (str): the name of asset to add.
            quantity (int):
                the quantity of asset to add.
                should not be negative.

        Returns:
            None

        Raises:
            ValueError: if quantity is negative.
        '''

        if quantity < 0:
            raise ValueError
        with self.database.get_session() as session:
            asset = (
                session.query(Asset)
                .filter_by(name=name)
                .one_or_none()
            )
            if asset:
                asset.total += quantity
                asset.instock += quantity
            else:
                asset = Asset(name=name, total=quantity)
                session.add(asset)

    @observable_method()
    def remove_asset(self, name, quantity=None):
        '''Remove quantity from asset with name.

        Arguments:
            name (str): the name of asset to remove.
            quantity (int):
                the quantity of asset to remove.
                should not be negative.
                set to None if intend to remove all.

        Returns:
            None

        Raises:
            ValueError: if quantity is negative.
            NoResultFound: if no asset with name exists.
            IntegrityError:
                if remove by quantity results in negative total or instock.
        '''

        if quantity is not None and quantity < 0:
            raise ValueError
        with self.database.get_session() as session:
            asset = (
                session.query(Asset)
                .filter_by(name=name)
                .one()
            )
            if quantity is None:
                quantity = asset.total
            asset.total -= quantity
            asset.instock -= quantity

    def modify_asset_instock(self, name, delta):
        '''Modify instock of asset with name.

        Arguments:
            name (str): the name of asset to remove.
            delta (int): the instock quantity of asset to modify.

        Returns:
            None

        Raises:
            NoResultFound: if no asset with name exists.
            IntegrityError:
                if modify by delta results in negative instock.
        '''

        with self.database.get_session() as session:
            asset = (
                session.query(Asset)
                .filter_by(name=name)
                .one()
            )
            asset.instock += delta

    def get_asset(self, name):
        '''Get asset by name.

        Arguments:
            name (str): the name of asset.

        Returns:
            tuple: (name, total, instock)

        Raises:
            NoResultFound: if no asset with name exists.
        '''

        with self.database.get_session() as session:
            asset = (
                session.query(Asset.name, Asset.total, Asset.instock)
                .filter_by(name=name)
                .one()
            )
        return asset

    def get_assets(self, active_only=False, instock_only=False):
        '''Get list of all assets sorted by name.

        Arguments:
            active_only (bool):
                True if want only assets with positive total.
            instock_only (bool):
                True if want only assets with positive instock.

        Returns:
            list of tuple: (name, total, instock)

        '''

        with self.database.get_session() as session:
            query = session.query(Asset.name, Asset.total, Asset.instock)
            if active_only:
                query = query.filter(Asset.total > 0)
            if instock_only:
                query = query.filter(Asset.instock > 0)
            query = query.order_by(Asset.name)
            assets = query.all()
        return assets

    @observable_method()
    def borrow_asset(self, borrower_name, asset_name, quantity, datedue):
        '''Borrower borrows an asset by quantity and must return by datedue.

        Arguments:
            borrower_name (str): the name of the borrower.
            asset_name (str): the name of the asset to borrow.
            quantity (int): the quantity of the asset to borrow. positive.
            datedue (date): the date when borrower has to return asset.

        Returns:
            None

        Raises:
            ValueError: if quantity is not positive.
            NoResultFound:
                if no borrower or asset with corresponding name exist.
            IntegrityError: if not enough asset instock to borrow.
        '''

        if quantity <= 0:
            raise ValueError
        with self.database.get_session() as session:
            borrower = (
                session.query(Borrower)
                .filter_by(name=borrower_name)
                .one()
            )
            asset = (
                session.query(Asset)
                .filter_by(name=asset_name)
                .one()
            )
            loan = Loan(
                borrower_id=borrower.id,
                asset_id=asset.id,
                quantity=quantity,
                datedue=datedue,
            )
            session.add(loan)
            asset.instock -= quantity

    @observable_method()
    def return_asset(self, borrower_name, asset_name):
        '''
        Borrower returns asset. Quantity could not be specified.
        Borrower must return all of them at once.

        Arguments:
            borrower_name (str): the name of the borrower.
            asset_name (str): the name of the asset to return.

        Returns:
            None

        Raises:
            NoResultFound:
                if no borrower or asset with corresponding name exist.
                if no such loan exist.
        '''

        with self.database.get_session() as session:
            borrower = (
                session.query(Borrower)
                .filter_by(name=borrower_name)
                .one()
            )
            asset = (
                session.query(Asset)
                .filter_by(name=asset_name)
                .one()
            )
            loans = (
                session.query(Loan)
                .filter_by(
                    borrower_id=borrower.id,
                    asset_id=asset.id,
                    is_returned=False
                )
                .all()
            )
            if not loans:
                raise NoResultFound
            for loan in loans:
                loan.is_returned = True
                asset.instock += loan.quantity

    def get_loans(self, borrower_name=None, asset_name=None,
            active_only=False, overdue_only=False):
        '''Get list of all loans (presumably sorted by insert time).

        Arguments:
            borrower_name (str): the name of the borrower. None means all.
            asset_name (str): the name of the asset. None means all.
            active_only (bool): True if want only loans that are not returned.
            instock_only (bool):
                True if want only loans that are overdue and not returned.
                For ease of use, setting this argument to True automatically
                sets active_only to True.

        Returns:
            list of tuple:
                (borrower_name, asset_name, quantity, datedue, is_returned)
        '''
        if overdue_only:
            active_only = True

        with self.database.get_session() as session:
            query = (
                session.query(
                    Borrower.name,
                    Asset.name,
                    Loan.quantity,
                    Loan.datedue,
                    Loan.is_returned
                )
                .join(Borrower)
                .join(Asset)
            )
            if borrower_name is not None:
                # 'is not None' should not be omitted because name can be ''
                query = query.filter(Borrower.name == borrower_name)
            if asset_name is not None:
                query = query.filter(Asset.name == asset_name)
            if active_only:
                query = query.filter(Loan.is_returned == False)
            if overdue_only:
                query = query.filter(Loan.datedue < date.today())
            loans = query.all()
        return loans
