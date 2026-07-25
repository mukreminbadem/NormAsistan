from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base, Alan

engine = create_engine(
    "sqlite:///data/normasistan.db",
    echo=False
)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def alanlari_getir():
    session = Session()

    alanlar = (
        session.query(Alan)
        .filter(Alan.aktif == True)
        .order_by(Alan.alan_adi)
        .all()
    )

    session.close()

    return alanlar
def alan_ekle(alan_adi):
    session = Session()

    alan = Alan(
        alan_adi=alan_adi,
        aktif=True
    )

    session.add(alan)
    session.commit()
    session.close()