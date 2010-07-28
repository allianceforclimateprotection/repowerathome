{% load dated_static %}
/* <![CDATA[ */
$("body").append('<script type="text/javascript" charset="utf-8" src="{% dated_static 'js/jquery.flot.min.js' %}"></script>');
$("body").append('<!--[if IE]><script type="text/javascript" charset="utf-8" src="{% dated_static 'js/excanvas.min.js' %}"></script><![endif]-->');
$("#chart_dialog").remove();
$("body").append("<div id='chart_dialog'><div id='chart'></div></div>");
var chart_data = {{chart_data|safe}};
if (!chart_data['point_data'].length) {
    $("#chart").html('<img src="{% dated_static 'images/theme/chart_demo.png' %}" alt="sample chart"/>');
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
        legend: {show: true},
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
$('#chart_dialog').dialog({
    title: 'Activity Chart', modal: true, resizable: true, draggable: true, autoOpen: false, width: 630,
    buttons: { "Close": function() { $('#chart_dialog').dialog('close'); }}
});
$('#chart_dialog').dialog('open');
/* ]]> */