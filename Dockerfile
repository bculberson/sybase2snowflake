FROM python:3

WORKDIR /usr/src/app

COPY devartodbcase_amd64.deb /usr/src/app/devartodbcase_amd64.deb
RUN apt-get -qq update && \
    apt-get install -qq netcat unixodbc unixodbc-dev && \
    apt install -y /usr/src/app/devartodbcase_amd64.deb

RUN sed -i 's/^Database=$/Database=master/' /etc/odbc.ini && \
    sed -i 's/^User ID=$/User ID=sa/' /etc/odbc.ini && \
    sed -i 's/^Password=$/Password=password/' /etc/odbc.ini && \
    sed -i 's/^Data Source=$/Server=dksybase/' /etc/odbc.ini && \
    echo "Port=5000" >> /etc/odbc.ini

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["sh", "./start_test.sh"]

