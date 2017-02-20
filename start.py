"""Show streaming Sensor Data in Browser"""

from flask import make_response
from flask import request
from jinja2 import Template
from flask import Flask, jsonify
from collections import deque

html = Template('''\
<!DOCTYPE html>
<html>
  <head>
    <title>Streaming Android Data</title>
    <style>
      #Mag_chart {
        min-height: 300px;
      }
      #Orient_chart {
        min-height: 300px;
      }
      #Acc_chart {
        min-height: 300px;
      }
      #LinAcc_chart {
        min-height: 300px;
      }
    </style>
    <link
      rel="stylesheet"
      href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
  </head>
  <body>
    <div class="container">
    <h4 class="label label-primary">{{ title }}</h4>
    <div id="Mag_chart"></div>
    <div id="Orient_chart"></div>
    <div id="LinAcc_chart"></div>
  </body>
  <script
    src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js">
  </script>
  <script
    src="//cdnjs.cloudflare.com/ajax/libs/flot/0.8.2/jquery.flot.min.js">
  </script>
  <script
    src="//cdnjs.cloudflare.com/ajax/libs/flot/0.8.2/jquery.flot.time.min.js">
  </script>

  <script>
  var Mag_chart;
  var Orient_chart;
  var LinAcc_chart;
  const MagVec = new Array();
  const MagOrient = new Array();
  const MagLinAcc = new Array();

  function get_data() {
    $.ajax({
        url: '/data',
        type: 'GET',
        dataType: 'json',
        success: on_data
    });
  }

  function on_data(data) {

    Mag_chart.setData([
        {data: data.mag_x, label: "Mag(X)"},
        {data: data.mag_y,label: "Mag(Y)"},
        {data: data.mag_z, label: "Mag(Z)"},]);
    Mag_chart.setupGrid();
    Mag_chart.draw();
    Orient_chart.setData([
        {data: data.orient_x, label: "Orient(X)"},
        {data: data.orient_y,label: "Orient(Y)"},
        {data: data.orient_z, label: "Orient(Z)"},]);
    Orient_chart.setupGrid();
    Orient_chart.draw();
    Acc_chart.setData([
        {data: data.linacc_x, label: "LinAcc_chart(X)"},
        {data: data.linacc_y,label: "LinAcc_chart(Y)"},
        {data: data.linacc_z, label: "LinAcc_chart(Z)"},]);
    Acc_chart.setupGrid();
    Acc_chart.draw();
    LinAcc_chart.setData([
        {data: data.linacc_x, label: "LinAcc_chart(X)"},
        {data: data.linacc_y,label: "LinAcc_chart(Y)"},
        {data: data.linacc_z, label: "LinAcc_chart(Z)"},]);
    LinAcc_chart.setupGrid();
    LinAcc_chart.draw();
    setTimeout(get_data, 500);
  }

  $(function() {
    Mag_chart = $.plot("#Mag_chart", [ ], { xaxis:{ mode: "time"} });
    Orient_chart = $.plot("#Orient_chart", [ ], { xaxis:{ mode: "time"}});
    Acc_chart = $.plot("#Acc_chart", [ ], { xaxis:{ mode: "time"}});
    LinAcc_chart = $.plot("#LinAcc_chart", [ ], { xaxis:{ mode: "time"}});
    get_data();
  });

    </script>
</html>
''')

app = Flask(__name__)
title = "Android Data Streaming"
# In memory RRDB
mx = deque(maxlen=100)
my = deque(maxlen=100)
mz = deque(maxlen=100)
ox = deque(maxlen=100)
oy = deque(maxlen=100)
oz = deque(maxlen=100)
ax = deque(maxlen=100)
ay = deque(maxlen=100)
az = deque(maxlen=100)
lax = deque(maxlen=100)
lay = deque(maxlen=100)
laz = deque(maxlen=100)
rest = ""

@app.route('/')
def home():
    return html.render(title=title)


@app.route('/streamdata', methods=['POST'])
def streamaccept():
    vals = request.json
    mx.append((vals['date'], vals['Mag_x']))
    my.append((vals['date'], vals['Mag_y']))
    mz.append((vals['date'], vals['Mag_z']))
    ox.append((vals['date'], vals['Orient_x']))
    oy.append((vals['date'], vals['Orient_y']))
    oz.append((vals['date'], vals['Orient_z']))
    ax.append((vals['date'], vals['Acc_x']))
    ay.append((vals['date'], vals['Acc_y']))
    az.append((vals['date'], vals['Acc_z']))
    lax.append((vals['date'], vals['LinAcc_x']))
    lay.append((vals['date'], vals['LinAcc_y']))
    laz.append((vals['date'], vals['LinAcc_z']))
    return make_response()

@app.route('/data')
def data():
    # * 1000 to convert to javascript time
    return jsonify(mag_x=[(int(time), val) for time, val in mx],
                   mag_y=[(int(time), val) for time, val in my],
                   mag_z=[(int(time), val) for time, val in mz],
                   orient_x=[(int(time), val) for time, val in ox],
                   orient_y=[(int(time), val) for time, val in oy],
                   orient_z=[(int(time), val) for time, val in oz],
                   acc_x=[(int(time), val) for time, val in ax],
                   acc_y=[(int(time), val) for time, val in ay],
                   acc_z=[(int(time), val) for time, val in az],
                   linacc_x=[(int(time), val) for time, val in lax],
                   linacc_y=[(int(time), val) for time, val in lay],
                   linacc_z=[(int(time), val) for time, val in laz])


def main():
    # debug will reload server on code changes
    # 0.0.0.0 means listen on all interfaces
    app.run(host='0.0.0.0', port=9999)


if __name__ == '__main__':
    main()