import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.requests import Request

from apps.services.repository import WmsRepository

logger = logging.getLogger(__name__)


class TransactionalGraphQLContext(dict):
    """Context that manages a single transaction across all resolvers"""

    def __init__(self, request: Request, session: Session):
        super().__init__()
        self.request = request
        self.session = session
        self.repository = WmsRepository(session)
        self._transaction_active = False
        self._committed = False
        self._rolled_back = False

    def __enter__(self):
        """Start transaction when entering context"""
        self.session.begin_nested()
        self._transaction_active = True
        logger.debug("Transaction started for GraphQL request")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Handle transaction completion"""
        try:
            if exc_type is not None:
                # Exception occurred, rollback
                self.rollback()
                logger.error(f"Transaction rolled back due to exception: {exc_val}")
            elif not self._committed and not self._rolled_back:
                # No exception and not manually handled, commit
                self.commit()
                logger.debug("Transaction committed successfully")
        finally:
            self._cleanup()

    def commit(self):
        """Manually commit the transaction"""
        if self._transaction_active and not self._committed:
            try:
                self.session.commit()
                self._committed = True
                self._transaction_active = False
                logger.debug("Transaction committed manually")
            except SQLAlchemyError as e:
                logger.error(f"Error committing transaction: {e}")
                self.rollback()
                raise

    def rollback(self):
        """Manually rollback the transaction"""
        if self._transaction_active and not self._rolled_back:
            try:
                self.session.rollback()
                self._rolled_back = True
                self._transaction_active = False
                logger.debug("Transaction rolled back manually")
            except SQLAlchemyError as e:
                logger.error(f"Error rolling back transaction: {e}")

    def _cleanup(self):
        """Clean up resources"""
        try:
            if self._transaction_active:
                self.session.rollback()
            self.session.close()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
