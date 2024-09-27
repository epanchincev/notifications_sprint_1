from handlers.notice import INotice


class Notifier:
    _handlers: dict
    _consume = False

    def __init__(self, handlers: list[INotice]):
        for handler in handlers:
            self._handlers[handler.type] = handler

    def add_handler(self, handler: INotice):
        self._handlers[handler.type] = handler

    def start(self):
        self._consume = True
        # Код чтения сообщений из очереди

    def stop(self):
        self._consume = False
