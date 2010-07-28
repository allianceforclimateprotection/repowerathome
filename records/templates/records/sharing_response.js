/* <![CDATA[ */
{% if is_shared %}
    var message_html = '{% filter escapejs %}{% include "_messages.html" %}{% endfilter %}'
    rah.mod_messages.init(message_html);
{% else %}
    rah.mod_facebook_connect.authorize();
{% endif %}
/* ]]> */