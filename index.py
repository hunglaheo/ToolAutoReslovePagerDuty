import json
import os
from time import sleep
import pdpyras
import json
from datetime import datetime
from dateutil.parser import parse
#session = pdpyras.APISession('610683d180d44e09c0d1aa66ba22ae32')
def clearOldIncidents():
    session = pdpyras.APISession('u+APm6HyXdztzDX-xomw',default_from="kwj85910@eoopy.com")
    incidents = session.list_all(
        'incidents',
        params={'user_ids[]':['PPQK4XC'],'statuses[]':['triggered']}
    )
    listResolved = []
    for x in incidents:
        url = "/incidents/" + x["id"] + "/alerts"
        a = session.get(url=url)
        b = json.loads(a.text) 
        if b["alerts"][0]["summary"] == "Vui lòng kiểm tra lại tool":
            now = datetime.timestamp(datetime.now())
            creatd_at = parse(b["alerts"][0]["created_at"])
            creatd_at = creatd_at.timestamp()
            result = now - creatd_at
            if(result>14400):
                x["status"] = 'resolved'
                listResolved.append(x)
                print(x["incident_number"])
        else:
            timeWork = b["alerts"][0]["body"]["details"]["Giờ làm việc"]
            timeWork = datetime.strptime(timeWork,'%d-%b-%Y (%H:%M)')
            timeWork = timeWork.timestamp()
            now = datetime.timestamp(datetime.now())
            result = now - timeWork
            if(result>14400):
                x["status"] = 'resolved'
                listResolved.append(x)
                print(x["incident_number"])
    pdated_incidents = session.rput('incidents',json=listResolved)
if __name__ == "__main__":
    while True:
        print("Clearing......")
        clearOldIncidents()
        print("Sleeping.....")
        sleep(3600)