/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
require(["mods/comments", "mods/events", "mods/commitments"],
    function (comments, events, commitments) {
        require.ready(function () {
            var address = $("#event_address").text();
            var loc = $("#event_location").text();
            var geocoder = new google.maps.Geocoder();
            var myOptions = {
                zoom: 9,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                scrollwheel: false
            };
            var gmap = new google.maps.Map(document.getElementById("event_map"), myOptions);
            if (geocoder) {
                geocoder.geocode({ 'address': address + " " + loc}, function (results, status) {
                    if (status === google.maps.GeocoderStatus.OK) {
                        gmap.setCenter(results[0].geometry.location);
                        var marker = new google.maps.Marker({
                            map: gmap, 
                            position: results[0].geometry.location
                        });
                        var infowindow = new google.maps.InfoWindow({
                            content: "<h4>" + address + "</h4><h6>" + loc + "</h6>"
                        });
                        google.maps.event.addListener(marker, 'click', function () {
                            infowindow.open(gmap, marker);
                        });
                    }
                });
            }
            comments.setup();
            events.guests();
            commitments.card_setup();
        });
    });
