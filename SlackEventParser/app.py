from SlackHelper import BussedSlackEvent


def lambda_handler(event, context):
    # Parse the raw event payload with the SlackEvent Class
    cur_SlackEvent = BussedSlackEvent(event)
    return cur_SlackEvent.body
