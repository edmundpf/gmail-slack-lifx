# gmail-slack-lifx
##### Get Notifications from all your Gmail Accounts in Slack Messenger and via your Lifx Lights. 
##### Display your latest emails in the terminal via IMAP.

## Prerequisites
1. You will need a bot user for your Slack Workspace. This can be created at https://api.slack.com/
   - Your Slack App needs to have these settings enabled:
     - Incoming Webhooks
     - Bots
     - Permissions
   - Get your *Bot User OAuth Access Token* from the Permissions tab
   
2. You will need your Lifx API key
   - Generate an API token at https://cloud.lifx.com/settings
   
## Installation
1. Download the .ZIP and extract **OR**
   - Use `git clone git@github.com:edmundpf/gmail-slack-lifx.git` to clone the repo via SSH
   - Use `git clone https://github.com/edmundpf/gmail-slack-lifx.git` to clone the repo via HTML
2. Install the required modules with `pip install -r requirements.txt`
3. Run `python3 data_file_gen.py` to generate all required data files
4. Run `python3 add_accounts.py` to add your emails and passwords to the data file.
5. Add your Slack and Lifx API keys to the *KEYS.csv* file in the *DATA* directory. Your file should look like this:

   ```
   SLACK,xxxxxxxxxxxxxxxxxxxxxxx
   LIFX,xxxxxxxxxxxxxxxxxxxxxxxx
   ```
   
## Customization
1. My script is currently set to send Slack notifications to the *#emails* and *#lifx_lights* channels. You will need to change the following lines of code to send notifications to your desired Slack channels:
   - In the *lifx_notify()* method:
     - `slack_mini_att(_EMAIL, "Lifx New Email Notification was successful! :yum:", "#your_channel_here", _COLOR)`
   - In the *email_attachment()* method:
     - `slack_att_custom(_attach, None, "#your_channel_here")`
     
## Gmail Setup
1. You may receive IMAP authentification errors for your accounts due to Google Security Settings if you run this on an external server and not your usual IP address. To fix these errors:
   - Make sure IMAP is enabled for your Gmail accounts
   - Allow less secure apps for your account https://myaccount.google.com/lesssecureapps
   - You will most likely get an email about a *blocked signin attempt* from Google:
     - If so, go to https://myaccount.google.com/u/0/device-activity and verify the device for your account
   - After your device has been verified by Google and less secure apps are allowed for your account, you'll be able to login via IMAP using the script
   
## Usage
1. Run `python3 master.py` to get all the most recent emails for your Gmail accounts
   - If a new email is found, a notification will be sent to your Slack messenger and your Lifx Lights
     - Your Slack messenger will show the sender of the email and the subject of the email
     - Your Lifx lights will pulse **RED** three times to indicate a new email has arrived
2. The terminal script will show you the most recent email for each account

## Setting up Cron
1. Run the script via Cron to get updates constantly throughout the day
2. My cron is configured to check for new emails every three minutes. Set your desired interval as follows:
   - `*/3 * * * * cd /your/script/directory/ && python3 master.py`
3. Your computer or server will now check for new emails and send notifications at your desired interval. 
