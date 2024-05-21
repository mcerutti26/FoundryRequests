import os
import time
from slack_sdk import WebClient
import json
import requests
import sys
from AWSHelper import AWSDataBase, get_aws_parameter
from SlackHelper import StateMachineSlackEvent


def update_home_tab(client, curuser, cur_db):
    # Try the LG Token
    r = requests.get('https://my.labguru.com/api/v1/projects/1.json', params=dict(token=cur_db.token))

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

    # If the LabGuru token is invalid, change the home tab to prompt the user to login again
    if not r.ok:
        assembled_blocks = intro_block + token_block
        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
            # the user that opened your app's app home
            user_id=curuser,
            view={"type": "home",
                  "callback_id": "home_view",
                  "blocks": assembled_blocks
                  }
        )
        sys.exit(200)
    # If the LabGuru token is valid, load the normal home tab with requestable experiments listed
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
        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
            # the user that opened your app's app home
            user_id=curuser,
            view={"type": "home",
                  "callback_id": "home_view",
                  "blocks": assembled_blocks
                  }
        )
    return


def lambda_handler(event, context):
    # Parse the Slack event into a variable
    curSlackEvent = StateMachineSlackEvent(event)
    # Setup Slack WebClient
    client = WebClient(token=curSlackEvent.slack_token)
    # Connect the AWS RDS with Slack and LabGuru user information
    with AWSDataBase(curSlackEvent.user_id) as db:
        # If the user has submitted a LabGuru login attempt, refresh their token
        if curSlackEvent.human_trigger == 'labguruloginSubmitted':
            cur_lg_un, cur_lg_pw = curSlackEvent.un_pw
            # Get a Labguru access token using the entered username and password
            r = requests.post('https://my.labguru.com/api/v1/sessions.json',
                              data={'login': cur_lg_un, 'password': cur_lg_pw})
            # If a LabGuru token was successfully retrieved, store it in the User database
            if r.ok:
                data = r.json()
                cur_token = data['token']
                db.token = cur_token
                # Pause for a second prior to updating the home tab, so the Database can be updated before it is queried
                time.sleep(1)
                update_home_tab(client, curSlackEvent.user_id, db)
        # Process the users Experiment Request Submission by generating a new experiment in LabGuru and creating a Slack
        # channel dedicated to collaborating on this experiment request.
        else:
            # Parse the event payload from Slack to read what experiment type was requested
            blockid = event['view']['blocks'][1]['block_id']
            exp_title = event['view']['state']['values'][blockid]['request_title']['value']
            exp_type = event['view']['blocks'][0]['text']['text'].replace('What is the title for your ', '').replace(
                ' request?', '').replace(' ', '_')
            # slack_userid = event['user']['id']
            slack_userid = curSlackEvent.user_id
            # A dictionary maps the Slack name of requestable experiments to LabGuru protocol ID #'s.
            slack_lg_dict = {'Nucleotide_Analysis': 70, 'Expression': 126, 'Western_Blots': 126,
                             'Expression_with_Western': 126,
                             'Western_Target_Onboarding': 124, 'aaRS_Barcode_Sequencing': 121, 'Uricase_Assay': 99,
                             'Transformation': 85, 'Colony_Picking': 130, 'Minipreps': 123, 'Plasmid_Mutagenesis': 137,
                             'Sample_Rearray': 131, 'Other': 68, 'Add_a_New_Genetic_Part': 143,
                             'Add_an_Anchor_Strain': 144, 'aaRS_(GNN)_'
                                                          'Sequencing': 146}

            # Create an LG experiment
            lg_token = db.token
            data = {
                "token": lg_token,
                "item": {
                    "milestone_id": 38,
                    "project_id": 18,
                    "protocol_id": slack_lg_dict[exp_type],
                    "title": exp_title
                }
            }
            r = requests.post(url='https://my.labguru.com/api/v1/experiments', json=data)

            # If user managed to submit an Experiment Request as their token expired, that use case will force a
            # hometab update
            if not r.ok:
                time.sleep(1)
                # When update_home_tab is run, the token will be expired, so the home page will prompt a new login.
                update_home_tab(client, curSlackEvent.user_id, db)
            else:
                # Create a new experiment in LabGuru of the submitted type and name
                expt_details = json.loads(r.content.decode())
                expt_id = expt_details['id']
                new_title = f"{int(expt_id):04d} - {exp_title}"
                rename_data = {
                    "token": lg_token,
                    "item": {
                        "milestone_id": 38,
                        "project_id": 18,
                        "title": new_title
                    }
                }
                exp_url = 'https://my.labguru.com/api/v1/experiments/' + str(expt_id)
                r2 = requests.put(url=exp_url, json=rename_data)
                # Create a Slack channel for collaboration
                channel_name = 'request-' + str(expt_id)
                slack_channel = client.conversations_create(name=channel_name, is_private=False)
                channel_id = slack_channel.get('channel').get('id')
                manager_id = get_aws_parameter(os.environ['foundryManagerUserIDPath'])
                client.conversations_invite(channel=channel_id, users=[manager_id, slack_userid])
                # Send a Slack message as the App Bot with a hyperlink to the LabGuru Experiment for quick access
                client.chat_postMessage(channel=channel_id,
                                        text="<" + exp_url.replace('api/v1', 'knowledge') + "|" + new_title + ">")
    return {
        "statusCode": 200
    }
