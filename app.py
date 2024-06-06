from aiohttp import web
import caldav
from icalendar import Calendar, Event
import logging

logging.basicConfig(level=logging.DEBUG)
routes = web.RouteTableDef()


def export_calendar(uri, username, password):
    export_cal = Calendar()
    export_cal.add('prodid', '-//Mozilla.org/NONSGML Mozilla Calendar V1.1//EN')
    export_cal.add('version', '2.0')

    # Use a breakpoint in the code line below to debug your script.
    client = caldav.DAVClient(uri, username=username, password=password)
    principal = client.principal()
    import_calendar = principal.calendars()[0]
    events = import_calendar.events()
    logging.log(f'Calendar {uri} has {len(events)} events.')
    for import_event in import_calendar.events():
        export_event = Event()
        for subcomponent in import_event.icalendar_instance.subcomponents:
            export_cal.add_component(subcomponent)
    return export_cal.to_ical()


@routes.get('/')
async def hello(request):
    caldav_uri = request.rel_url.query.get('uri', None)
    caldav_usr = request.rel_url.query.get('usr', None)
    caldav_pwd = request.rel_url.query.get('pwd', None)
    return web.Response(body=export_calendar(caldav_uri, caldav_usr, caldav_pwd))

app = web.Application()
app.add_routes(routes)
web.run_app(app)