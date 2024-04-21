# Foosh
Учеба без голода!
Не трать время на очереди - заказывай еду онлайн!

## Prod

[Install Python](https://www.python.org/downloads/), copy the repo, setup the venv and install requirements:

```bash
git clone https://gitlab.crja72.ru/django/2024/spring/course/projects/team-4.git
cd team-4
python -m venv venv
source venv/bin/activate
pip install -r requirements/prod.txt
```

Load cities from fixtures:

```bash
python manage.py cities_light_fixtures load --base-url file:fixtures/cities_light/
```

**Setup a test YooKassa shop**. Follow the instruction: https://yookassa.ru/docs/support/merchant/payments/implement/test-store. Then, set the corresponding variables in .env file: `YOOKASSA_SHOP_ID` and `YOOKASSA_API_KEY`. `YOOKASSA_SUCCESS_URL` is going to be `your_domen/cart/success`. Also, add your domen to `DJANGO_ALLOWED_HOSTS`.

Run the server:

```bash
python manage.py runserver
```

## Dev

Setup everything like in Prod section, but install dev requirements:

```bash
pip install -r requirements/dev.txt
```

To use YooKassa, firstly, setup ngrok and pass the URL to `DJANGO_ALLOWED_HOSTS` in .env file. Also, define the `YOOKASSA_SUCCESS_URL`, it's going to be `your_ngrok_url/cart/success`.

And have a good time!

- To dump cities, use:

```bash
python manage.py cities_light_fixtures dump
```

And copy result from `venv/Lib/site-packages/cities_light/data/fixtures/` to `fixtures/cities_light/`.

## Test

Setup everything like in Dev section, but install test requirements:

```bash
pip install -r requirements/test.txt
```

To run the tests:

```bash
python manage.py test
```

To check linting and code style *(run this command from the root of the project)*:

```bash
flake8 .
```
