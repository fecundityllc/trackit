
def dedup_partner(user_id):
    from orbweaver.mongomodels import Event
    from django.utils import timezone
    from collections import defaultdict
    import json

    ACTIVE = 1
    DELETE = 3

    now = timezone.now()

    events = Event.objects(start_date_time__gt=now, user_id=user_id)
    active = events.filter(status=ACTIVE)

    data = defaultdict(list)

    for e in active:
        data[(e.name, e.start_date_time)].append(e)

    duplicates = {k: v for k, v in data.items() if len(v) > 1}

    ids = set()
    for _, duplicate_events in duplicates.items():
        remove_these = sorted(duplicate_events, key=lambda e: e.created_at)
        remove_these.pop()
        for d in remove_these:
            ids.add(d._id)

    Event.objects(_id__in=ids).update(status=DELETE)

    with open(f'{user_id}.json', 'w') as writer:
        json.dump(list(ids), writer)
