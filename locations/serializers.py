from rest_framework import serializers
from iranian_cities.models import Ostan, Shahrestan
from .models import Address


class CitySerializer(serializers.ModelSerializer):
    # serializer for all cities
    class Meta:
        model = Shahrestan
        fields = "__all__"


class ProvinceWithCitiesSerializer(serializers.ModelSerializer):
    # serialize all provinces with their cities
    cities = serializers.SerializerMethodField()

    class Meta:
        model = Ostan
        fields = ["id", "amar_code", "name", "cities"]

    def get_cities(self, obj) -> list:
        # This will return all cities belonging to the province
        cities = Shahrestan.objects.filter(ostan=obj)
        return CitySerializer(cities, many=True).data


class AddressSerializer(serializers.ModelSerializer):
    province_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    id = serializers.IntegerField(read_only=True)  # make id just readable
    # user = serializers.IntegerField(read_only=True)   # make user just readable

    class Meta:
        model = Address
        fields = [
            "id",
            "title",
            "phone_number",
            "user",
            "province",
            "province_name",
            "city",
            "city_name",
            "postal_code",
            "street",
            "address",
        ]

    def get_province_name(self, obj) -> str:
        return obj.province.name

    def get_city_name(self, obj) -> str:
        return obj.city.name

    def validate(self, data):
        province = data.get("province")
        city = data.get("city")

        # Check if the city belongs to the selected province
        if not Shahrestan.objects.filter(id=city.id, ostan=province).exists():
            raise serializers.ValidationError(
                {"city": "The selected city does not belong to the selected province."}
            )
        return data
