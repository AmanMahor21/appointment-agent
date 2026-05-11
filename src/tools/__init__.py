# Tools package init
from src.tools.booking import book_appointment
from src.tools.update import update_appointment
from src.tools.cancel import cancel_appointment
from src.tools.view import view_appointments

all_tools = [book_appointment, update_appointment,
             cancel_appointment, view_appointments]
