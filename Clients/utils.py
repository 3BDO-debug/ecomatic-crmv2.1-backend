import datetime
from dateutil.relativedelta import relativedelta


def client_device_warranty_status_updater(client_devices):
    today_date = datetime.date.today()
    for device in client_devices:

        if (
            device.installation_status == "Installed by the company"
            and today_date
            > device.installation_date
            + relativedelta(months=device.related_storage_item.warranty_coverage)
        ):
            device.in_warranty = False
            device.save()
