d3.json("localhost:5000/top_movies/USA/Drama", function(data) {
    for (var i = 0; i < data.length; i++) {
        console.log(data[i].title)
    }
})