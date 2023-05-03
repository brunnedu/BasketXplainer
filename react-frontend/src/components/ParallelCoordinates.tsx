import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import HighchartsExporting from 'highcharts/modules/exporting';
import HighchartsAccessibility from 'highcharts/modules/accessibility';
import HighchartsParallelCoordinates from 'highcharts/modules/parallel-coordinates';
HighchartsExporting(Highcharts);
HighchartsAccessibility(Highcharts);
HighchartsParallelCoordinates(Highcharts);






interface ParallelCoordinatesProps {
  data_orig: string;
  limits: any;
  custom: any;
}

const ParallelCoordinates: React.FC<ParallelCoordinatesProps> = ({ data_orig, limits, custom }) => {
  // example format
  // data = [
  //   [0, 30], 
  //   [2, 45], 
  // ];
  // console.log("ParallelCoordinates update");
  if(data_orig === "") return (<div></div>);

  var columns: Array<string>;
  var data: Array<Array<number>>;
  //the data is a csv string. the first row is the column names. the rest needs to be converted to a 2d array
  var lines = data_orig.split("\n");
  columns = lines[0].split(",");
  data = [];
  for (var i = 1; i < lines.length; i++) {
    var currentline = lines[i].split(",");
    var row = [];
    for (var j = 0; j < currentline.length; j++) {
      row.push(parseFloat(currentline[j]));
    }
    data.push(row);
  }

  // console.log(columns);
  // console.log(data);
  // console.log(custom);

  //add custom to data
  row = [];
  var keys = Object.keys(custom);
  for (i = 0; i < keys.length; i++) {
    var key = keys[i];
    row.push(custom[key]);
  }
  data.push(row);

  // console.log(data);

  // console.log(limits);
  //limits looks like this
  // {
  //   "AST": [
  //   20.397802299961352,
  //   29.187563553697185
  //   ],
  //   "BLK": [
  //   2.706578074001372,
  //   7.122690218681554
  //   ],
  // }

  //example format
  // const limits2 = [
  //   {
  //     type: 'linear',
  //     min: 0,
  //     max: 10,
  //     startOnTick: false,
  //     reversed: true,
  //   },
  //   {
  //     type: 'linear',
  //     min: 10,
  //     max: 100,
  //     startOnTick: false,
  //     reversed: true,
  //   }
  // ];
  var limits2:any = [];
  for (i = 0; i < columns.length; i++) {
    var name:string = columns[i].trim();
    var limit = limits[name];
    var limit0 = Math.floor(limit[0]);
    var limit1 = Math.ceil(limit[1]);
    var tickAmount = 1;
    var tickInterval = (limit1 - limit0) / tickAmount;
    limits2.push({
      type: 'linear',
      min: limit0,
      max: limit1,
      startOnTick: false,
      // endOnTick: true,
      reversed: false,
      // tickAmount: tickAmount,
      tickInterval: 1,
    });
  }

  
  
  const getOptions = () => ({
    chart: {
      type: 'line',
      backgroundColor: '#e4c494',
      width: 350,
      height: 300,
      parallelCoordinates: true,
      parallelAxes: {
        lineWidth: 2,
      },
    },
    title: {
      text: 'Parallel Coordinates Chart',
    },
    xAxis: {
      categories: columns,
      offset: 10,
    },
    // the y axis needs to be reversed and needs to have limits
    yAxis: limits2,
    series: data.map((set, i) => ({
      name: `Line ${i}`,
      data: set,
      color: (i == 31 ? '#00FF00' : 'rgba(0, 0, 0, 0.2)'),
    })),
    credits: {
      enabled: false,
    },
  });


  return <HighchartsReact highcharts={Highcharts} options={getOptions()} />;
};

// function ParallelCoordinates() {
//   return <HighchartsReact highcharts={Highcharts} options={getOptions()} />;
// }

export default ParallelCoordinates;