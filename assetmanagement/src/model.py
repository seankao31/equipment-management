from datetime import date, datetime, timedelta

from sqlalchemy.exc import IntegrityError

from assetmanagement.src.database import Asset, Borrower, Database, Loan

class Model:
    def __init__(self, database=Database()):
        self.database = database

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
            borrower = Borrower(name=name)
            session.add(borrower)

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
        '''

        with self.database.get_session() as session:
            borrower = (
                session.query(Borrower)
                .filter_by(name=name)
                .one()
            )
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

        if quantity and quantity < 0: # quantiy == 0 is allowed
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