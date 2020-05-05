from datetime import datetime, timedelta
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/dashboard")
def gen_dashboard():
  d = {'MachineName' : ['DISCOVERY1', 'DISCOVERY2', 'DISCOVERY3',
                        'DISCOVERY4', 'DISCOVERY5', 'DISCOVERY6'],
       'Status' : ['', '', '', '', '', ''],
       'Domain' : ['', '', '', '', '', ''],
       'Username' : ['', '', '', '', '', ''],
       'StartTime' : ['', '', '', '', '', ''],
       'ElapsedTime' : ['', '', '', '', '', '']}
  df = pd.DataFrame(data=d)
  #print(df)
  #print(df.info())

  path = "\\\\ahknts233\\CAE\\flipchip\\Discovery_Tools\\AnsysFWW\\newcs"
  file = "\\" + str(pd.Timestamp.today().date()) + ".csv"
  log_data = pd.read_csv(path + file, index_col=1)

  offset = datetime.now() - timedelta(minutes = 15)

  for MachineName in df['MachineName']:
  #  print(df.loc[df['MachineName'] == MachineName, 'MachineName'])
    flag = df['MachineName'] == MachineName
    try:
      tmp = log_data.loc[MachineName]
      ts = str(datetime.now().date()) + " " + tmp.iloc[-1]["LogTime"]
      stop = datetime.strptime(ts, "%Y-%m-%d %H:%M")
      if stop > offset:
        df.loc[flag, 'Status'] = 'InUse'
        df.loc[flag, 'Domain'] = tmp.iloc[-1]["Domain"]
        df.loc[flag, 'Username'] = tmp.iloc[-1]["Username"]
        username = tmp.iloc[-1]["Username"]
        tmp = tmp.loc[tmp['Username'] == username]
        ts = str(datetime.now().date()) + " " + tmp.iloc[0]["LogTime"]
        start = datetime.strptime(ts, "%Y-%m-%d %H:%M")
        df.loc[flag, 'StartTime'] = start.time()
        df.loc[flag, 'ElapsedTime'] = stop - start
      else:
        df.loc[flag, 'Status'] = 'Available'
    except:
      df.loc[flag, 'Status'] = 'AVAILABLE'

  df = df[['MachineName','Status','Domain','Username','StartTime','ElapsedTime']]
  dashboard = df.groupby("MachineName", as_index=False).last()
  print(dashboard)
  #print(dashboard.info())
  return render_template('LicenseViewer.html',
                         tables = [dashboard.to_html(classes='table_blue')],
                         titles = ["na", "ANSYS Discovery Usage Dashboard"])

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000, debug = False)

