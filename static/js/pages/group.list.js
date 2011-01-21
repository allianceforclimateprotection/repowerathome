/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
require(["libs/jquery.ui", "mods/search"],
    function (ui, search) {
        var widget = search.init_widget();
        /*jslint nomen: false*/
        widget.data('autocomplete')._renderItem = function (ul, item) {
        /*jslint nomen: true*/
            return $('<li/>')
                .data('item.autocomplete', item)
                .append($('<img/>', {
                    'class': 'group_image',
                    src: item.img,
                    alt: 'group image',
                    height: '30',
                    width: '30'
                }))
                .append($('<a/>', {
                    href: item.url,
                    text: item.label
                }))
                .append($('<br/>', {
                    'class': 'clear'
                }))
                .appendTo(ul);
        };
    });
