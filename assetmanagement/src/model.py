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
