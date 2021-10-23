d3.json("../../data/hourly_forecast_json2.json").then(function(results) {
    console.log(results);

   var trace1 = {
       x: results.map(row => row.startDateTime),
       y: results.map(row => row.temperature),
       type: 'scatter'
   };
   
   var data=[trace1];

   Plotly.newPlot('plot',data);
});



d3.selectAll("#weatherdata").on("change", updatePlotly);

function updatePlotly() {

d3.json("../../data/hourly_forecast_json2.json").then(function(results) {
    var dropdownMenu = d3.select("#weatherdata");
    var dataset = dropdownMenu.property("value");

    console.log(results);
    console.log(dataset);
    console.log(results.map(row => parseInt(row.windSpeed.replace(" mph",""))));
    var x = []
    var y = []

    if (dataset === 'Temperature') {
        y = results.map(row => row.temperature);
    }

    else if (dataset === 'WindSpeed') {
        y = results.map(row => parseInt(row.windSpeed.replace(" mph","")));
    }
    

    Plotly.restyle("plot", "y", [y]);
});
}
