// the code below changes all numeric month to words
function numericMonthToWord(){
    var jNumericMonth = $(".numeric-month");

    var numericMonth = null;
    
    if(jNumericMonth.text()[0] != jNumericMonth.text()[1]){
        numericMonth = jNumericMonth.text().substring(0,2)
    }else{
        numericMonth = jNumericMonth.text()[0]
    }
    // var numericMonth = parseInt(jNumericMonth.text()[0]) 
    console.log(numericMonth);
    // month dictionary
    const months = {
        1 : "January",
        2 : "February",
        3 : "March",
        4 : "April",
        5 : "May",
        6 : "June",
        7 : "July",
        8 : "August",
        9 : "September",
        10 : "October",
        11 : "November",
        12 : "December"          
    }

    // iterate through the object
    for (let keyNumericMonth in months) {
        if (numericMonth == keyNumericMonth){
            // set word month
            jNumericMonth.html(months[keyNumericMonth])
            // return months[keyNumericMonth]
        }
    }
  }
  numericMonthToWord()
//   console.log(numericMonthToWord());

// the code below opens and closes side nav bar
function openNav() {
    document.getElementById("side-navigation-wrapper").style.width = "250px";
    document.getElementById("main-content").style.marginLeft = "250px";
  }
  
function closeNav() {
    document.getElementById("side-navigation-wrapper").style.width = "0";
    document.getElementById("main-content").style.marginLeft= "0";
  }