hasjobbot
=========

A automated robot for http://hasjob.co. After creating account and validating the email address this bot will apply for all the jobs matched with the keyword. The robot is written by using https://pypi.python.org/pypi/mechanize. The robot is not intented for spaming but it is developed to learn the python 'mechanize' library in details. Suggestions and improvements are always welcome.

Running bot
-----------
```
#>python hasjobbot.py --dataFile input.xml
```

Example xml data file
---------------------
```XML
<?xml version="1.0" encoding="UTF-8"?>
<user>
    <username>ramkumar321</username>
    <password>123456</password>
    <email>hasjob1@gmail.com</email>
    <phone>0123456789</phone>
    <message>
    Hello sir,
      I want to apply for this job. Thank you
    </message>
    <keyword>python</keyword>
</user>
```
