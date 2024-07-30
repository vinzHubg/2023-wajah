
from database.Connection import Connection


class Context:

    def __init__(self, connection: Connection) -> None:
        self.__connection = connection

    def get_connectin(self) -> Connection:
        return self.__connection
