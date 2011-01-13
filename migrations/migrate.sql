INSERT INTO commitments_contributor (first_name, last_name, email, location_id, user_id, created, updated)
SELECT u.first_name, u.last_name, u.email, p.location_id, u.id, NOW(), NOW()
FROM auth_user u
LEFT JOIN rah_profile p ON u.id = p.user_id
LEFT JOIN commitments_contributor c ON u.id = c.user_id
WHERE c.id IS NULL;

INSERT INTO `messaging_message` (`id`,`name`,`subject`,`body`,`sends`,`message_timing`,`x_value`,`recipient_function`,`send_as_batch`,`batch_window`,`time_snap`,`minimum_duration`,`generic_relation_content_type_id`,`created`,`updated`)
VALUES
    (24,'You\'ve created a team','Organizing your Repower at Home team','{% extends \'rah/base_email.html\' %}\r\n{% block email_content %}\r\n<p>\r\nHi {{ recipient.first_name }},\r\n</p>\r\n\r\n<p>\r\n I’m Shira, the Field Director for Repower at Home. My job is to bring the enthusiasm for saving energy that you find on repowerathome.com into the real world by working with leaders like you.\r\n</p>\r\n\r\n<p>\r\nI see you recently created a team on repowerathome.com, <a href=”http://{{ domain }}{{ content_object.get_absolute_url }}”>{{ content_object}}</a>. Nice! Teams are a great way for  a community  to share ideas, compete with friends and work together to save energy. \r\n</p>\r\n\r\n<p>\r\nAs the team administrator, you can invite people to your team, moderate discussions and more by using the tools on your team’s page. <strong>Get started by inviting some friends to join your team</strong>. <a href=”http://{{ domain }}{{ content_object.get_absolute_url }}”>Try it out now</a>.\r\n</p> \r\n\r\n<p>\r\nRepower at Home teams often work to organize events in their communities, like <a href=”http://{{ domain }}/events/”>energy meetings</a> and challenges to recruit  <a href=”http://{{ domain }}/about-pledge/”>Trendsetters</a>. The Repower at Home field team can tell you more about these opportunities. To get in touch, drop us a line at <mailto:”field@repowerathome.com”>field@repowerathome.com</a>.  We’d love to hear your ideas for getting others energized about saving energy.\r\n</p>\r\n\r\n<p>\r\nHappy energy savings,<br />\r\nShira Miller<br />\r\nField Director, Repower at Home \r\n</p>\r\n{% endblock %}',0,'send_immediately',0,'lambda x: x.managers',0,NULL,NULL,NULL,NULL,'2011-01-13 09:44:23','2011-01-13 09:46:53');

INSERT INTO `messaging_message_content_types` (`id`,`message_id`,`contenttype_id`)
VALUES
    (88,24,30);

INSERT INTO `messaging_abtest` (`id`,`message_id`,`test_message_id`,`test_percentage`,`is_enabled`,`stream_id`,`created`,`updated`)
VALUES
    (23,24,NULL,0,1,1,'2011-01-13 09:55:11','2011-01-13 09:55:11');

