from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import LibraryGame, BggGame, Withdraw, Badge, Location, Supplier, StoreGame

User = get_user_model()


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'name', 'email', 'username')
        extra_kwargs = {
            'url': {'view_name': 'players', 'lookup_field': 'id'},
            'first_name': {'required': True},
            'email': {'required': True},
            'username': {'required': True}
        }

    def get_name(self, obj: User):
        return " ".join(filter(None, [obj.first_name, obj.last_name]))


class BggGameSerializer(serializers.ModelSerializer):
    badges = BadgeSerializer(many=True)

    class Meta:
        model = BggGame
        fields = (
            'bggid',
            'name',
            'rank',
            'thumbnail',
            'image',
            'min_playtime',
            'max_playtime',
            'min_players',
            'max_players',
            'badges',
            'other_names'
        )


class WithdrawBaseSerializer(serializers.ModelSerializer):
    requisitor = PlayerSerializer(read_only=True)

    class Meta:
        model = Withdraw
        fields = ('id', 'requisitor')


class LibraryGameSerializer(serializers.ModelSerializer):
    game = BggGameSerializer(read_only=True)
    owner = PlayerSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    game_id = serializers.IntegerField(write_only=True, required=True)
    owner_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="owner", required=True,
                                                  write_only=True)
    location_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), source="location", required=False,
                                                     write_only=True)
    current_withdraw = WithdrawBaseSerializer(read_only=True)

    class Meta:
        model = LibraryGame
        fields = (
            'id',
            'game',
            'game_id',
            'owner',
            'owner_id',
            'notes',
            'location',
            'location_id',
            'date_checkin',
            'date_checkout',
            'current_withdraw',
            'status',
        )


class StoreGameSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)
    game = BggGameSerializer(read_only=True)

    game_id = serializers.IntegerField(write_only=True, required=True)
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        source="supplier",
        required=True,
        write_only=True
    )

    class Meta:
        model = StoreGame
        fields = (
            'id',
            'game',
            'game_id',
            'supplier',
            'supplier_id',
            'selling_price',
            'selling_price_associate',
            'buying_price',
            'stock'
        )
        extra_kwargs = {
            'selling_price': {'required': True},
            'stock': {'required': True},
        }


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'first_name', 'last_name')

    def get_name(self, data):
        return f"{data.first_name} {data.last_name}"


class WithdrawSerializer(serializers.ModelSerializer):
    game_id = serializers.PrimaryKeyRelatedField(queryset=LibraryGame.objects.all(),
                                                 source='game',
                                                 write_only=True,
                                                 required=True)
    requisitor_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                       source="requisitor",
                                                       required=True,
                                                       write_only=True)
    requisitor = PlayerSerializer(read_only=True)
    game = LibraryGameSerializer(read_only=True)

    class Meta:
        model = Withdraw
        fields = ('id', 'requisitor', 'requisitor_id', 'game', 'game_id', 'date_withdrawn', 'date_returned')


