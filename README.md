# FoundryRequests

This project contains source code and supporting files for four serverless applications (AWS Lambda functions) that are 
a part of the AWS architecture for a Slack application where other teams within our company's R&D can request 
boilerplate experiments for our Foundry team to execute. The homepage of the application lists out all of the available 
experiments to request, and upon clicking an associated "Request" button, the user is prompted to submit the request
with the name of the experiment. After submission, a new experiment is created in our electronic lab notebook hosted
on LabGuru's website and a dedicated Slack channel is created for the Foundry manager, requester, and any other involved 
personnel to collaborate on the experiment.

This repository includes the following directories, each one is a Lambda function:

- AuthandResponse - Confirms that the Slack request is coming from someone in our company's Slack Workspace. This 
function also deploys the modal (aka pop-up) after a "Request" button is clicked. This response functionality was added 
because this Lambda is the first Lambda triggered by the app, and Slack modals must respond within 3 seconds of a Slack app button click.
- HomePage - Loads the Slack homepage with a list of requestable experiments and associated "Request" buttons.
- SlackEventParser - Interprets the event payload sent from Slack as it is passed from one AWS Step Function to another.
- Submission - Creates an experiment in our LabGuru electronic lab notebook website and creates a dedicated Slack 
channel for the request.

The template.yaml file is a template that defines the application's AWS resource deployment and is used by Pycharm's AWS Toolkit 
to package the four directories into Docker containers that are synced with the associated AWS Lambda functions.

## Slack App View and Function
After installing the FoundryRequests app to Slack, the app will check if you have a valid token to our company's electronic lab notebook, LabGuru, stored in the AWS RDS.
Access tokens are shared across Slack applications via this AWS RDS, and the users can refresh their token from any of our Slack applications.
Here is an example view of the RDS Users table:

![alt text](RDS_UsersTable.png)

If the user's token is expired or does not exist, the homepage will load with a prompt to login:

![alt text](GetNewTokenHomepage.png)

After clicking 'Get New LG Token' a pop-up modal allows the user to enter their login information for the LabGuru website. As you can see from the RDS Users table, only the user's token is saved, not their username and password.

![alt text](FoundryRequestsLoginModal.png)

Once the user has a valid token in the RDS, the catalogue of requestable experiments is listed on the homepage. Clicking the associated "Request" button launches a pop-up to fill in the Title of the experiment and hit 'Submit'.

![alt text](FoundryRequestsHomePage.png)
![alt text](FoundryRequestsEntryModal.png)

Clicking 'Submit' results in a new Slack channel for the requester and Foundry team to collaborate on the experiment and a hyperlink is sent by the app that leads to the LabGuru electronic lab notebook entry for the requested experiment. 
The lab notebook will be pre-filled with the boilerplate experiment information based on the type of requested experiment.

![alt text](FoundryRequestsOutputChannelandNotebookEntry.png)

## AWS Serverless Architecture and Resources

These lambda functions operate within the scope of the AWS architecture designed below. The architecture was based on the AWS Well Architected Framework for a serverless app with some modifications to better fit my use case.

![alt text](AWS_Architecture_FoundryRequestsApp.png)

The first StepFunction that is triggered by the API Gateway and verifies that the request is coming from someone within my company:

![alt text](StepFunctionMap_FoundryRequestsRequestValidator.png)

The second StepFunction that handles the bulk of the actual work to submit a request and load the app homepage:

![alt text](StepFunctionMap_FoundryRequestsStepFunction.png)