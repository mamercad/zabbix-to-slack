# Slack to Zabbix

Zabbix alertscript that sends triggers to Slack. There are likely numerous of these in the wild, but this one is mine, and I prefer to use my own stuff sometimes.

## Installation

1. All you really need from this repo is `slack.py`, the image `zabbix.png` is called from the script over HTTP from this Github repo. Copy `slack.py` into your Zabbix alertscripts directory, typically something like `/usr/lib/zabbix/alertscripts`.

2. In the Zabbix interface, create a new `Media Type` called `Slack` located in the Administration section:
  * Name: `Slack`
  * Type: `Script`
  * Script name: `slack.py`
  * Script parameters:
    * `{ALERT.SENDTO}`
    * `{ALERT.SUBJECT}`
    * `{ALERT.MESSAGE}`
  * Enabled: `checked`

3. Create a user named `slack` also in the Administration section:
  * Alias: `slack`
  * Name: `Slack`
  * Last Name: `Notify`
  * Groups: `Read only`
  * Password: (up to you)
  * Language: (up to you)
  * Theme: (up to you)
  * Auto-login: (probably unchecked)
  * Auto-logout: (probably unchecked)
  * Refresh: doesn't matter
  * Rows per page: doesn't matter
  * URL (after login): doesn't matter

4. Under the previous user's `Media` add `Slack`:
  * Type: `Slack`
  * Send to: `SLACK_API_KEY,#SLACK_CHANNEL`
    * For example: `xoxp-?-?-?-?,#general`
  * When active: (up to you)
  * Use if severity: (up to you)
  * Enabled: `checked`

That should be it.
