FROM python:3.6-slim
RUN mkdir /eCommProject
WORKDIR /eCommProject
ADD . /eCommProject
RUN pip install -r requirement.txt
EXPOSE 9000
CMD python manage.py runserver 0:9000

 
