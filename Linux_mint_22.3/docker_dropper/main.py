from sqlalchemy import create_engine, LargeBinary, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
import socket
from datetime import datetime, timezone

def receive_connection(host: str, port: int) -> tuple[tuple[str, int] | None, bytes | None]:

    connection: socket.socket | None = None
    address: tuple[str, int] | None = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen(100)
        connection, address = server.accept()
        data: bytes = b''
        with connection:
            while True:
                data += bytes(connection.recv(1024))
                if not data: break
                connection.sendall(data)

    return (address, data)    

class Base(DeclarativeBase):
    pass

class DataRecord(Base):
    __tablename__ = "log"
    
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement=True)
    addr: Mapped[str] = mapped_column(String(255), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False)
    time: Mapped[str] = mapped_column(String(19), nullable=False)
    data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

def log_connection(db_path: str, address: str, incoming_port: int, current_time: datetime, incoming_data: bytes) -> None:

    engine = create_engine(f"sqlite:///{db_path}")

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        record = DataRecord(
            addr=address,
            port=incoming_port,
            time=current_time,
            data=incoming_data
        )
        session.add(record)
        session.commit()


def main() -> int:

    host: str = "127.0.0.1"
    port: int = 8080
    db_path: str = "log.db"
    addr: tuple[str, int] | None = None
    tz = timezone.utc
    time: datetime = datetime.now(tz)

    addr, data = receive_connection(host, port)

    if data is None:
        return 1

    print(f"This is data: {data!r}")

    if addr is not None:
        ip = addr[0]
        port = addr[1]
    else:
        return 1

    log_connection(db_path, ip, port, time, data)
    return 0

main()
