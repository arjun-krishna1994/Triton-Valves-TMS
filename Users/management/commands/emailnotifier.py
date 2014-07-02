from django.core.management.base import NoArgsCommand, make_option
class Command(NoArgsCommand):

    help = "Django Emailer"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        import datetime
        from django.core.mail import send_mail
        from Users.userfunctions import ScheduleMessages
        from django.template.loader import get_template
        from django.template.context import Context
        from django.core.mail.message import EmailMessage
        t = get_template('emailTemplate.html')
        today = datetime.datetime.today()
        tomorrow = today + datetime.timedelta(1)
        day_after = tomorrow + datetime.timedelta(1)
        today_messages = ScheduleMessages(today.month,today.year).get_message_for_day(today.day)
        tomorrow_messages = ScheduleMessages(tomorrow.month,tomorrow.year).get_message_for_day(tomorrow.day)
        day_after_messages = ScheduleMessages(day_after.month,day_after.year).get_message_for_day(day_after.day)
        #stri = "Tasks:- \n Today's:" + "\n" + today_messages + "\n" + "Tomorrow:" + "\n" + tomorrow_messages + " Day After: "  + "\n" + day_after_messages
        c = Context({'today':today , 'tomorrow':tomorrow , 'day_after':day_after})
        msg = EmailMessage(subject = "Daily Notifications" , body = t.render(c), from_email ='arjun.krishna1994@gmail.com', to = ['arjun.krishna1994@gmail.com'])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        exit()
