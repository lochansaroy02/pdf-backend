from sqlalchemy import MetaData
from app.database import Base, engine

def reset_table():
    # Create a MetaData instance and reflect the current database state
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Drop the pdf_documents table if it exists
    if 'pdf_documents' in metadata.tables:
        metadata.tables['pdf_documents'].drop(engine)
        print("Dropped existing pdf_documents table.")

    # Recreate all tables (including pdf_documents) with the latest schema
    Base.metadata.create_all(bind=engine)
    print("Recreated the tables with the latest schema.")

if __name__ == "__main__":
    reset_table()
