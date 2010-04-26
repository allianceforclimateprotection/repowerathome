/* <![CDATA[ */
$("body").append('<script type="text/javascript" charset="utf-8" src="{{ MEDIA_URL }}js/jquery.flot.min.js"></script>');
$("body").append('<!--[if IE]><script type="text/javascript" charset="utf-8" src="{{MEDIA_URL}}js/excanvas.min.js"></script><![endif]-->');
$("#chart_dialog").remove();
$("body").append("<div id='chart_dialog'><div id='chart'></div></div>");
var chart_data = {{chart_data|safe}};
if (!chart_data['point_data'].length) {
    $("#chart").html('<img src="' + media_url + 'images/theme/chart_demo.png" alt="sample chart"/>');
} else {
    // Add an additional datapoint at the beginning to represent 0 points
    yesterday = chart_data['point_data'][0][0] - (60*60*24*1000*1);
    chart_data['point_data'].unshift([yesterday, 0]);

    var plot = $.plot($("#chart"), [ { data: chart_data['point_data'] }], {
        series: {
            lines: { show: true },
            points: { show: true, radius: 10 },
            shadowSize: 5
        },
        grid: { hoverable: true, clickable: true, backgroundColor: { colors: ["#DDD", "#FFF"] } },
        legend: {show: false},
        xaxis: {mode: "time",autoscaleMargin: 0.1,  minTickSize: [1, "day"]},
        yaxis: {min: 0, tickDecimals: 0, autoscaleMargin: 0.6}
    });
    $("#chart").bind("plothover", function (event, pos, item) {
        if (item) {
            showTooltip(item.pageX, item.pageY, item.dataIndex);
        }
        else {
            $(".chart_tooltip").remove();
        }
    });
    function showTooltip(x, y, index) {
        // The first datapoint is an artificial point representing zero points, so it doesn't need a tooltip
        if (index == 0){
            return;
        }
        $('<div class="chart_tooltip">' + chart_data["tooltips"][index-1] + '</div>').css( {
            position: 'absolute',
            display: 'none',
            top: y - 18,
            left: x + 5
        }).appendTo("body").fadeIn(300);
    }
}
/* ]]> */