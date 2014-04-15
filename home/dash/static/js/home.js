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
        url: '/api/search/',
        success: function(data){

            var plot_data = [];

            var max, min;

            $.each(data.results, function(i, v){
                if (i == 0 || v.value > max) max = v.value;
                if (i == 0 || v.value < min) min = v.value;
                plot_data.push([new Date(v.created_at), v.value])
            });

            max = max * 1.05;
            min = min * 0.95;

            var interactive_plot = $.plot(id, [plot_data], {
                grid: {
                    borderColor: "#f3f3f3",
                    borderWidth: 1,
                    tickColor: "#f3f3f3"
                },
                series: {
                    shadowSize: 0, // Drawing is faster without shadows
                    color: "#3c8dbc"
                },
                lines: {
                    color: "#3c8dbc"
                },
                yaxis: {
                    min: min,
                    max: max,
                    show: true
                },
                xaxis: {
                    show: true,
                    mode: "time"
                }
            });

        }
    });

}
