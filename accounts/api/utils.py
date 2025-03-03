import threading
from django.core.mail import send_mail


class EmailSenderThread(threading.Thread):
    def __init__(self, email_object):
        """
        :param email_object: یک شیء که حاوی اطلاعات ایمیل است.
        """
        self.email_object = email_object
        super().__init__()

    def run(self):
        """
        متد اصلی اجرای Thread که ایمیل را ارسال می‌کند.
        """
        self.email_object.send()
