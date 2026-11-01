from django.http import JsonResponse

from personnel.models import City


def cities_by_province(request):
    province_id = request.GET.get("province_id")

    if not province_id:
        return JsonResponse([], safe=False)

    cities = City.objects.filter(
        province_id=province_id
    ).order_by("name")

    data = [
        {
            "id": city.id,
            "name": city.name,
        }
        for city in cities
    ]

    return JsonResponse(data, safe=False)