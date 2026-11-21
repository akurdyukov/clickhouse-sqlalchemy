ClickHouse SQLAlchemy
=====================

ClickHouse dialect for SQLAlchemy to `ClickHouse database <https://clickhouse.com/>`_.

This is ``clickhouse-sqlalchemy-ng``, a maintained fork of
`clickhouse-sqlalchemy <https://github.com/xzkostyan/clickhouse-sqlalchemy>`_
by Konstantin Lebedev, which has had no release since 0.3.2. It keeps the
``clickhouse_sqlalchemy`` import name and the ``clickhouse://`` URL schemes,
so it is a drop-in replacement.


.. image:: https://img.shields.io/pypi/v/clickhouse-sqlalchemy-ng.svg
    :target: https://pypi.org/project/clickhouse-sqlalchemy-ng

.. image:: https://coveralls.io/repos/github/akurdyukov/clickhouse-sqlalchemy/badge.svg?branch=master
    :target: https://coveralls.io/github/akurdyukov/clickhouse-sqlalchemy?branch=master

.. image:: https://img.shields.io/pypi/l/clickhouse-sqlalchemy-ng.svg
    :target: https://pypi.org/project/clickhouse-sqlalchemy-ng

.. image:: https://img.shields.io/pypi/pyversions/clickhouse-sqlalchemy-ng.svg
    :target: https://pypi.org/project/clickhouse-sqlalchemy-ng

.. image:: https://img.shields.io/pypi/dm/clickhouse-sqlalchemy-ng.svg
    :target: https://pypi.org/project/clickhouse-sqlalchemy-ng

.. image:: https://github.com/akurdyukov/clickhouse-sqlalchemy/actions/workflows/actions.yml/badge.svg
   :target: https://github.com/akurdyukov/clickhouse-sqlalchemy/actions/workflows/actions.yml


Installation
============

    .. code-block:: bash

        pip install clickhouse-sqlalchemy-ng

Both packages install the same ``clickhouse_sqlalchemy`` module, so uninstall
the original first: ``pip uninstall clickhouse-sqlalchemy``.


Documentation
=============

Documentation of the original project is available at
https://clickhouse-sqlalchemy.readthedocs.io and applies to this fork; see
`CHANGELOG.md <https://github.com/akurdyukov/clickhouse-sqlalchemy/blob/master/CHANGELOG.md>`_ for what changed since 0.3.2.


Usage
=====

Supported interfaces:

- **native** [recommended] (TCP) via `clickhouse-driver <https://github.com/mymarilyn/clickhouse-driver>`
- **async native** (TCP) via `asynch <https://github.com/long2ice/asynch>`
- **http** via requests

Define table

    .. code-block:: python

        from sqlalchemy import create_engine, Column, MetaData

        from clickhouse_sqlalchemy import (
            Table, make_session, get_declarative_base, types, engines
        )

        uri = 'clickhouse+native://localhost/default'

        engine = create_engine(uri)
        session = make_session(engine)
        metadata = MetaData(bind=engine)

        Base = get_declarative_base(metadata=metadata)

        class Rate(Base):
            day = Column(types.Date, primary_key=True)
            value = Column(types.Int32)

            __table_args__ = (
                engines.Memory(),
            )

        Rate.__table__.create()


Insert some data

    .. code-block:: python

        from datetime import date, timedelta

        from sqlalchemy import func

        today = date.today()
        rates = [
            {'day': today - timedelta(i), 'value': 200 - i}
            for i in range(100)
        ]


And query inserted data

    .. code-block:: python

        session.execute(Rate.__table__.insert(), rates)

        session.query(func.count(Rate.day)) \
            .filter(Rate.day > today - timedelta(20)) \
            .scalar()


License
=======

ClickHouse SQLAlchemy is distributed under the `MIT license
<http://www.opensource.org/licenses/mit-license.php>`_.
