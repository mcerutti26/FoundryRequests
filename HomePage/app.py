from slack_sdk import WebClient
import requests
import sys
from AWSHelper import get_aws_parameter, AWSDataBase
from SlackHelper import lg_login_modal


def update_home_tab(client, curuser, cur_db):
    # Retrieve LabGuru token
    cur_token = cur_db.token
    # Test if LabGuru token is valid
    r = requests.get('https://my.labguru.com/api/v1/projects/1.json', params=dict(token=cur_token))

    intro_block = [{
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Foundry Request Generator",
        }
    },
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Create a new Foundry Request with the click of a button"
            }
        }
    ]
    token_block = [
        {'type': 'actions',
         'elements': [{
             "type": "button",
             "text": {
                 "type": "plain_text",
                 "text": "Get New LG Token"
             },
             "value": "click_me_123",
             "action_id": "tokenaction"
         }]
         }]
    # If LabGuru token is not valid, update the home page of the Slack app to prompt the user to login and
    # retrieve/store a new token
    if not r.ok:
        assembled_blocks = intro_block + token_block
        client.views_publish(
            user_id=curuser,
            view={"type": "home",
                  "callback_id": "home_view",
                  "blocks": assembled_blocks
                  }
        )
        sys.exit(201)
    # If LabGuru token is valid, update the home page of the Slack app normally and provide buttons for requesting
    # experiments.
    else:
        assembled_blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Foundry Request Generator",
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "Create a new Foundry Request with the click of a button"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Analytical - General",
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Nucleotide Analysis*\n96-plex electrophoresis of DNA or RNA samples"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Request"
                    },
                    "value": "Nucleotide_Analysis"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Expression*\nGrowth, induction, and harvest of 1mL cultures"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Request"
                    },
                    "value": "Expression"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Western Blots*\nCapillary-based protein sizing/quantification"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Request"
                    },
                    "value": "Western_Blots"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Expression with Western*\nHT Expression followed by HT Western of expressed cultures"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Request"
                    },
                    "value": "Expression_with_Western"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Western Target Onboarding*\nEvaluate detectability of new Western targets"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Request"
                    },
                    "value": "Western_Target_Onboarding"
                }
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Cloning",
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Transformation*\nBulk chemical transformations of validated plasmids"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Request"
                    },
                    "value": "Transformation"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Colony Picking*\nPick from plates into 1mL cultures"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Request"
                    },
                    "value": "Colony_Picking"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Minipreps*\nBulk minipreps from 1mL cultures"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Request"
                    },
                    "value": "Minipreps"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Plasmid Mutagenesis*\nQuikChange-style mutagenesis reactions"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Request"
                    },
                    "value": "Plasmid_Mutagenesis"
                }
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Sample Management",
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Sample Rearray*\nRemap samples from one plate to another"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Request"
                    },
                    "value": "Sample_Rearray"
                }
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Other",
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Other*\nAnything not covered by the templates"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Request"
                    },
                    "value": "Other"
                }
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "LIMS Management",
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Add a New Genetic Part*\nAdds a genetic part to the table and updates relevant colletions"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Request"
                    },
                    "value": "Add_a_New_Genetic_Part"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Add an Anchor Strain*\nPromotes a strain to Anchor status and updates child genotypes"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Request"
                    },
                    "value": "Add_an_Anchor_Strain"
                }
            },
        ]
        client.views_publish(
            user_id=curuser,
            view={"type": "home",
                  "callback_id": "home_view",
                  "blocks": assembled_blocks
                  }
        )
    return


def experiment_modal(client, triggerid, request_type):
    # Open Modal for User to fill in the name of the request before submitting
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


def lambda_handler(event, context):
    # Retrieve Slack bot token for the FoundryRequests Slack app from AWS Systems Manager Parameter Store.
    slack_token = get_aws_parameter(param_name='/slackBotTokens/FoundryRequests')
    # Setup Slack WebClient
    client = WebClient(token=slack_token)
    # Parse the Slack event payload, and determine actions to take based on payload format.
    if event.get('event'):
        user_id = event.get('event').get('user')
        with AWSDataBase(user_id) as db:
            update_home_tab(client, user_id, db)
    else:
        user_id = event.get('user').get('id')
        with AWSDataBase(user_id) as db:
            if event.get('actions')[0].get('action_id') == 'tokenaction':
                r = lg_login_modal(trigger_id=event.get('trigger_id'), slack_client=client)
                return r
            update_home_tab(client, user_id, db)
    return {
        "statusCode": 200
    }
