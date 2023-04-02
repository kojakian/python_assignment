# Take-Home Assignment - Solution proposed

Task 1 : 

- A script will get the data from the last two weeks of IBM and Apple stocks and store them in an SQLite database. This is the Table format :

```
    id, symbol, date, open_price, close_price, volume
```

The API key must be added by replacing the text in the file apikey.txt

Task 2 :

- I chose FastAPI as it's light and quick to setup, as I don't need a framework such as Flask or Django for such a small project.

Dockerize : 

- I set a Docker container with an entrypoint that will copy the current data and populate the database with the latest data available. 

To build and run here what need to be typed :   

```
docker build -t myfinancial .
docker-compose up
```

The API can be accessed through the address http://127.0.0.1:8888

Examples :

```
http://127.0.0.1:8888/api/financial_data?start_date=2023-03-31&end_date=2023-03-20
http://127.0.0.1:8888/api/statistics?start_date=2023-03-31&end_date=2023-03-20
```