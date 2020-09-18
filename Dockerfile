FROM lambci/lambda:build-python3.8
RUN yum install -y postgresql-devel python-psycopg2 postgresql-libs