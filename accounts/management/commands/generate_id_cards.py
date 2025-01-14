from django.core.management.base import BaseCommand

from accounts.models import User
from accounts.utils.id_card_generator import IDCardGenerator


class Command(BaseCommand):
    help = "توليد بطاقات تعريفية للمستخدمين"

    def add_arguments(self, parser):
        parser.add_argument(
            "--role",
            help="توليد بطاقات لدور محدد (مثل: doctor, patient)",
        )
        parser.add_argument(
            "--department",
            help="توليد بطاقات لقسم محدد",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="توليد بطاقات لجميع المستخدمين",
        )

    def handle(self, *args, **options):
        # تحديد المستخدمين
        users = User.objects.all()

        if options["role"]:
            users = users.filter(role=options["role"])

        if options["department"]:
            users = users.filter(department__name=options["department"])

        if not options["all"] and not (options["role"] or options["department"]):
            self.stdout.write(
                "يرجى تحديد معايير التصفية (--role أو --department) أو استخدام --all"
            )
            return

        total = users.count()
        if total == 0:
            self.stdout.write("لم يتم العثور على مستخدمين")
            return

        self.stdout.write(f"جاري توليد {total} بطاقة تعريفية...")

        # توليد البطاقات
        results = IDCardGenerator.generate_batch(users)

        # عرض النتائج
        success = len([r for r in results if r["success"]])
        failed = len([r for r in results if not r["success"]])

        self.stdout.write(
            self.style.SUCCESS(f"اكتمل التوليد: {success} نجاح, {failed} فشل")
        )

        # عرض الأخطاء إن وجدت
        if failed > 0:
            self.stdout.write("\nالأخطاء:")
            for result in results:
                if not result["success"]:
                    self.stdout.write(
                        self.style.ERROR(f"- {result['user']}: {result['error']}")
                    )
