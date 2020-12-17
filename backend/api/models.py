from django.db import models
from datetime import timedelta, datetime
from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField


class Badge(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = PhoneNumberField(blank=True, null=True, default=None)
    email = models.EmailField(blank=True, null=True, default=None)
    website = models.CharField(blank=True, null=True, default=None, max_length=200)


class Location(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=100, default=None)
    email = models.EmailField(default=None, unique=True)
    username = models.CharField(max_length=100, default=None, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

    @staticmethod
    def most_withdraws(number):
        return Withdraw.objects.all().values('requisitor__name').annotate(total=Count('requisitor')).order_by('-total')[
               :number]

    def num_games_owned(self):
        return self.librarygame_set.count()


class BggGame(models.Model):
    bggid = models.CharField(max_length=300, primary_key=True)
    name = models.CharField(max_length=300)

    badges = models.ManyToManyField(Badge, blank=True, default=None)

    rank = models.IntegerField(null=True)
    min_players = models.IntegerField(null=True)
    max_players = models.IntegerField(null=True)
    min_playtime = models.IntegerField(null=True)
    max_playtime = models.IntegerField(null=True)
    thumbnail = models.CharField(blank=True, max_length=500, default='')
    image = models.CharField(blank=True, max_length=500)

    @staticmethod
    def most_withdraws(number):
        return Withdraw.objects.all().values('game__game__name', 'game__game__image').annotate(
            total=Count('game')).order_by('-total')[:number]

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Game(models.Model):
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)

    game = models.ForeignKey(BggGame, null=True, blank=True, on_delete=models.CASCADE)

    notes = models.TextField(blank=True)
    date_checkin = models.DateTimeField(default=None, blank=True, null=True)
    date_checkout = models.DateTimeField(default=None, blank=True, null=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"%s" % self.name


class LibraryGame(Game):
    location = models.ForeignKey(Location, null=True, blank=True, default=None, on_delete=models.CASCADE)

    def status(self):
        if not self.location or self.date_checkin is None:
            return 'not-checked-in'
        elif self.date_checkout is not None:
            return 'checked-out'
        elif self.withdraw_set.filter(date_returned=None).count() == 0:
            return 'available'
        else:
            return 'not-available'

    def current_withdraw(self):
        if self.status() == "not-available":
            return self.withdraw_set.filter(date_returned=None).first()
        else:
            return None

    def save(self, *args, **kwargs):
        if self.location:
            self.date_checkin = timezone.now()

        super(LibraryGame, self).save()


class UsedGame(Game):
    price = models.FloatField(default=0.0, blank=False, null=False)


class Withdraw(models.Model):
    requisitor = models.ForeignKey(Player, on_delete=models.CASCADE, default=None)
    game = models.ForeignKey(LibraryGame, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    date_withdrawn = models.DateTimeField(auto_now_add=True)
    date_returned = models.DateTimeField(default=None, blank=True, null=True)

    def returned(self):
        return self.date_returned is not None

    returned.boolean = True

    def __unicode__(self):
        return u"%s with %s" % (self.game.name, self.requisitor.name)

    def __str__(self):
        return u"%s with %s" % (self.game.name, self.requisitor.name)

    @staticmethod
    def last(days):

        items = Withdraw.objects.filter(date_withdrawn__range=(datetime.now() - timedelta(days=days), datetime.now())) \
            .extra({'date_withdrawn': "date(date_withdrawn)"}) \
            .values('date_withdrawn') \
            .annotate(created_count=Count('id'))

        items = list(items)

        dates = [x.get('date_withdrawn') for x in items]

        for d in (datetime.today() - timedelta(days=x) for x in range(0, days)):
            if d.date().isoformat() not in dates:
                items.append({'date_withdrawn': d.date().isoformat(), 'created_count': 0})

        items.sort(key=lambda o: o['date_withdrawn'])
        return items
