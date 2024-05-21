from slack_sdk import WebClient
from AWSHelper import get_aws_parameter


def experiment_modal(client, triggerid, request_type):
    client.views_open(trigger_id=triggerid, view={
        "title": {
            "type": "plain_text",
            "text": "Request Generator"
        },
        "submit": {
            "type": "plain_text",
            "text": "Request"
        },
        "type": "modal",
        "close": {
            "type": "plain_text",
            "text": "Cancel"
        },
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "What is the title for your " + request_type.replace('_', ' ') + " request?"
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "request_title"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Title"
                }
            }
        ]
    })
    return


def lambda_handler(event, context):
    groSlackTeamID = get_aws_parameter(param_name='groSlackTeamID')
    # Confirm that the event came from a GRO Biosciences Slack account
    if event.get('team_id') == groSlackTeamID:
        # non-button event and matches GRO ID
        # AWS EventBridge will bus the event to the next StepFunction
        return {
            'statusCode': 200
        }
    else:
        # button event and it matches GRO ID
        # The button click may require a rapid modal response, so the following conditionals will assess if actions
        # need to be taken in this Lambda or can wait for the next StepFunction.
        if event.get('user').get('team_id') == groSlackTeamID:
            # Decode and extract slack_event
            slack_event = event
            # Moved modal kickoffs to inside the first lambda function to prevent expiring Slack trigger_ids
            if slack_event['type'] == 'block_actions':
                # Get event triggerid to enable app actions
                triggerid = slack_event['trigger_id']
                buttontype = slack_event['actions'][0]['text']['text']
                if buttontype == 'Request':
                    # Retrieve Slack bot token for the FoundryRequests Slack app from AWS Systems Manager Parameter
                    # Store.
                    slack_token = get_aws_parameter(param_name='/slackBotTokens/FoundryRequests')
                    # Initiate Slack WebClient, and create a pop-up modal
                    client = WebClient(token=slack_token)
                    # Modal content is dependent on which Slack button was clicked
                    request_type = event.get('actions')[0].get('value')
                    experiment_modal(client=client, triggerid=triggerid,
                                     request_type=request_type)
                    # Return a non-200 status, so the AWS EventBridge does not continue on to the next StepFunction
                    return {
                        'statusCode': 201
                    }
            # Return a 200 status, so the AWS EventBridge continues on to the next StepFunction
            return {
                'statusCode': 200
            }
        # Return a 400 status to kill the request and flag this as a non-GRO Biosciences request
        else:
            return {
                'statusCode': 400
            }
