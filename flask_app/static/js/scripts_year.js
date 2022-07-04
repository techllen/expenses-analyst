// console.log("CONNECTED TO JS")

// YEARLY ANALYSIS
// get money in and money out values
var moneyIn = parseFloat($("#total-income").text())
// console.log(moneyIn)
var moneyOut = parseFloat($("#total-expenses").text())

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

var currentYearString = toString(currentYear)

// BAR GRAPH

var moneyGraphArray = [['Year', 'Money In', 'Money Out'],[currentYear,moneyIn,moneyOut]]
google.charts.load('current', {'packages':['bar']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable(
          moneyGraphArray
        );

        var options = {
          chart: {
            title: 'Money In/Money Out',
            // subtitle: 'Sales, Expenses, and Profit: 2014-2017',
          },
          bars: 'vertical' // Required for Material Bar Charts.
        };

        var chart = new google.charts.Bar(document.getElementById('money-graph'));

        chart.draw(data, google.charts.Bar.convertOptions(options));
      }


      $(window).resize(function(){
          drawChart();
      });

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


