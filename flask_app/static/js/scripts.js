// console.log("CONNECTED TO JS")


// get money in and money out values
var moneyIn = parseFloat($("#total-income").text())
// console.log(moneyIn)
var moneyOut = parseFloat($("#total-expenses").text())

// below code will plot a graph for money in - money out analysis
const labels = [
    "Money In",
    "Money Out",
  ];

  const data = {
    labels: labels,
    datasets: [{
      label: "Money In/Money Out",
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

const labels1 = [
    "Money In",
    "Money Out",
  ];

  const data1 = {
    labels: labels1,
    datasets: [{
      label: "Money In/Money Out",
      backgroundColor: "#153d77",
      borderColor: 'rgb(255, 99, 132)',
      data: [3000,5000],
    }]
  };

  const config1 = {
    type: 'bar',
    data: data1,
    options: {}
  };

  const myChart1 = new Chart(
    document.getElementById("money-out-brkdwn-bar"),
    config1
  );

// below code will plot a graph for money out breakdown doughnut graph analysis
const labels2 = [
    "Money In",
    "Money Out",
  ];

  const data2 = {
    labels: labels2,
    datasets: [{
      label: "Money In/Money Out",
      backgroundColor: "#153d77",
      borderColor: "#42BE9B",
      data: [3000,5000],
    }]
  };

  const config2 = {
    type: 'doughnut',
    data: data2,
    options: {}
  };

  const myChart2 = new Chart(
    document.getElementById("money-out-brkdwn-doughnut"),
    config2
  );



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

