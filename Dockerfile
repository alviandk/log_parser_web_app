FROM python:3.6.1

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add app
ADD . /usr/src/app

# db migration
CMD python manage.py db migrate
CMD python manage.py db upgrade

CMD python manage.py init_db

# run server
CMD python manage.py runserver -h 0.0.0.0

