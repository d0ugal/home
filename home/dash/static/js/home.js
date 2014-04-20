function device_series_graph(device_id, series_id, id){

    fmt = function(date){
        // Convert the date into YYYY-MM-DD
        // btw, JavaScript date handling is horrible. It's basically broken.
        var yyyy = date.getFullYear();
        var mm = ('0' + (date.getMonth()+1)).slice(-2);
        var dd = ('0' + (date.getDate())).slice(-2);
        return yyyy + '-' + mm + '-' + dd;
    }

    var today = new Date();
    var tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);

    $.ajax({
        contentType: 'application/json',
        data: JSON.stringify({
            "start": fmt(today),
            "end": fmt(tomorrow),
            "device_id": device_id,
            "series_id": series_id,
        }),
        dataType: 'json',
        type: 'POST',
        url: '/api/graph/',
        success: function(data){

            var series = [];
            var max, min;

            $.each(data.data, function(x, result){

                var plot_data = [];

                $.each(result.values, function(i, v){
                    if (i == 0 || v.value > max) max = v.value;
                    if (i == 0 || v.value < min) min = v.value;
                    plot_data.push([new Date(v.created_at), v.value])
                });

                series.push(plot_data);

            });

            max = max * 1.05;
            min = min * 0.95;

            var interactive_plot = $.plot(id, series, {
                grid: {
                    hoverable: true,
                    borderColor: "#EBEFF7",
                    borderWidth: 1,
                    tickColor: "#EBEFF7"
                },
                series: {
                    shadowSize: 0,
                    lines: {
                        show: true
                    }
                },
                lines: {
                    fill: true,
                    fillColor: { colors: [{ opacity: 0.4 }, { opacity: 0.1}] }
                },
                yaxis: {
                    min: min,
                    max: max,
                    show: true
                },
                xaxis: {
                    show: true,
                    mode: "time"
                },
                colors: ["#3c8dbc", "#f56954"],
            });

            //Initialize tooltip on hover
            $("<div class='tooltip-inner' id='line-chart-tooltip'></div>").css({
                position: "absolute",
                display: "none",
                opacity: 0.8
            }).appendTo("body");

            console.log(id);

            $(id).bind("plothover", function(event, pos, item) {

                if (item) {
                    var x = item.datapoint[0].toFixed(2),
                            y = item.datapoint[1].toFixed(2);

                    $("#line-chart-tooltip").html(y)
                            .css({top: item.pageY + 5, left: item.pageX + 5})
                            .fadeIn(200);
                } else {
                    $("#line-chart-tooltip").hide();
                }

            });

        }
    });

};
