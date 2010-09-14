from mail.models import Message


def main():
    print 'Running send_email script...'
    messages = Message.objects.to_be_sent()
    print '  Found %d messages to send.' % len(messages)
    for message in messages:
        sent = message.send()
        if sent:
            print '  Message %d: Sent successfully.' % message.pk
        else:
            print '  Message %d: Error sending! See its logs for more details.' % message.pk
    print 'Finished running send_email script.'

if __name__ == '__main__':
    main()
