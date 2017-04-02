$(document).ready(function () {
    $("[data-plot]").each(function (i, wrapperEl) {
        var plotData = JSON.parse(wrapperEl.dataset.plot);

        var chartEl = document.createElement("div");
        wrapperEl.appendChild(chartEl);

        Plotly.newPlot(chartEl, [{
            x: plotData.data_x,
            y: plotData.data_y
        }], {
            height: 400,
            xaxis: {title: plotData.x_axis_title, showgrid: true},
            yaxis: {title: plotData.y_axis_title}
        });
    })
});
