// function loadHomepage(event=null)
// {
//   console.log(event);

//   let dropdownMenu = document.getElementById("selDataset");
//   let shortLocation;
//   if (dropdownMenu == null)  {
//     shortLocation = "UCLA";
//   }
//   else
//   {
//     shortLocation = dropdownMenu.options[dropdownMenu.options.selectedIndex].value;
//   }

d3.json("/data2").then(function(data){

  // Set values for dropdown menu
  let campusLocations = data["locations"];
  var dropdownOptions = [];
  for (let i = 0; i < campusLocations.length; i++) {
    let campus = campusLocations[i];
    let campusName = campus["locationName"];
    let shortName = campus["shortName"];
      
    dropdownOptions.push({"shortName": shortName, "campusName": campusName});
  }

  // Use D3 to select dropdown menu
  var dropdown = d3.select("#selDataset");

  // Append dropdown options to menu
  dropdownOptions.forEach(option => {
    dropdown.append("option").text(option["campusName"]).attr("value", option["shortName"]).attr("name", option["shortName"]);
  });

// do not use data anymore
});

d3.json("/data2").then(function(locationData){

  // Your weather this week
  // Weekly forecast
  let dailyForecasts = locationData["dailyForecasts"];
  var forecastPeriods = [];
  for (let i = 0; i < dailyForecasts.length; i++) {
    let period = dailyForecasts[i];
    let periodResponseName = period["daily_responseName"];
    let periodStartDate = period["daily_startDate"];
    let periodIcon = period["daily_icon"];
    let periodShortForecast = period["daily_shortForecast"];
    let periodTemperature = period["daily_temperature"];
    let periodDetailedForecast = period["daily_detailedForecast"];
    
    forecastPeriods.push({"periodResponseName": periodResponseName, "periodStartDate": periodStartDate, "periodIcon": periodIcon, "periodShortForecast": periodShortForecast, "periodTemperature": periodTemperature, "periodDetailedForecast": periodDetailedForecast});
  }

  // Period Forecasts
  var weeklyForecast = d3.select("#period-forecasts");

  for (let i = 0; i < forecastPeriods.length; i++) {
    console.log(forecastPeriods[i]["periodIcon"]);
    let auxp = weeklyForecast.append("p");
    auxp.append("h4").text(forecastPeriods[i]["periodResponseName"] + " (" + forecastPeriods[i]["periodStartDate"] + ")");
    auxp.append("img").attr("src", forecastPeriods[i]["periodIcon"]);
    auxp.append("div").text(forecastPeriods[i]["periodShortForecast"])
    auxp.append("div").text(forecastPeriods[i]["periodTemperature"] + "° F");
    auxp.append("div").text(forecastPeriods[i]["periodDetailedForecast"])
    auxp.append("hr").attr("class", "weather-divider")
    } 


  // Leaflet map
  let lat = parseFloat(locationData["locations"][0]["latitude"])
  let lon = parseFloat(locationData["locations"][0]["longitude"])
  console.log(`${lat}, ${lon}`)

  var myMap = L.map('map').setView([lat, lon], 15);


  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/light-v10',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoibmFwcHl0cmFpbHMiLCJhIjoiY2t1dXBvYXJ1MWlhNzJ1cGphZXJ3MHJ4diJ9.r-J1-mrEKBLhc2V3Kw5wXA'
  }).addTo(myMap);


  // Then move the map
  myMap.panBy(new L.Point(0, -75), {animate: false});

  let currentDateObj = new Date().toJSON().slice(0, 10);
  let currentDate =  currentDateObj.toString()
  let currentHour = new Date().getHours();
  let legendTitle = d3.select("#legend-title");
  if (currentHour >= 6 && currentHour < 18) {
    isDay = true;
    legendTitle.append("strong").text("Today's");
    legendTitle.append("br");
    legendTitle.append("strong").text("Forecast");
  }
  else {
    isDay = false;
    legendTitle.append("strong").text("Tonight's");
    legendTitle.append("br");
    legendTitle.append("strong").text("Forecast");
  }
  
  for (let i=0; i < dailyForecasts.length; i++) {
    var daily_startDate = dailyForecasts[i]["daily_startDate"];
    var daily_endDate = dailyForecasts[i]["daily_endDate"];
    var daily_minWindSpeed = dailyForecasts[i]["daily_minWindSpeed"];
    var daily_maxWindSpeed = dailyForecasts[i]["daily_maxWindSpeed"];
    var daily_isDaytime = dailyForecasts[i]["daily_isDaytime"];
    // var forecastWindSpeed = 0
    // var forecastTemp = 0

    // if (currentDate == daily_endDate) {
    //   console.log("A string");
    //   console.log(daily_minWindSpeed);
    //   console.log(parseInt(daily_maxWindSpeed));
    //   console.log(currentDate)
    //   console.log(daily_endDate);
    //   // console.log(daily_startDate);
    //   console.log(daily_isDaytime);
    // }

    if (isDay == true) {
      if (daily_isDaytime == true && daily_endDate == currentDate && daily_maxWindSpeed != "None") {
        console.log("Day: First if statement")
        var forecastWindSpeed = parseInt(daily_maxWindSpeed);
        var forecastTemp = dailyForecasts[i]["daily_temperature"];
        console.log(dailyForecasts[i]["daily_responseNumber"])
      }
      else if (daily_isDaytime == true && daily_endDate == currentDate && daily_maxWindSpeed == "None") {
        console.log("Day: Second if statement")
        var forecastWindSpeed = daily_minWindSpeed;
        var forecastTemp = dailyForecasts[i]["daily_temperature"];
      }
      else {
        console.log("Day: Else statement")
        // forecastWindSpeed = "FWS"
        // forecastTemp = "FT"
      }
    }

    else {
      if (daily_isDaytime == false && daily_startDate == currentDate && daily_maxWindSpeed != "None") {
        console.log("Night: First if statement")
        var forecastWindSpeed = parseInt(daily_maxWindSpeed);
        var forecastTemp = dailyForecasts[i]["daily_temperature"];
      }
      else if (daily_isDaytime == false && daily_startDate == currentDate && daily_maxWindSpeed == "None") {
        console.log("Night: Second if statement")
        var forecastWindSpeed = daily_minWindSpeed;
        var forecastTemp = dailyForecasts[i]["daily_temperature"];
      }
      else if (daily_isDaytime == false && daily_endDate == currentDate && daily_maxWindSpeed != "None") {
        console.log("Night: Third if statement")
        var forecastWindSpeed = parseInt(daily_maxWindSpeed);
        var forecastTemp = dailyForecasts[i]["daily_temperature"];
      }
      else if (daily_isDaytime == false && daily_endDate == currentDate && daily_maxWindSpeed == "None") {
        console.log("Night: Fourth if statement")
        var forecastWindSpeed = daily_minWindSpeed;
        var forecastTemp = dailyForecasts[i]["daily_temperature"];
      }
      else {
        console.log("Night: Else statement")
        // forecastWindSpeed = "FWS"
        // forecastTemp = "FT"
      }
    }  

      // console.log(currentDate);
    console.log(forecastWindSpeed);
    console.log(forecastTemp);

  }


  // The function that will determine the color of a neighborhood based on the borough that it belongs to
  function chooseColor(windSpeed) {
    if (windSpeed < 1) return "palegreen";
    else if (windSpeed <= 3) return "lightgreen";
    else if (windSpeed <= 7) return "#70DB70";
    else if (windSpeed <= 12) return "#43E043";
    else if (windSpeed <= 18) return "lawngreen";
    else if (windSpeed <= 24) return "greenyellow";
    else if (windSpeed <= 31) return "yellow";
    else if (windSpeed <= 38) return "gold";
    else if (windSpeed <= 46) return "orange";
    else if (windSpeed <= 54) return "tomato";
    else if (windSpeed <= 63) return "orangered";
    else if (windSpeed <= 75) return "red";
    else return "maroon";
  }

  function chooseFillColor(temperature) {
    if (temperature < 25) return "darkblue";
    else if (temperature <= 34) return "cornflowerblue";
    else if (temperature <= 44) return "paleturquoise";
    else if (temperature <= 54) return "aquamarine";
    else if (temperature <= 64) return "springgreen";
    else if (temperature <= 74) return "limegreen";
    else if (temperature <= 84) return "yellowgreen";
    else if (temperature <= 94) return "goldenrod";
    else if (temperature <= 105) return "darkorange";
    else return "firebrick";
  }



  //   if (borough == "Brooklyn") return "yellow";
  //   else if (borough == "Bronx") return "red";
  //   else if (borough == "Manhattan") return "orange";
  //   else if (borough == "Queens") return "green";
  //   else if (borough == "Staten Island") return "purple";
  //   else return "black";

  // Creating a new marker:
  var campus = L.circle([lat, lon], {
    color: chooseColor(forecastWindSpeed),
    weight: 15,
    stroke: true,
    fillColor: chooseFillColor(forecastTemp),
    fillOpacity: 0.5,
    radius: 550
  }).addTo(myMap);

  // Binding a popup to the circle
  campus.bindPopup("<center><b>Current<br>Conditions</b><br><img src='https://api.weather.gov/icons/land/day/skc?size=medium'><br><hr><b>Sunny</b><br>Temperature: 75° F<br>Wind Speed: 5mph<br>Wind Direction: NNW</center>");



// do not use localData anymore
});

// }


// loadDropdown();
// loadHomepage();

// // let dropdownMenu = document.getElementById("selDataset")
// // dropdownMenu.addEventListener("change", loadHomepage);

// document.getElementById("selDataset").addEventListener("change", function(event){
//   // console.log(event)
//   console.log(dropdownMenu.options[dropdownMenu.options.selectedIndex].value)
// })

