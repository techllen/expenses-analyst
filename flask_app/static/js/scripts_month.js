

// MONTHLY ANALYSIS
// get money in and money out values
var moneyInMonth = parseFloat($("#total-income-month").text())
// console.log(moneyIn)
var moneyOutMonth = parseFloat($("#total-expenses-month").text())

// below code will plot a graph for money in - money out analysis
var totalLabelsMonth = [
    "Money In",
    "Money Out",
  ];

  var dataMonth = {
    labels: totalLabelsMonth,
    datasets: [{
      label: "Monthly Money In/Money Out",
      backgroundColor: "#153d77",
      borderColor: 'rgb(255, 99, 132)',
      data: [moneyInMonth,moneyOutMonth],
    }]
  };

  var configMonth = {
    type: 'bar',
    data: dataMonth,
    options: {}
  };

  var myChartMonth = new Chart(
    document.getElementById("money-graph-month"),
    configMonth
  );


  // below code will plot a graph for money out breakdown bar graph analysis

// gat current year 
var currentYear = parseInt($("#current-year-month").text())
// get current month
var currentMonth = parseInt($("#current-month").text())
// console.log(currentYear)
// console.log(currentMonth)

// this method get the categories data from the controller using API
var categoriesLabelsMonth = [];
var categoriesTotalsMonth = [];

function getCategories(month,year){
  // retrieving data from API
  var categoriesDataMonth = fetch(`http://localhost:5000/get_all_categories/${currentMonth}/${currentYear}`)
  .then( response => response.json() )
  .then(data => {
    for (let i = 0; i < data.length; i++) {
      // console.log( data[i].category)
      // adding labels to the array
      categoriesLabelsMonth.push(data[i].category);
      categoriesTotalsMonth.push(data[i].category_total);
    }
  }
    // console.log(data.length) 
    )
}

getCategories(currentMonth,currentYear);

console.log(categoriesLabelsMonth)
console.log(categoriesTotalsMonth)

// plotting breakdown bar graph

var categoriesData = {
  labels: categoriesLabelsMonth,
  datasets: [{
    label: "Categories Breakdown Individual Comparison(Monthly)",
    backgroundColor: "#153d77",
    borderColor: 'rgb(255, 99, 132)',
    // data: [3000,5000],
    data: categoriesTotalsMonth,
  }]
};

var categoriesDataConfig = {
  type: 'bar',
  data: categoriesData,
  options: {}
};

var myChart1 = new Chart(
  document.getElementById("money-out-brkdwn-bar-month"),
  categoriesDataConfig
);


// below code will plot a graph for money out breakdown doughnut graph analysis

var categoriesData = {
  labels: categoriesLabelsMonth,
  datasets: [{
    label: "Categories Breakdown To Total Comparison(Monthly)",
    backgroundColor: "#153d77",
    borderColor: "#42BE9B",
    // data: [3000,5000],
    data : categoriesTotalsMonth
  }]
};

var categoriesDataConfig2 = {
  type: 'line',
  data: categoriesData,
  options: {}
};

var myChart2 = new Chart(
  document.getElementById("money-out-brkdwn-doughnut-month"),
  categoriesDataConfig2
);

