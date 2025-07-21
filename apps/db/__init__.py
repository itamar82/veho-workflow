from sqlalchemy import Engine, create_engine

engine: Engine = create_engine("sqlite+pysqlite:///wms.db", echo=True)
