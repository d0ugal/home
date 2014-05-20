function device_series_graph(device_id, series_id, id){

    fmt = function(date){
        // Convert the date into YYYY-MM-DD HH:MM
        // btw, JavaScript date handling is horrible. It's basically broken.
        var yyyy = date.getFullYear();
        var mm = ('0' + (date.getMonth()+1)).slice(-2);
        var dd = ('0' + (date.getDate())).slice(-2);
        var hh = ('0' + (date.getHours())).slice(-2);
        var MM = ('0' + (date.getMinutes())).slice(-2);
        var ss = ('0' + (date.getSeconds())).slice(-2);
        return yyyy + '-' + mm + '-' + dd + ' ' + hh + ':' + MM + ':' + ss;
    }

    var today = new Date();
    var yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);

    $.ajax({
        contentType: 'application/json',
        data: JSON.stringify({
            "start": fmt(yesterday),
            "end": fmt(today),
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

                $.each(result, function(graph_name, points){

                    var plot_data = [];

                    $.each(points, function(i, point){

                        var date = point[0];
                        var value = point[1];

                        if (plot_data.length == 0 || value > max) max = value;
                        if (plot_data.length == 0 || value < min) min = value;

                        plot_data.push([new Date(date), value]);

                    })

                    series.push(plot_data);

                });


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

            $(id).bind("plothover", function(event, pos, item) {

                if (item) {
                    var x = item.datapoint[0].toFixed(2),
                            y = item.datapoint[1].toFixed(2);

                    var x_str = fmt(new Date(x * 1));

                    $("#line-chart-tooltip").html(x_str + ": <br/> " + y)
                            .css({top: item.pageY + 5, left: item.pageX + 5})
                            .fadeIn(200);
                } else {
                    $("#line-chart-tooltip").hide();
                }

            });

        }
    });

};

$(function(){

    $(".webcam-image").each(function(i, val){

        var original = val.src;

        var reloader = function(){
            var new_src = original + "?z=" + new Date().getTime();
            console.log(new_src);
            val.src = new_src;
            setTimeout(reloader, 10000);
        }

        reloader()

    });

});
