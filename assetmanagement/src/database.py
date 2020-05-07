from contextlib import contextmanager

from sqlalchemy import (Boolean, CheckConstraint, Column, Date, ForeignKey,
                        Integer, String, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from definitions import ENGINE

Base = declarative_base()

class Passcode(Base):
    __tablename__ = 'passcode'

    id = Column(Integer, primary_key=True)
    salt = Column(
        String(32),
        nullable=False
    )
    key = Column(
        String(128),
        nullable=False
    )

class Borrower(Base):
    __tablename__ = 'borrower'

    id = Column(Integer, primary_key=True)
    name = Column(
        String,
        nullable=False,
        index=True,
        unique=True
    )
    is_active = Column(Boolean, nullable=False, default=True)

    loans = relationship('Loan', back_populates='borrower')

    def __repr__(self):
        return '<User(name: {}, is_active: {})>'.format(
            self.name, self.is_active)

def default_instock(context):
    return context.get_current_parameters()['total']

class Asset(Base):
    __tablename__ = 'asset'

    id = Column(Integer, primary_key=True)
    name = Column(
        String,
        nullable=False,
        index=True,
        unique=True
    )
    total = Column(
        Integer,
        CheckConstraint('total >= 0', name='check_positive'),
        nullable=False
    )
    instock = Column(
        Integer,
        CheckConstraint('instock >= 0', name='check_positive'),
        CheckConstraint('instock <= total', name='bounded_by_total'),
        nullable=False,
        default=default_instock
    )

    loans = relationship('Loan', back_populates='asset')

    def __repr__(self):
        return '<Asset(name: {}, total: {}, instock: {})>'.format(
            self.name, self.total, self.instock)

class Loan(Base):
    __tablename__ = 'loan'

    id = Column(Integer, primary_key=True)
    borrower_id = Column(Integer, ForeignKey("borrower.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("asset.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    datedue = Column(Date, nullable=False)
    is_returned = Column(Boolean, nullable=False, default=False)

    borrower = relationship('Borrower', back_populates='loans')
    asset = relationship('Asset', back_populates='loans')

    def __repr__(self):
        return ('<Loan(borrower_id: {}, asset_id: {}, quantity: {}, '
            'datedue: {}, is_returned: {})>'.format(
                self.borrower_id, self.asset_id, self.quantity,
                self.datedue, self.is_returned))

class Database:
    def __init__(self, engine=ENGINE):
        self.engine = create_engine(engine)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def get_session(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
