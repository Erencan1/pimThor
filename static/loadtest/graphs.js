class Graph
{
  constructor(div_id)
  {
      this.data = [];
      this.div_id = div_id;
      // this.xaxis_set = new Set();
  }

  add(da, name, yaxis)
  {
      var keys = Object.keys(da);
      keys.sort();
      var x = [];
      var y = [];
      var t;
      for (var k=0; k<keys.length; k++)
      {
          t = keys[k];
          x.push(t);
          y.push(da[t]);
      }
      // for (var t in da)
      // {
      //     // this.xaxis_set.add(t);
      //     x.push(t);
      //     y.push(da[t]);
      // }
      var trace = {
          x: x,
          y: y,
          // type: 'scatter',
          name: name
      };
      if (yaxis){
          trace['yaxis'] = yaxis;
      }
      this.data.push(trace);
  }

  display()
  {
      var layout = {
          // xaxis:{
          //     "categoryarray": Array.from(this.xaxis_set)
          // },
          yaxis2: {
              overlaying: 'y',
              side: 'right'
          }
      };
      Plotly.newPlot(this.div_id, this.data, layout);
  }

}

function hmap(prb_data, div_id) {
    var time = [];
    var prb_value = [];
    for (var t in prb_data)
    {
        time.push(t);
        prb_value.push(prb_data[t]);
    }
    // prb_value.push([-122, 0]);
    var data = [
        {
            x: [1,2,3,4,5,6,7,8,9,10],
            y: time,
            z: prb_value,
            colorscale: 'Jet',
            // colorscale: [
            //     [0, 'blue'],
            //
            //     [0.08, 'rgb(178,223,138)'],
            //     [0.1, 'yellow'],
            //     [0.15, 'rgb(227,26,28)'],
            //     [0.4, 'white'],
            //     [1, 'white']
            // ],
            type: 'heatmap'
        }
        ];
    var layout = {title: 'Uplink Noise Heat Map'};
    Plotly.newPlot(div_id, data, layout);
}