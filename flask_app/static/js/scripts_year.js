// console.log("CONNECTED TO JS")

// YEARLY ANALYSIS
// get money in and money out values
var moneyIn = parseFloat($("#total-income").text())
// console.log(moneyIn)
var moneyOut = parseFloat($("#total-expenses").text())

// below code will plot a graph for money in - money out analysis
const totalLabels = [
    "Money In",
    "Money Out",
  ];

  const data = {
    labels: totalLabels,
    datasets: [{
      label: "Annual Money In/Money Out",
      backgroundColor: "#153d77",
      borderColor: 'rgb(255, 99, 132)',
      data: [moneyIn,moneyOut],
    }]
  };

  const config = {
    type: 'bar',
    data: data,
    options: {}
  };

  const myChart = new Chart(
    document.getElementById("money-graph"),
    config
  );

// below code will plot a graph for money out breakdown bar graph analysis

// gat current year 
var currentYear = parseInt($("#current-year").text())
// console.log(currentYear)

// this method get the categories data from the controller using API
var categoriesLabels = [];
var categoriesTotals = [];

function getCategories(year){
  // retrieving data from API
  var categoriesData = fetch(`http://localhost:5000/get_all_categories/${year}`)
  .then( response => response.json() )
  .then(data => {
    for (let i = 0; i < data.length; i++) {
      // console.log( data[i].category)
      // adding labels to the array
      categoriesLabels.push(data[i].category);
      categoriesTotals.push(data[i].category_total);
    }
  }
    // console.log(data.length) 
    )
}

getCategories(currentYear);

// console.log(categoriesLabels)
// console.log(categoriesTotals)

  var categoriesData = {
    labels: categoriesLabels,
    datasets: [{
      label: "Categories Breakdown Individual Comparison",
      backgroundColor: "#153d77",
      borderColor: 'rgb(255, 99, 132)',
      // data: [3000,5000],
      data: categoriesTotals,
    }]
  };

  var categoriesDataConfig = {
    type: 'bar',
    data: categoriesData,
    options: {}
  };

  var myChart1 = new Chart(
    document.getElementById("money-out-brkdwn-bar"),
    categoriesDataConfig
  );

// below code will plot a graph for money out breakdown doughnut graph analysis

var categoriesData = {
  labels: categoriesLabels,
  datasets: [{
    label: "Categories Breakdown To Total Comparison",
    backgroundColor: "#153d77",
    borderColor: "#42BE9B",
    // data: [3000,5000],
    data : categoriesTotals
  }]
};

var categoriesDataConfig2 = {
  type: 'line',
  data: categoriesData,
  options: {}
};

var myChart2 = new Chart(
  document.getElementById("money-out-brkdwn-doughnut"),
  categoriesDataConfig2
);

// MONTHLY ANALYSIS
// get money in and money out values
// var moneyInMonth = parseFloat($("#total-income-month").text())
// // console.log(moneyIn)
// var moneyOutMonth = parseFloat($("#total-expenses-month").text())

// // below code will plot a graph for money in - money out analysis
// var totalLabelsMonth = [
//     "Money In",
//     "Money Out",
//   ];

//   var dataMonth = {
//     labels: totalLabelsMonth,
//     datasets: [{
//       label: "Monthly Money In/Money Out",
//       backgroundColor: "#153d77",
//       borderColor: 'rgb(255, 99, 132)',
//       data: [moneyInMonth,moneyOutMonth],
//     }]
//   };

//   var configMonth = {
//     type: 'bar',
//     data: dataMonth,
//     options: {}
//   };

//   var myChartMonth = new Chart(
//     document.getElementById("money-graph-month"),
//     configMonth
//   );


//   // below code will plot a graph for money out breakdown bar graph analysis

// // gat current year 
// var currentYear = parseInt($("#current-year-month").text())
// // get current month
// var currentMonth = parseInt($("#current-month").text())
// // console.log(currentYear)
// // console.log(currentMonth)

// // this method get the categories data from the controller using API
// var categoriesLabelsMonth = [];
// var categoriesTotalsMonth = [];

// function getCategories(month,year){
//   // retrieving data from API
//   var categoriesDataMonth = fetch(`http://localhost:5000/get_all_categories/${month}/${year}`)
//   .then( response => response.json() )
//   .then(data => {
//     for (let i = 0; i < data.length; i++) {
//       // console.log( data[i].category)
//       // adding labels to the array
//       categoriesLabelsMonth.push(data[i].category);
//       categoriesTotalsMonth.push(data[i].category_total);
//     }
//   }
//     // console.log(data.length) 
//     )
// }

// getCategories(currentMonth,currentYear);

// console.log(categoriesLabelsMonth)
// console.log(categoriesTotalsMonth)




// this function make async call to the api to get the current weather for alamance
// var weather_api = config.OPEN_WEATHER_API_KEY;
async function getCurrentWeather(element){
    var cityName = "Alamance"
    // retrieving data from API
    var response = await fetch("http://api.openweathermap.org/data/2.5/weather?q=Alamance&APPID=52ec07192d14ae6c4d0605f05fec6566");
    // convert the data into JSON format.
    var weatherData = await response.json();

    var weather = {
        "temperature": weatherData.main.temp,
        "weatherDescription": weatherData.weather[0].description,
        "weatherIcon": weatherData.weather[0].icon
    }
    // console.log(weather)
    // adding the retrieved data to the webpage
    $("#temperature").html(weather.temperature)
    $("#weather-description").html(weather.weatherDescription)
    $("#weather-icon").attr("src", "https://openweathermap.org/img/w/"+weather.weatherIcon+".png")
    return weather;
}

getCurrentWeather()
// console.log(retrievedWeatherData)


