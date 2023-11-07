import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import json
from datetime import datetime, timedelta


def send_mail(sub,body):
    email_address='mecooldeepak14@gmail.com'
    email_password='qntw jcxm oezm tecx'
    receiver_mail='deepak.kr2899@gmail.com'

    # setup the parameters of the message
    msg=MIMEMultipart()
    msg['From']=email_address
    msg['To']=receiver_mail
    msg['Subject']=sub
    # add in the message body
    msg.attach(MIMEText(body, 'plain'))

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(email_address,email_password)
    s.send_message(msg)
    # Terminate the SMTP session and close the connection
    s.quit() 
    # print("Mail sent Successful")


def get_connector_details(connector_id):
    url=f"https://api.fivetran.com/v1/connectors/{connector_id}"
    payload = ""
    headers = {
    'Accept': 'application/json;version=1',
    'Authorization': 'Basic ajUySFJJVFc5VDFubGJudjp2Yk8wRkJTakNWQ2JPOVh2SEl4eUpYTFZTd1U5OTlhMg==',
    'Cookie': 'INGRESSCOOKIE=b65567d4f48ebd558c87d600d2f76fbd|bac6da9b4d464a443a3af1340233b03f'
    }
    response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)
    output={'succeeded_at':response['data']['succeeded_at'],\
            'setup_state':response['data']['status']['setup_state'],\
            'sync_state':response['data']['status']['sync_state']}
    return output





if __name__=='__main__':
    connector_id='chaste_cautiously'

    connector_data=get_connector_details(connector_id)
    sync_state=connector_data['sync_state']
    setup_state=connector_data['setup_state']
    succeeded_at=datetime.strftime(datetime.strptime(connector_data['succeeded_at'],'%Y-%m-%dT%H:%M:%S.%fZ'),'%Y%m%d%H%M')

    #connector scheduled time is the time when this connector is scheduled for data sync
    connector_scheduled_time=datetime.strftime(datetime.utcnow()-timedelta(minutes=30),'%Y%m%d%H%M')
    #check time will be the when we start monitoring which is after 30 min of connector scheduled time
    check_time=datetime.strftime(datetime.utcnow(),'%Y%m%d%H%M')
    

    if setup_state=='connected':
        if sync_state=='syncing':
            send_mail('Data sync still in progress','The data sync is still in progress. Please check why its taking extra time.')
        elif sync_state=='paused':
            send_mail('Data Sync paused','Data sync is paused. Please verify it')
        elif sync_state=='resheduled':
            send_mail('Data sync resheduled','Data sync is resheduled. Please verify it')
        elif sync_state=='scheduled':
            if succeeded_at>=connector_scheduled_time and succeeded_at<=check_time:
                send_mail('Sync Successful','Sync was completed successfully. Please proceed further')
            else:
                send_mail('Data not synced','Data was not synced. Please verify it')
    else:
        send_mail('Connector not connected','The connector is not connected. Please check it.')




    # get_connector_details(connector_id)
    # send_mail('Sync Successful','Please proceed further and refresh the nodes')