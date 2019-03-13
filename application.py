
#Import Flask module and create web server 
#render_template allows for html files to be searched in the template folder
from flask import Flask, render_template, request
from datetime import datetime
import json


app = Flask(__name__)                      #__name__ mean this file i.e. main.py
       
data = {}
data['Carinfo'] = []
data['Queueinfo'] = []

@app.route("/")                            #Default page to show with nothing after the slash
def home():                                #define the default page
    today = datetime.now().strftime("%Y-%m-%d")
    total = 0
    LTL = 0
    RTL = 0
    with open('{}.txt'.format(today)) as json_file:  
        datafile = json.load(json_file)
    for p in datafile['Carinfo']:
        total += int(p['Car'])
    for p in datafile['Queueinfo']:
        LTL = p['Queue LTL']
    for p in datafile['Queueinfo']:
        RTL = p['Queue RTL']
    
    return 'Total Number of cars today: ' + str(total) + \
           '<br/><br/>Left Traffic light current queue: ' + LTL+\
           '<br/><br/>Right Traffic light current queue: ' + RTL

@app.route('/save-vehicle',methods=['POST', 'GET'])
def savevehicle():
    if request.method=='GET':
        a=request.args.get('car', '')
        b=request.args.get('bike', '')
        c=request.args.get('maxfreq', '')
        d=request.args.get('sensor', '')

        data['Carinfo'].append({  
            'Timestamp': datetime.now().strftime("%H:%M:%S"),
            'Car': a,
            'Bike': b,
            'Maximum Frequency': c,
            'Sensor': d
        })
        
        #save data json file by date
        file = datetime.now().strftime("%Y-%m-%d")
        with open('{}.txt'.format(file), 'w') as outfile:  
            json.dump(data, outfile, indent=4)
        
        return "Saved."
    else:
        return "Not get method"
        
@app.route('/save-queue',methods=['POST', 'GET'])
def savequeue():
    if request.method=='GET':
        
        #clear data dictionary for ensuring optimal server performance
        if datetime.now().strftime("%H:%M:%S") < '00:01:00':
            clear.data()
        
        
        a=request.args.get('phase', '')
        b=request.args.get('phasetimeltl', '')
        c=request.args.get('phasetimertl', '')
        d=request.args.get('queueltl', '')
        e=request.args.get('queuertl', '')
        f=request.args.get('duration', '')

        data['Queueinfo'].append({  
            'Timestamp': datetime.now().strftime("%H:%M:%S"),
            'Phase': a,
            'Phase Time LTL': b,
            'Phase Time RTL': c,
            'Queue LTL': d,
            'Queue RTL': e,
            'Remaining Duration': f
        })
        
        #save data json file by date
        file = datetime.now().strftime("%Y-%m-%d")
        with open('{}.txt'.format(file), 'w') as outfile:  
            json.dump(data, outfile, indent=4)            
        
        return "Saved."
    else:
        return "Not get method"
    
if __name__ == "__main__":                #assign script name to __main__ while script is running
    app.run(debug=True)                    #show errors on webpage - allows easier debugging
    
