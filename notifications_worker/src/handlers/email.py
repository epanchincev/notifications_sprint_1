from notice import INotice, NotificationType


class EmailNotice(INotice):
    type = NotificationType.email.value

    def verify(self):
        pass
