# Foosh
Учеба без голода!
Не трать время на очереди - заказывай еду онлайн!

# Prod
Load cities from fixtures:

```bash
python manage.py cities_light_fixtures load --base-url file:fixtures/cities_light/
```

To dump, use:

```bash
python manage.py cities_light_fixtures dump
```

And copy result from `venv/Lib/site-packages/cities_light/data/fixtures/` to `fixtures/cities_light/`.
