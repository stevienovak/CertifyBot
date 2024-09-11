pycert
======

PyCert: Automated Certificate Generator and Emailer for PyCon PH

Developed for PyCon PH 2015, this script automates the process of creating and distributing attendance certificates. It efficiently processes a CSV file containing attendee names and emails, generates individual PDF certificates, and emails them to each participant. Due to its effectiveness, it has been utilized annually to handle certificate distribution for hundreds of attendees.

- Input: accepts a CSV file which contains a list of attendee names and emails
- Output: generate multiple PDFs (certificate of attendance) and then sends the certificates via email to each paticipant.

Main Parts:

- certificate maker
- email sender with pdf attachment

## Dev Environment Setup
```
(pycert) $ pip install -r requirements.txt
```

## Settings
Add a `settings.json` in `config/` folder with the following format:
```
{
    "gmail_user": "you@gmail.com",
    "gmail_password": "<your-app-password>"
}
```



## References:

### Generating PDF
- https://realpython.com/creating-modifying-pdf/#setting-font-properties
- https://medium.com/@schedulepython/how-to-watermark-your-pdf-files-with-python-f193fb26656e

### Sending Email
- https://realpython.com/python-send-email/#adding-attachments-using-the-email-package
