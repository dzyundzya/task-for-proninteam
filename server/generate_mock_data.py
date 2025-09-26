# flake8: noqa
# mypy: ignore-errors
# ruff: noqa
from typing import Any
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from server.apps.users.models import CustomUser
from server.apps.collects.models import Collect
from server.apps.payments.models import Payment
from server.apps.collects.choices import OccasionType


class Command(BaseCommand):
    help = 'Generate mock data for the application (several thousand records)'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=100,
            help='Number of users to create (default: 100)',
        )
        parser.add_argument(
            '--collects',
            type=int,
            default=500,
            help='Number of collects to create (default: 500)',
        )
        parser.add_argument(
            '--payments',
            type=int,
            default=3000,
            help='Number of payments to create (default: 3000)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before generation',
        )

    def handle(self, *args: Any, **options: Any) -> None:
        fake = Faker('ru_RU')
        users_count = options['users']
        collects_count = options['collects']
        payments_count = options['payments']
        
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Payment.objects.all().delete()
            Collect.objects.all().delete()
            CustomUser.objects.all().delete()
        
        self.stdout.write(f'Generating {users_count} users...')
        users = self._create_users(fake, users_count)
        
        self.stdout.write(f'Generating {collects_count} collects...')
        collects = self._create_collects(fake, collects_count, users)
        
        self.stdout.write(f'Generating {payments_count} payments...')
        self._create_payments(fake, payments_count, users, collects)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated: '
                f'{CustomUser.objects.count()} users, '
                f'{Collect.objects.count()} collects, '
                f'{Payment.objects.count()} payments'
            )
        )

    def _create_users(self, fake: Faker, count: int) -> list[CustomUser]:
        users = []
        for i in range(count):
            user = CustomUser.objects.create(
                username=fake.user_name() + str(i),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_active=True,
            )
            user.set_password('testpass123')
            user.save()
            users.append(user)
            
            if i % 100 == 0:
                self.stdout.write(f'Created {i} users...')
        
        return users

    def _create_collects(self, fake: Faker, count: int, users: list[CustomUser]) -> list[Collect]:
        collects = []
        occasions = [choice[0] for choice in OccasionType.choices]
        
        for i in range(count):
            author = fake.random_element(users)
            collect = Collect.objects.create(
                author=author,
                title=fake.sentence(nb_words=4)[:100],
                occasion=fake.random_element(occasions),
                description=fake.text(max_nb_chars=500),
                planned_amount=(
                    Decimal(fake.random_number(digits=4, fix_len=False)) 
                    if fake.boolean(chance_of_getting_true=70) else None
                ),
                end_date=(
                    timezone.now() + timezone.timedelta(days=fake.random_int(1, 365))
                    if fake.boolean(chance_of_getting_true=60) else None
                ),
                is_active=fake.boolean(chance_of_getting_true=90),
            )
            collects.append(collect)
            
            if i % 100 == 0:
                self.stdout.write(f'Created {i} collects...')
        
        return collects

    def _create_payments(
        self, 
        fake: Faker, 
        count: int, 
        users: list[CustomUser], 
        collects: list[Collect]
    ) -> None:
        for i in range(count):
            user = fake.random_element(users)
            collect = fake.random_element(collects)
            
            Payment.objects.create(
                user=user,
                collect=collect,
                amount=Decimal(fake.random_number(digits=3, fix_len=False)),
                comment=fake.sentence() if fake.boolean(chance_of_getting_true=50) else '',
                paid=fake.boolean(chance_of_getting_true=80),
                payment_day=(
                    timezone.now() - timezone.timedelta(days=fake.random_int(0, 30))
                    if fake.boolean(chance_of_getting_true=70) else None
                ),
            )
            
            if i % 500 == 0:
                self.stdout.write(f'Created {i} payments...')
                
            if i % 100 == 0:
                from server.apps.collects.services import CollectAmountService
                CollectAmountService.update_collect_amounts(collect)
