import datetime as dt
from pytz import timezone


def convert_my_iso_8601(iso_8601, tz_info):
    assert iso_8601[-1] == "Z"
    iso_8601 = iso_8601[:-1] + "000"
    iso_8601_dt = dt.datetime.strptime(iso_8601, "%Y-%m-%dT%H:%M:%S.%f")
    return iso_8601_dt.replace(tzinfo=timezone("UTC")).astimezone(tz_info).date()
