// d3.json("http://127.0.0.1:5000/countries", function(data) {
//     for (var i = 0; i < data.length; i++) {
//         console.log(data[i].country)
//     }
// })

function buildtable(query_string) {
    console.log(query_string)
    d3.json("http://127.0.0.1:5000/top_movies_table" + query_string).then((data) => {
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

function buildGraph(query_string) {
    d3.json("http://127.0.0.1:5000/top_movies_graph" + query_string).then((data) => {
        console.log(data)
        var graphData = data;
        //Create lists to collect data to graph.
        var cost = [];
        var revenue = [];
        var labels = [];
        //Get data for the plots
        for (var i = 0; i < data.length; i++) {
            if (graphData[i].budget.split(" ")[1]) {
                cost.push(graphData[i].budget.split(" ")[1]);
            }else{cost.push(0)}
            if (graphData[i].worldwide_gross_income.split(" ")[1]){
                revenue.push(graphData[i].worldwide_gross_income.split(" ")[1]);
            }else{revenue.push(0)}
            labels.push(graphData[i].title);
        }
        console.log(cost);
        console.log(revenue);
        console.log(labels);
        var trace1 = {
            x: labels,
            y: cost,
            type: 'bar',
            name: 'Cost',
            width: 0.5,
            marker: {
                color: 'red'
            }
        }
        var trace2 = {
            x: labels,
            y: revenue,
            type: 'bar',
            name: 'Revenue',
            width: 1.0,
            marker: {
                opacity: 0.5,
                color: 'green'
            }
        }
        var barLayout = {
            title: 'Financial Performance',
            xaxis: {
                tickangle: -45,
            },
            barmode: 'overlay'
        };
        var barData = [trace1, trace2];
        Plotly.newPlot("bar", barData, barLayout);
    }
    )
}

function optionChanged(filter_type, value) {
    //Check the value of each options
    var c_dropdown = d3.select("#selcountryDataset");
    var g_dropdown = d3.select("#selgenreDataset");
    var startyear_dropdown = d3.select("#selstartyearDataset");
    var endyear_dropdown = d3.select("#selendyearDataset");
    query_string = "?"
    //if value exists, build query string
    if (c_dropdown.property("value") && c_dropdown.property("value") != "All") {
        country = c_dropdown.property("value");
        query_string = query_string + "country=" + country + "&"
    }
    if (g_dropdown.property("value") && g_dropdown.property("value") != "All") {
        genre = g_dropdown.property("value");
        query_string = query_string + "genre=" + genre + "&"
    }
    if (startyear_dropdown.property("value")) {
        startyear = startyear_dropdown.property("value");
        query_string = query_string + "startyear=" + startyear + "&"
    }
    if (endyear_dropdown.property("value")) {
        endyear = endyear_dropdown.property("value");
        query_string = query_string + "endyear=" + endyear
    }
    // query_string="?"
    // if country:
    // query_string = query_string + "country=" + country + "&"
    // if genre:
    //query_string = query_string + "genre=" + genre + "&" 
    buildtable(query_string);
    buildGraph(query_string);
    // getDemoInfo(id);
}

function init() {

    var c_dropdown = d3.select("#selcountryDataset");


    d3.json("http://127.0.0.1:5000/countries").then((c_data) => {
        console.log(c_data)


        c_data.country.forEach(function (countries) {
            c_dropdown.append("option").text(countries).property("value");
        });

        query_string = "?startyear=1970" + "&endyear=2020"
        buildtable(query_string);
        buildGraph(query_string);

    });


    var g_dropdown = d3.select("#selgenreDataset");


    d3.json("http://127.0.0.1:5000/genres").then((g_data) => {
        console.log(g_data)


        g_data.genre.forEach(function (genres) {
            g_dropdown.append("option").text(genres).property("value");
        });

    });

    var startyear_dropdown = d3.select("#selstartyearDataset");

    d3.json("http://127.0.0.1:5000/year").then((startyear_data) => {
        console.log(startyear_data)


        startyear_data.year.forEach(function (years) {
            startyear_dropdown.append("option").text(years).property("value");
        });

        startyear_dropdown.property('value', '1970');

    });

    var endyear_dropdown = d3.select("#selendyearDataset");

    d3.json("http://127.0.0.1:5000/year").then((endyear_data) => {
        console.log(endyear_data)


        endyear_data.year.forEach(function (years) {
            endyear_dropdown.append("option").text(years).property("value");
        });

        endyear_dropdown.property('value', '2020');

    });
}


init();



