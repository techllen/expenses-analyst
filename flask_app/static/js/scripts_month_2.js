// MONTHLY ANALYSIS
// get money in and money out values
var moneyInMonth = parseFloat($("#total-income-month").text())
// console.log(moneyIn)
var moneyOutMonth = parseFloat($("#total-expenses-month").text())
// gat current year 
var currentYear = parseInt($("#current-year-month").text())
// get current month
var currentMonth = parseInt($("#current-month").text())

// this method get the categories data from the controller using API
var categoriesLabels = [];
var categoriesTotals = [];

var categoriesLabelsAndTotalDonut = [];

function getCategories(month,year){
  // retrieving data from API
  var categoriesData = fetch(`http://localhost:5000/get_all_categories/${currentMonth}/${currentYear}`)
  .then( response => response.json() )
  .then(data => {
    for (let i = 0; i < data.length; i++) {
      // console.log( data[i].category)
      // adding labels to the array
      if (i == 0 ){
        var categoriesLabelsAndTotalDonutLets = [];
        categoriesLabelsAndTotalDonutLets[0] = "Category";
        categoriesLabelsAndTotalDonutLets[1] = "Category Total";
        // console.log(data[i])
        categoriesLabelsAndTotalDonut.push(categoriesLabelsAndTotalDonutLets)
      }else{
        var categoriesLabelsAndTotalDonutLets = [];
        categoriesLabelsAndTotalDonutLets[0] = data[i].category;
        categoriesLabelsAndTotalDonutLets[1] = Math.floor(Math.abs(data[i].category_total));
        // console.log(data[i])
        categoriesLabelsAndTotalDonut.push(categoriesLabelsAndTotalDonutLets)
      // }
    }
  }
}
    // console.log(data.length) 
    )
}

getCategories(currentMonth,currentYear);

console.log(categoriesLabelsAndTotalBar)


// MONEY OUT BREAKDOWN DONUT GRAPH
// getting the values for plotting the graph

google.charts.load("current", {packages:["corechart"]});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
  var data = new google.visualization.arrayToDataTable(categoriesLabelsAndTotalDonut);
  // data.addColumn('string', 'Category');
  // data.addColumn('string', 'Category Total');

  // for (let j = 0; j < categoriesLabelsAndTotalDonut.length; j++) {
  //   data.addRows(JSON.parse(categoriesLabelsAndTotalDonut[j]));
  //   console.log(categoriesLabelsAndTotalDonut[j])
  // }

  var options = {
    title: 'Money out breakdown Comparison To Total',
    pieHole: 0.3,
  };

  var chart = new google.visualization.PieChart(document.getElementById('money-out-brkdwn-doughnut-month'));
  chart.draw(data, options);
}


$(window).resize(function(){
  drawChart();
});



