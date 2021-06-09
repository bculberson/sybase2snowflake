#!/usr/bin/env python
import snowflake.connector
import sys, os


ACCOUNT=sys.argv[1]
USERNAME=sys.argv[2]
PASSWORD=sys.argv[3]
if len(sys.argv) > 4:
    DELETE=sys.argv[4]
else:
    DELETE="NODELETE"

ctx = snowflake.connector.connect(
    user=USERNAME,
    password=PASSWORD,
    account=ACCOUNT
    )
cs = ctx.cursor()
for filename in sys.stdin:
    filename = filename.rstrip()
    print(f"Adding file {filename} to user's internal stage\n")
    cs.execute(f"PUT file://{filename} @~ OVERWRITE=TRUE")
    if DELETE == "DELETE":
        print(f"Deleting file {filename}\n")
        os.unlink(filename)
cs.close()
ctx.close()
