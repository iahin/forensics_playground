# Splunk Enterprise installation

Developer License installation

1.  Request from website

2.  After receiving license attached file from email

3.  Go to splunk localhost/setting/licensing and follow instruction

# Splunk SDK for python

## Installation

1.  Download sdk from <https://github.com/splunk/splunk-sdk-python>

2.  In the sdk directory, run python setup.py

3.  In user home directory, run notebook.exe .splunkrc and add
    template(written in readme of sdk)

# Notes

1.  Able to select which app to index when editing source info while
    uploading new logs

## Troubleshoot

  1   xml.etree.ElementTree.ParseError: syntax error: line 1, column 0   Change Access scheme in .splunkrc from http to https and port number from 8000 to 8089

## Reference

1.  Explore and get value out of your raw data: An Introduction to
    Splunk \| by Bruno Amaro Almeida \| Towards Data Science -
    <https://towardsdatascience.com/explore-and-get-value-out-of-your-raw-data-an-introduction-to-splunk-e5cb94c0855e>
2.  SPLUNK steps for data:
    <http://localhost:8000/en-US/app/Splunk_Security_Essentials/journey>
3.  Importing Windows Event Log files into Splunk -
    <https://www.cloud-response.com/2019/07/importing-windows-event-log-files-into.html>
4.  Splunklib python tutorial:
    <https://www.youtube.com/watch?v=N4rZaptxUfM> 