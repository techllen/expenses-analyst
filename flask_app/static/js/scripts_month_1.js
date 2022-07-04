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

var categoriesLabelsAndTotalBar = [];

function getCategories(month,year){
  // retrieving data from API
  var categoriesData = fetch(`http://localhost:5000/get_all_categories/${currentMonth}/${currentYear}`)
  .then( response => response.json() )
  .then(data => {
    for (let i = 0; i < data.length; i++) {
      // console.log( data[i].category)
      // adding labels to the array
      if (i == 0 ){
        var categoriesLabelsAndTotalBarLets = [];
        categoriesLabelsAndTotalBarLets[0] = "Month"
        categoriesLabelsAndTotalBarLets[1] = "Category";
        categoriesLabelsAndTotalBarLets[2] = "Category Total";
        // console.log(data[i])
        categoriesLabelsAndTotalBar.push(categoriesLabelsAndTotalBarLets)
      }else{
        var categoriesLabelsAndTotalBarLets = [];
        categoriesLabelsAndTotalBarLets[0] = currentMonth
        categoriesLabelsAndTotalBarLets[1] = data[i].category;
        categoriesLabelsAndTotalBarLets[2] = Math.floor(Math.abs(data[i].category_total));
        // console.log(data[i])
        categoriesLabelsAndTotalBar.push(categoriesLabelsAndTotalBarLets)
      // }
    }
  }
}
    // console.log(data.length) 
    )
}

getCategories(currentMonth,currentYear);

console.log(categoriesLabelsAndTotalBar)

google.charts.load('current', {'packages':['bar']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable(
          categoriesLabelsAndTotalBar
        );

        var options = {
          chart: {
            title: 'Money Out Breakdown Individual Comparison',
            // subtitle: 'Sales, Expenses, and Profit: 2014-2017',
          },
          bars: 'vertical' // Required for Material Bar Charts.
        };

        var chart = new google.charts.Bar(document.getElementById('money-out-brkdwn-bar-month'));

        chart.draw(data, google.charts.Bar.convertOptions(options));
      }


$(window).resize(function(){
  drawChart();
});



