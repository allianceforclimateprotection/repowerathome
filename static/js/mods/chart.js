define(function () {
    return {
        $(".chart_link").click(function () {
            $.getScript($(this).attr("href"));
            return false;
        }
    }
});
