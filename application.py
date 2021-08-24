import os, requests, json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# triggers modal popup when bot receives /sendpage command
@app.command("/sendpage")
def open_modal(ack, body, client):

    # Acknowledge the command request
    ack()

    # Call views_open with the built-in client
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
	"title": {
		"type": "plain_text",
		"text": "Create Opsgenie Alert"
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit"
	},
	"type": "modal",
    "callback_id": "view_1",
	"close": {
		"type": "plain_text",
		"text": "Cancel"
	},
	"blocks": [
		{
			"type": "divider"
		},
		{
			"type": "input",
			"block_id": "input_message",
			"element": {
				"type": "plain_text_input",
				"action_id": "plain_text_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Alert Message"
			}
		},
		{
			"type": "input",
			"block_id": "input_team",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item"
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "ASER_Team"
						},
						"value": "ASER_Team"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Android"
						},
						"value": "Android"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "CameraBackend"
						},
						"value": "CameraBackend"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "CameraCloud"
						},
						"value": "CameraCloud"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "App_QA"
						},
						"value": "App_QA"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "ClientApps_Team"
						},
						"value": "ClientApps_Team"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Call_Center_Outage_Team"
						},
						"value": "Call_Center_Outage_Team"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "CSE"
						},
						"value": "CSE"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "CURE"
						},
						"value": "CURE"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Customer_Marketing_Outage_Team"
						},
						"value": "Customer_Marketing_Outage_Team"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "DevOps_Team"
						},
						"value": "DevOps_Team"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Drupal_Team"
						},
						"value": "Drupal_Team"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "E-Commerce"
						},
						"value": "E-Commerce"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "FCP engineering"
						},
						"value": "FCP engineering"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "FIRE"
						},
						"value": "FIRE"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "International"
						},
						"value": "International"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "iOS"
						},
						"value": "iOS"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "IT"
						},
						"value": "IT"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Monitoring"
						},
						"value": "Monitoring"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Network"
						},
						"value": "Network"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "PR_Outage_Team"
						},
						"value": "PR_Outage_Team"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Security"
						},
						"value": "Security"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Siren_Services"
						},
						"value": "Siren_Services"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Social_Media_Outage_Team"
						},
						"value": "Social_Media_Outage_Team"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "SS3 Core"
						},
						"value": "SS3 Core"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "UK_Team_Alerts"
						},
						"value": "UK_Team_Alerts"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "WebApp"
						},
						"value": "WebApp"
					}
				],
				"action_id": "static_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Team"
			}
		}
	]
}
    )

# Handles the view_submission request
@app.view("view_1")
def handle_submission(ack, body, client, view, logger):
    alert_message = view["state"]["values"]["input_message"]["plain_text_input-action"]["value"]
    alert_team = view["state"]["values"]["input_team"]["static_select-action"]["selected_option"]["value"]
    user = body["user"]["id"]
    api_key = os.environ.get('OPSGENIE_INTEGRATION_KEY')

    # Acknowledge the view_submission request and closes the modal
    ack()

    # Do whatever you want with the input data - here we're using the input data to send a create alert request to opsgenie
	# then sending the user a verification of their submission

	#api requests to opsgenie
    headers = {
		'Authorization': f'GenieKey {api_key}',
		'Content-Type': 'application/json',
		}

    data = {
	'message': alert_message,
	'responders': [{
		'name': alert_team,
		'type': 'team'
	}],
	'priority': 'P1'
	}

    data = json.dumps(data)

    response = requests.post('https://api.opsgenie.com/v2/alerts', headers=headers, data=data)

    # to see the request body
    # print(response.request.body)

    # Message to send user
    msg = ""
    try:
        # Save to DB
        msg = f"Your submission of \"{alert_message}\" to {alert_team} was successful!"
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission"

    # Message the user
    try:
        client.chat_postMessage(channel=user, text=msg)
    except e:
        logger.exception(f"Failed to post a message {e}")

	# Another handling of the message to send user
    # if response.status_code == 202:
    #     msg = f"Your submission of \"{alert_message}\" to {alert_team} was successful!"
    # else:
    #     msg = "There was an error with your submission"

# Terminal kept indicating an unhandled request and suggested I use this listener function
# Upon review this handles the response message back from opsgenie when the alert is created
@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
