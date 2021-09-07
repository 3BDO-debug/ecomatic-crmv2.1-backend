from . import models


def installationRequirementsFormsResetter(ticket_id, ticket_device_id):
    related_ticket = models.Ticket.objects.get(id=ticket_id)
    related_ticket_device = models.TicketDevice.objects.get(id=ticket_device_id)
    models.GasOvenInstallationRequirementsForm.objects.filter(
        related_ticket=related_ticket, related_ticket_device=related_ticket_device
    ).delete()

    models.SlimHobInstallationRequirementsForm.objects.filter(
        related_ticket=related_ticket, related_ticket_device=related_ticket_device
    ).delete()
    models.CookerInstallationRequirementsForm.objects.filter(
        related_ticket=related_ticket, related_ticket_device=related_ticket_device
    ).delete()
    models.HoodInstallationRequirementsForm.objects.filter(
        related_ticket=related_ticket, related_ticket_device=related_ticket_device
    ).delete()
    