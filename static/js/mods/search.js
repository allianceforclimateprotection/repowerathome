/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
define(function () {
    return {
        init_widget: function () {
            var form = $('.search_widget');
            var widget = $('#search_widget_input').autocomplete({
                source: function (req, res) {
                    $.ajax({
                        url: form.attr('action'),
                        dataType: 'json',
                        data: {
                            search: req.term,
                            format: 'json'
                        },
                        success: function (data) {
                            res(data);
                        }
                    });
                },
                focus: function (event, ui) {
                    this.value = ui.item.label;
                    return false;
                },
                select: function (event, ui) {
                    window.location = ui.item.url;
                    return false;
                },
                minLength: 2
            });
            /*jslint nomen: false*/
            widget.data('autocomplete')._renderItem = function (ul, item) {
            /*jslint nomen: true*/
                return $('<li/>')
                    .data('item.autocomplete', item)
                    .append($('<a/>', {
                        href: item.url,
                        text: item.label
                    }))
                    .appendTo(ul);
            };
            /*jslint nomen: false*/
            widget.data('autocomplete')._renderMenu = function (ul, items) {
            /*jslint nomen: true*/
                var self = this;
                if (items.length) {
                    $.each(items, function (index, item) {
                        self._renderItem(ul, item);
                    });
                } else {
                    return $('<li/>', {
                        text: 'No results'
                    })
                    .appendTo(ul);
                }
            };
            widget.data('autocomplete')._response = function (content) {
                content = this._normalize( content );
                this._suggest( content );
                this._trigger( "open" );
                this.element.removeClass( "ui-autocomplete-loading" );
            };
            return widget;
        }
    };
});
