define(function() {
    return {
        init: function () {
            $(".search_widget").submit(function () {
                var form = $(this);
                $.ajax({
                    url: form.attr("action"),
                    type: form.attr("method"),
                    data: form.serialize(),
                    success: function (data) {
                        data = jQuery.trim(data);
                        if (data.length > 0) {
                            $(".search_results").removeClass("hidden");
                            $(".search_results", form).html(data);
                        } else {
                            $(".search_results").addClass("hidden");
                        }
                    }
                });
                return false;
            });
            $(".search_more").live("click", function () {
                var link = $(this);
                $.get(link.attr("href"), function (data) {
                    link.replaceWith(data);
                });
                return false;
            });
        }
    }
});
