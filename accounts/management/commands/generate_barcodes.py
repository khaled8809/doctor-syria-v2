from django.core.management.base import BaseCommand

from accounts.models import User
from utils.barcode_generator import BarcodeGenerator


class Command(BaseCommand):
    help = "توليد الباركود لجميع المستخدمين الحاليين"

    def handle(self, *args, **kwargs):
        users = User.objects.filter(barcode="")
        total = users.count()

        if total == 0:
            self.stdout.write(self.style.SUCCESS("جميع المستخدمين لديهم باركود بالفعل"))
            return

        self.stdout.write(f"جاري توليد الباركود لـ {total} مستخدم...")

        success = 0
        failed = 0

        for user in users:
            try:
                barcode_path = BarcodeGenerator.generate_user_id_barcode(user)
                user.barcode = barcode_path
                user.save(update_fields=["barcode"])
                success += 1
                self.stdout.write(f"تم توليد باركود للمستخدم {user.username}")
            except Exception as e:
                failed += 1
                self.stdout.write(
                    self.style.ERROR(
                        f"فشل توليد باركود للمستخدم {user.username}: {str(e)}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f"اكتمل التوليد: {success} نجاح, {failed} فشل")
        )
