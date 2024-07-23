from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment


class Command(BaseCommand):
    def handle(self, *args, **options):
        payment_list = [
            {
                "paid_lesson": Lesson.objects.get(id=2),
                "payment_type": "",
                "amount": "15000",
            },
            {
                "paid_lesson": Lesson.objects.get(id=3),
                "payment_type": "by_cash",
                "amount": "1200",
            },
            {
                "paid_course": Course.objects.get(id=2),
                "payment_type": "",
                "amount": "25000",
            },
        ]

        payment_for_create = []
        for payment in payment_list:
            payment_for_create.append(Payment(**payment))

        Payment.objects.bulk_create(payment_for_create)
