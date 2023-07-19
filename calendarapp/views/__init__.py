from .event_list import AllEventsListView, RunningEventsListView, CancelarCita ,DetalleCita
from .other_views import (
    CalendarViewNew,
    CalendarView,
    create_event,
    EventEdit,
    event_details,
    add_eventmember,
    EventMemberDeleteView,
)


__all__ = [
    AllEventsListView,
    RunningEventsListView,
    
    CancelarCita,
    CalendarViewNew,
    CalendarView,
    create_event,
    EventEdit,
    event_details,
    add_eventmember,
    EventMemberDeleteView
    ,DetalleCita,
]
