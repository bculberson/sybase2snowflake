import pyodbc
import json
import gzip
import sys, os


DSN=sys.argv[1]
DATABASE=sys.argv[2]
TABLE=sys.argv[3]
FOLDER=sys.argv[4]


def write_data(data, dataChunk):
    filename = f"{FOLDER}/{DSN}.{DATABASE}.{TABLE}_{dataChunk}.json.gz"
    path = os.path.abspath(f"{filename}")
    with gzip.open(path, 'wt', encoding="ascii") as zipfile:
        json.dump(data, zipfile)
    print(path)


conn = pyodbc.connect("DSN=DEVART_ASE", timeout=1)
conn.autocommit = True
cursor = conn.cursor()
cursor.execute(f"USE {DATABASE}")
cursor.execute(f"SELECT * FROM {TABLE}")
data = []
dataChunkSize = 0
dataChunk = 0
while True:
    result = cursor.fetchmany(1000)
    if not result:
        write_data(data, dataChunk)
        break
    for row in result:
        data.append(list(row))
        dataChunkSize = dataChunkSize + sys.getsizeof(row)
    if dataChunkSize > 1e8:
        write_data(data, dataChunk)
        data = []
        dataChunkSize = 0
        dataChunk = dataChunk + 1
cursor.close()
conn.close()

