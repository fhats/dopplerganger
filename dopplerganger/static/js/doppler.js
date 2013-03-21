function run() {
    var width = 960;
    var height = 500;

    var svg = d3.select("#showbox").insert("svg", ":first-child")
        .attr("width", width)
        .attr("height", height)
      .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(.55)")
      .append("g");

    var connection = new WebSocket('ws://' + window.location.host + '/dots');

    connection.onmessage = function(evt) {
        var point = JSON.parse(evt.data);
        svg.append("circle")
                .attr("cx", point.x)
                .attr("cy", point.y)
                .attr("r", 2.5);
    }

}
