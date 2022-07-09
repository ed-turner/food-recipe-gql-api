from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_bulk_lazy_loader import BulkLazyLoader

BulkLazyLoader.register_loader()

Base = declarative_base()


