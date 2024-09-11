# CertifyBot
CertifyBot is a streamlined tool designed to automate the tedious process of generating certificates and emailing them to participants. With simple customization options, it efficiently creates and sends personalized certificates, saving time and eliminating manual tasks.

# Project Overview
This script automates the creation and distribution of certificates for a tennis club in Singapore, recognizing participants for their efforts in winning the Singapore club. It processes a CSV file containing participant names and email addresses, generates personalized PDF certificates, and sends them via email. This solution has been effectively used to distribute certificates to hundreds of participants annually.

## Input:
A CSV file containing a list of participant names and email addresses.
## Output:
Automatically generates individual PDFs (Certificates of Achievement) and emails them to each participant.
## Main Components:

Certificate Generator: Creates personalized certificates in PDF format to celebrate participants' achievements.

Email Sender: Automatically sends the certificates as email attachments to the participants.

## Step 1: Setup

<div style="background-color: #0d1117; padding: 16px; border-radius: 6px; margin-bottom: 16px;">
  <pre style="margin: 0;"><code style="color: #c9d1d9; background-color: #0d1117;">git clone https://github.com/stevienovak/CertifyBot.git</code></pre>
</div>

## Step 2: Write up your JSON File in the Config folder as follows:

<div style="background-color: #0d1117; padding: 16px; border-radius: 6px; margin-bottom: 16px;">
  <pre style="margin: 0;"><code style="color: #c9d1d9; background-color: #0d1117;">
    
    dict1 = {
    "gmail_user": "[YourUserName@gmail.com",
    "gmail_password": "[Password]"
    }
    with open("settings.json", "w") as out_file:
      json.dump(dict1, out_file, indent=4, sort_keys=False)
</code></pre>
</div>

## Step 3: Running the Script

<div style="background-color: #0d1117; padding: 16px; border-radius: 6px; margin-bottom: 16px;">
  <pre style="margin: 0;"><code style="color: #c9d1d9; background-color: #0d1117;">python cert_autobot.py
</code></pre>
</div>
