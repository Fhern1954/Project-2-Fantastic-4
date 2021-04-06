// d3.json("http://127.0.0.1:5000/countries", function(data) {
//     for (var i = 0; i < data.length; i++) {
//         console.log(data[i].country)
//     }
// })

function buildtable(query_string) {
    console.log(query_string)
    d3.json("http://127.0.0.1:5000/top_movies" + query_string).then((data)=> {
        console.log(data)
        
        var tableData = data;


        // Get a reference to the table body
        var tbody = d3.select("tbody");
        
        tbody.html("");

        data.forEach(item => {
            var row = tbody.append("tr");
            Object.entries(item).forEach(([key, value]) => {
              var cell = row.append("td");
              cell.text(value);
            });
        });
        // Object.entries(data => {
        //     console.log(data);
        //     var row = tbody.append("tr");
        //     Object.entries(data).forEach(([key, value]) => {
        //       var cell = row.append("td");
        //       cell.text(value);
        //     });
          
        // });    
        });
    }

function optionChanged(id) {
        //Check the value of each options
        //if value exists, build query string
        // query_string="?"
        // if country:
            // query_string = query_string + "country=" + country + "&"
        // if genre:
            //query_string = query_string + "genre=" + genre + "&" 
        buildtable(query_string);
        // getDemoInfo(id);
    } 

function init() {
         
    var c_dropdown = d3.select("#selcountryDataset");
    
        
    d3.json("http://127.0.0.1:5000/countries").then((c_data)=> {
        console.log(c_data)
    
            
        c_data.country.forEach(function(countries) {
            c_dropdown.append("option").text(countries).property("value");
            });

        c_dropdown.property('value','USA');

        buildtable("USA");      
    
        });
        

    var g_dropdown = d3.select("#selgenreDataset");
    
        
    d3.json("http://127.0.0.1:5000/genres").then((g_data)=> {
        console.log(g_data)
        
                
        g_data.genre.forEach(function(genres) {
            g_dropdown.append("option").text(genres).property("value");
                });
        
        });

    var startyear_dropdown = d3.select("#selstartyearDataset"); 
    
    d3.json("http://127.0.0.1:5000/year").then((startyear_data)=> {
        console.log(startyear_data)
        
                
        startyear_data.year.forEach(function(years) {
            startyear_dropdown.append("option").text(years).property("value");
                });

                startyear_dropdown.property('value','2019');        
        
        });

    var endyear_dropdown = d3.select("#selendyearDataset"); 
    
        d3.json("http://127.0.0.1:5000/year").then((endyear_data)=> {
            console.log(endyear_data)
            
                    
            endyear_data.year.forEach(function(years) {
                endyear_dropdown.append("option").text(years).property("value");
                    });

                endyear_dropdown.property('value','2020');          
            
            });    
}

       
init();

  

