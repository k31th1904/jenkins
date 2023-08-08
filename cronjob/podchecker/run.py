import os
import sys
import datetime
from kubernetes import client, config
import logging
import ssl
import smtplib
from email.message import EmailMessage

# Collect OS env
password = os.environ['MAILPASSWORD']
sender = os.environ['SENDER']
receiver = os.environ['RECEIVER']


# Create a filename with the current timestamp
#filename = f'/var/log/report_{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.log'
filename = f'/k8slog/report.log'

# Configure logs output
logging.basicConfig(filename=filename, level=logging.ERROR,format='%(levelname)s : %(message)s')
now = datetime.datetime.now(datetime.timezone.utc)

# Configure SMTP
def email(content_list):
    
    
    email_message_from = sender
    email_message_to = receiver
    email_subject = "ERROR: K8S pending pods"
    email_body = content_list

    email_message = EmailMessage()

    email_message['From'] = email_message_from
    email_message['To'] = email_message_to
    email_message['Subject'] = email_subject
    email_message.set_content(email_body)

    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        try:
            smtp.starttls()
            smtp.login(email_message_from,password)
            smtp.sendmail(email_message_from, email_message_to, email_message.as_string())
        except Exception as error:
            print ("Mail Send Error!")

        print("\nNotification email has been sent to %s at %s\n" %(receiver,str(now.strftime("%Y-%m-%d_%H:%M:%S %Z"))))
    return

# load cluster info for kubctl
config.load_incluster_config()

v1 = client.CoreV1Api()

pods = v1.list_namespaced_pod("default")
pending_pods =[]
results = []
for pod in pods.items:
    if pod.status.phase == "Pending":
        results.append("%s%15s%15s%33s" % (pod.metadata.name, pod.metadata.namespace, pod.status.phase, str(pod.metadata.creation_timestamp)))
        pending_pods.append("Pod %s in namespace '%s' was found pending at %s" % (pod.metadata.name, pod.metadata.namespace, now.strftime("%Y-%m-%d %H:%M:%S %Z")))
        #logging.info(pending_pod)

if (results and pending_pods):
    print("Listing 'Pending' pods in default namespace:\n")
    report="This is a system generated alert from your K8S cluster: \n\n"
    print("%s%30s%11s%17s" % ("Pod Name","Namespace","Phase","Created"))
    for i in results:
        print(i)
    for y in pending_pods:
        logging.error(y)
        report+=str("%s\n"%y)
    email(report)

else:
    print("Good News! No 'Pending' pod found. - %s" % str(now.strftime("%Y-%m-%d %H:%M:%S %Z")))
