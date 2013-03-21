function run() {
    var width = 960;
    var height = 500;

    var svg = d3.select("#showbox").insert("svg", ":first-child")
        .attr("width", width)
        .attr("height", height)
      .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(.55)")
      .append("g");

    svg.append("circle")
            .attr("cx", 0)
            .attr("cy", 0)
            .attr("r", 2.5);

    var connection = new WebSocket('ws://' + window.location.host + '/dots');

    connection.onmessage = function(evt) {
        console.log(evt.data);
    }

}
