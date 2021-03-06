from sqlalchemy import Column, String, BigInteger, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

association_table = Table(
    "association",
    Base.metadata,
    Column("product_id", BigInteger, ForeignKey("product.id")),
    Column("store_id", BigInteger, ForeignKey("store.id")),
)


class Product(Base):
    """product table."""
    __tablename__ = "product"
    id = Column(BigInteger, primary_key=True)
    category = relationship("Category", back_populates="products")
    history = relationship("History", back_populates="products")
    stores = relationship(
        "Store", secondary=association_table, back_populates="products"
    )
    category_id = Column(BigInteger, ForeignKey("category.id"))
    history_id = Column(BigInteger, ForeignKey("history.id"))
    brands = Column(String(150))
    product_name = Column(String(150))
    nutriscore_fr = Column(String(1))
    quantity = Column(String(5))
    product_url = Column(String(155))


class Store(Base):
    """store table."""
    __tablename__ = "store"
    id = Column(BigInteger, primary_key=True)
    products = relationship(
        "Product", secondary=association_table, back_populates="stores"
    )
    store_name = Column(String(155))


class Category(Base):
    """category table."""
    __tablename__ = "category"
    id = Column(BigInteger, primary_key=True)
    products = relationship("Product", back_populates="category")
    category_name = Column(String(155))


class History(Base):
    """history table."""
    __tablename__ = "history"
    id = Column(BigInteger, primary_key=True,)
    products = relationship("Product", back_populates="history")
