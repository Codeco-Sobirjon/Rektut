def filter_by_title(queryset, request):
    title = request.query_params.get("title", '')
    if title:
        queryset = queryset.filter(
            Q(company__title__icontains=title)
        )
    return queryset


def filter_by_category(queryset, request):
    category = request.query_params.get("category", [])
    if category:
        ids_category = [int(id_str) for id_str in category.split(",")]
        queryset = queryset.filter(Q(job_category__in=ids_category))
    return queryset


def filter_by_city(queryset, request):
    city = request.query_params.get("city", [])
    if city:
        ids_city = [int(id_str) for id_str in city.split(",")]
        queryset = queryset.filter(Q(job_city__in=ids_city))
    return queryset


def filter_is_top_ads(queryset, request):
    is_top = request.query_params.get('isTop', 'False').lower() == 'true'
    action_map = {
        True: lambda qs: qs.filter(is_pop=True),
        False: lambda qs: qs
    }
    return action_map[is_top](queryset)


def filter_is_pop_ads(queryset, request):
    is_pop = request.query_params.get('isPop', 'False').lower() == 'true'
    action_map = {
        True: lambda qs: qs.filter(is_pop=True),
        False: lambda qs: qs
    }
    return action_map[is_pop](queryset)