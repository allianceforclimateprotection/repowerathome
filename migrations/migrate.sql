ALTER TABLE messaging_message ADD generic_relation_content_type_id int(11) AFTER minimum_duration;
UPDATE messaging_message SET generic_relation_content_type_id=48 WHERE name='Event invite';
UPDATE messaging_message SET generic_relation_content_type_id=30 WHERE name='Team invite';

INSERT INTO `messaging_message` (`id`,`name`,`subject`,`body`,`sends`,`message_timing`,`x_value`,`recipient_function`,`send_as_batch`,`batch_window`,`time_snap`,`minimum_duration`,`generic_relation_content_type_id`,`created`,`updated`)
VALUES	
    (18,'Once you create an event','Your Repower at Home event','{% extends \'rah/base_email.html\' %}\r\n{% block email_content %}\r\n<p>Hi {{ recipient.first_name }},</p>\r\n\r\n<p>\r\nThanks for hosting a Repower at Home event on<br/>\r\n{{ content_object.when|date }} at {{ content_object.start|time }}.  Because of leaders like you,<br/>\r\nwe\'re on our way to meeting our energy savings goal of 7 million pounds of coal.\r\n</p>\r\n\r\n<p>\r\n<b>Your next step is to invite guests.  <a href=\"http://{{ domain }}{% url event-guests content_object.id %}\">Get started now.</a></b>\r\n</p>\r\n\r\n<p>\r\nUse <a href=\"{{ content_object.get_absolute_url }}\"> your event\'s page</a> to manage every aspect of<br/>\r\nyour event.  On the event\'s page, you can:\r\n<ul>\r\n<li>Check the status of your guests</li>\r\n<li>Make someone else a co-host</li>\r\n<li>Send reminder and announcement emails to your whole guest list</li>\r\n<li>Check off steps on your way to the event</li>\r\n</ul>\r\n</p>\r\n\r\n<p>\r\nAfter your event, you\'ll be able to enter your guests\' commitments on the events<br/>\r\npage.  This will pre-load their accounts, allowing them to start saving energy right<br/>\r\naway.\r\n</p>\r\n\r\n<p>\r\nOn this call you\'ll learn more about Repower at Home and how you can be part of the movement. <a href=\'http://bit.ly/clk2Kz\'>Click here to RSVP</a>. If you have questions about the call or how you can get involved, contact Brian Ward at brian.ward@climateprotect.org, or call (202) 567-6800.\r\n</p>\r\n\r\n<p>\r\nCheers,<br/>\r\nThe Repower at Home team\r\n</p>\r\n{% endblock %}',0,'send_immediately',0,'lambda x: x.creator',0,NULL,NULL,NULL,NULL,'2010-09-13 10:43:34','2010-09-13 16:10:40'),
    (19,'1 week after after you create an event','Guest list update for your Repower at Home event','{% extends \'rah/base_email.html\' %}\r\n{% block email_content %}\r\n<p>\r\nHi {{ recipient.first_name }},\r\n</p>\r\n\r\n<p>\r\nSo far, {{ content_object.confirmed_guests.count }} {{ content_object.confirmed_guests.count|pluralize:\"person,people\" }} have responded to you event invitation, but your still waiting on<br/>\r\n{{ content_object.outstanding_invitations }} other{{ content_object.outstanding_invitations|pluralize}}:\r\n{% if content_object.outstanding_invitations %}\r\n<ul>\r\n{% for guest in content_object.guests_that_have_not_responded %}\r\n<li>{{ guest }}</li>\r\n{% endfor %}\r\n</ul>\r\n{% endif %}\r\nTime to give these holdouts a gentle nudge in the right direction. <a href=\"http://{{ domain }}{% url event-reminder content_object.id %}?guests={{ event.guests_no_response_id_list }}\">Click here to send them a reminder email</a>.\r\n</p>\r\n\r\n<p>\r\nSome people overlook emails in their inbox.  <strong>Calling these guests can go a long way</strong>.  If you\'ve already spoken to them, you can <a href=\"http://{{ domain }}{% url event-guests content_object.id %}\">update their RSVP status on your event\'s page.</a>\r\n</p>\r\n\r\n<p>\r\nCheers,<br/>\r\nThe Repower at Home team\r\n</p>\r\n{% endblock %}',0,'after_start',120,'lambda x: x.hosts()',0,NULL,'11:00:00',240,NULL,'2010-09-13 12:58:28','2010-09-13 16:10:16'),
    (20,'1 week before the event','Finish your preparations for your Repower at Home event','{% extends \'rah/base_email.html\' %}\r\n{% block email_content %}\r\n<p>\r\nHi {{ recipient.first_name }},\r\n</p>\r\n\r\n<p>\r\nYour event is on {{ content_object.when|date }}, one week from today!  {{ content_object.confirmed_guests.count }} of your guests have<br/>\r\nconfirmed their attendance, but your still waiting to hear from {{ content_object.outstanding_invitations }} more.\r\n<ul>\r\n<li><a href=\"http://{{ domain }}{% url event-reminder content_object.id %}?guests={{ event.guests_no_response_id_list }}\">Send a reminder email to all the guests who are coming</a></li>\r\n<li><a href=\"http://{{ domain }}{% url event-announcement content_object.id %}?guests={{ event.guests_no_response_id_list }}\">Encourage holdouts to RSVP</a></li>\r\n</ul>\r\n</p>\r\n\r\n<p>\r\nCheers,<br/>\r\nThe Repower at Home team\r\n</p>\r\n{% endblock %}',0,'before_end',168,'lambda x: x.hosts()',0,NULL,'11:00:00',504,NULL,'2010-09-13 13:15:06','2010-09-13 16:11:14'),
    (21,'48 hours before the event','Your Repower at Home event is less than 2 days away!','{% extends \'rah/base_email.html\' %}\r\n{% block email_content %}\r\n<p>\r\nHi {{ content_object.first_name }},\r\n</p>\r\n\r\n<p>\r\nYour event is right around the corner! It\'s an exciting time,<br/>\r\nbut don\'t forget to nail down the final details.\r\n</p>\r\n\r\n<p>\r\nFirst, <a href=\"http://{{ domain }}{% url event-reminder content_object.id %}?guests={{ event.guests_no_response_id_list }}\">send one last reminder to your guests</a>.\r\n</p>\r\n\r\n<p>\r\nNext, make sure to print out all of your <a href=\"http://{{ domain }}/hosting/\">meeting materials</a>\r\n</p>\r\n\r\n<p>\r\nHave a great time at the event! We\'ll see you again soon after the event when you enter your guests\' commitments.\r\n</p>\r\n\r\n<p>\r\nCheers,<br/>\r\nThe Repower at Home team\r\n</p>\r\n{% endblock %}',0,'before_end',48,'lambda x: x.hosts()',0,NULL,'11:00:00',168,NULL,'2010-09-13 13:55:02','2010-09-13 16:11:33'),
    (22,'Day after the event','Enter your guests\' commitments','{% extends \'rah/base_email.html\' %}\r\n{% block email_content %}\r\n<p>\r\nHi {{ recipient.first_name }},\r\n</p>\r\n\r\n<p>\r\nGood work organizing your event yesterday! Because of your leadership, a whole<br/>\r\nbunch of new people are now engaged in the movement for a cleaner, better world.\r\n</p>\r\n\r\n<p>\r\nHelp your guests get to the next level.  <a href=\"http://{{ domain }}{% url event-commitments content_object.id %}\">Enter their commitments</a> from your<br/>\r\nevent.  This will remind them of their goals and get them motivated.  The sooner you <br/>\r\nenter the commitments, the sooner they can start saving energy.\r\n</p>\r\n\r\n<p>\r\nYou can also take this opportunity to <a href=\"http://{{ domain }}{% url group_list %}\">invite your guests to a team</a>.  <a href=\"http://{{ domain }}{% url group_list %}\">Teams</a> are<br/>\r\na great way to keep in touch with your guests and plan future projects as a group.\r\n</p>\r\n\r\n<p>\r\nCheers,<br/>\r\nThe Repower at Home team\r\n</p>\r\n{% endblock %}',0,'after_end',24,'lambda x: x.hosts()',0,NULL,'11:00:00',NULL,NULL,'2010-09-13 16:09:09','2010-09-13 16:09:09'),
    (23,'Day before the event','{{ content_object.creator.first_name }}\'s event is tomorrow!','<p>\r\nHey {{ recipient.first_name }},\r\n</p>\r\n\r\n<div>\r\nYou\'re all set to attend {{ content_object.creator.first_name }}\'s event tomorrow:\r\n<div style=\"margin-left: 20px;\">\r\n<i>Location:</i>\r\n<span>{{ content_object.place_name }}</span><br/>\r\n<span style=\"margin-left: 65px;\">{{ content_object.where }}</span><br/>\r\n<span style=\"margin-left: 65px;\">{{ content_object.location.place }}, {{ content_object.location.st }} {{ content_object.location.zipcode }}</span>\r\n</div>\r\n<div style=\"margin-left: 20px;\">\r\n<i>Time:</i>\r\n<span>{{ content_object.start|time }}</span>\r\n</div>\r\n<div style=\"margin-left: 20px;\">\r\n<i>Date:</i>\r\n<span>{{ content_object.when|date }}</span>\r\n</div>\r\n</div>\r\n\r\n<p>\r\nCheers,<br/>\r\nThe Repower at Home team\r\n</p>',0,'before_end',24,'lambda x: x.attendees()',0,NULL,'11:00:00',NULL,NULL,'2010-09-14 15:24:10','2010-09-14 15:24:10');

INSERT INTO `messaging_abtest` (`id`,`message_id`,`test_message_id`,`test_percentage`,`is_enabled`,`stream_id`,`created`,`updated`)
VALUES
	(16,18,NULL,0,1,13,'2010-09-13 16:13:07','2010-09-13 16:13:07'),
	(17,19,NULL,0,1,13,'2010-09-13 16:13:14','2010-09-13 16:13:14'),
	(18,20,NULL,0,1,13,'2010-09-13 16:13:20','2010-09-13 16:13:20'),
	(19,21,NULL,0,1,13,'2010-09-13 16:13:24','2010-09-13 16:13:24'),
	(20,22,NULL,0,1,13,'2010-09-13 16:13:29','2010-09-13 16:13:29'),
	(21,23,NULL,0,1,13,'2010-09-14 16:08:48','2010-09-14 16:08:48');

CREATE TABLE `messaging_message_content_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message_id` int(11) NOT NULL,
  `contenttype_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `message_id` (`message_id`,`contenttype_id`),
  KEY `messaging_message_content_types_38373776` (`message_id`),
  KEY `messaging_message_content_types_a184c428` (`contenttype_id`),
  CONSTRAINT `contenttype_id_refs_id_ad1ed89d` FOREIGN KEY (`contenttype_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `message_id_refs_id_7c4db37d` FOREIGN KEY (`message_id`) REFERENCES `messaging_message` (`id`)
) DEFAULT CHARSET=utf8;

INSERT INTO `messaging_message_content_types` (`id`,`message_id`,`contenttype_id`)
VALUES
	(1,1,43),
	(2,1,51),
	(3,2,43),
	(4,2,51),
	(5,3,43),
	(6,3,51),
	(7,4,43),
	(8,4,51),
	(9,5,43),
	(10,5,51),
	(11,6,3),
	(12,7,3),
	(13,8,46),
	(14,9,32),
	(15,10,32),
	(16,11,32),
	(17,12,49),
	(18,13,49),
	(19,14,49),
	(20,15,34),
	(21,16,34),
	(22,17,34),
	(23,18,48),
	(24,19,48),
	(25,20,48),
	(26,21,48),
	(27,22,48),
	(28,23,48);
	
UPDATE events_commitment c
JOIN actions_action a ON c.action_id = a.id
SET c.question = REPLACE(a.slug, '-', '_');
	
CREATE TABLE dup_guests AS
	SELECT MAX(g.id) AS id
	FROM events_guest g
	WHERE g.email <> ''
	GROUP BY g.event_id, g.email
	HAVING count(*) > 1;
UPDATE events_guest
SET email = ''
WHERE id IN (SELECT id FROM dup_guests);
DROP TABLE dup_guests;

INSERT INTO commitments_contributor (id, first_name, last_name, email, phone, location_id, user_id, created, updated)
SELECT id, MAX(first_name), MAX(last_name), MAX(email), MAX(phone), MAX(location_id), user_id, created, updated
FROM events_guest
WHERE user_id IS NOT NULL
GROUP BY user_id
UNION
SELECT id, MAX(first_name), MAX(last_name), email, MAX(phone), MAX(location_id), NULL, created, updated
FROM events_guest
WHERE user_id IS NULL AND email <> ''
GROUP BY email
UNION
SELECT id, first_name, last_name, NULL, phone, location_id, NULL, created, updated
FROM events_guest
WHERE user_id IS NULL AND email = '';

CREATE TABLE `events_guest_new` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `contributor_id` int(11) NOT NULL,
  `invited` date DEFAULT NULL,
  `added` date DEFAULT NULL,
  `rsvp_status` varchar(1) NOT NULL,
  `comments` longtext NOT NULL,
  `notify_on_rsvp` tinyint(1) NOT NULL,
  `is_host` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `event_id` (`event_id`,`contributor_id`),
  KEY `contributor_id_refs_id_4f07cc38` (`contributor_id`),
  CONSTRAINT `contributor_id_refs_id_4f07cc38` FOREIGN KEY (`contributor_id`) REFERENCES `commitments_contributor` (`id`),
  CONSTRAINT `event_id_refs_id_d9a57ddf` FOREIGN KEY (`event_id`) REFERENCES `events_event` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO events_guest_new (id, event_id, contributor_id, invited, added, rsvp_status, comments, notify_on_rsvp, is_host, created, updated)
SELECT eg.id, eg.event_id, CASE WHEN cc.id IS NOT NULL THEN cc.id ELSE eg.id END, 
    eg.invited, eg.added, eg.rsvp_status, eg.comments, eg.notify_on_rsvp, eg.is_host, eg.created, eg.updated
FROM events_guest eg
LEFT JOIN commitments_contributor cc ON eg.user_id = cc.user_id OR eg.email = cc.email;

RENAME TABLE events_guest TO events_guest_old, events_guest_new TO events_guest;

-- NOTE: 6 records fall out; 2660 -> 2654
INSERT INTO commitments_commitment (id, contributor_id, question, answer, action_id, created, updated)
SELECT MAX(ec.id), eg.contributor_id, ec.question, MAX(ec.answer), ec.action_id, MAX(ec.created), MAX(ec.updated)
FROM events_commitment ec
JOIN events_guest eg ON ec.guest_id = eg.id
GROUP BY eg.contributor_id, ec.question, ec.action_id;

UPDATE messaging_queue q
JOIN django_content_type ct ON q.content_type_id = ct.id
JOIN django_content_type nct ON nct.app_label = "commitments" AND nct.model = "commitment"
SET q.content_type_id = nct.id
WHERE ct.app_label = "events" AND ct.model = "commitment";

UPDATE messaging_queue q
JOIN django_content_type ct ON q.batch_content_type_id = ct.id
JOIN django_content_type nct ON nct.app_label = "commitments" AND nct.model = "contributor"
JOIN events_guest g ON q.batch_object_pk = g.id
SET q.batch_content_type_id = nct.id, q.batch_object_pk = g.contributor_id
WHERE ct.app_label = "events" AND ct.model = "guest";

ALTER TABLE events_eventtype ADD survey_id int(11) AFTER description;
ALTER TABLE events_eventtype ADD CONSTRAINT `survey_id_refs_id_3de7612c` FOREIGN KEY (`survey_id`) REFERENCES `commitments_survey` (`id`);
UPDATE events_eventtype et
JOIN events_survey s ON et.id = s.event_type_id AND s.is_active = 1
SET et.survey_id = s.id;

ALTER TABLE events_event ADD default_survey_id int(11) AFTER event_type_id;
ALTER TABLE events_event ADD CONSTRAINT `default_survey_id_refs_id_9d07220a` FOREIGN KEY (`default_survey_id`) REFERENCES `commitments_survey` (`id`);
UPDATE events_event e
JOIN events_survey s ON e.event_type_id = s.event_type_id AND s.is_active = 1
SET e.default_survey_id = s.id;

INSERT INTO commitments_contributorsurvey (contributor_id, survey_id, entered_by_id, created, updated)
SELECT DISTINCT g.contributor_id, e.default_survey_id, e.creator_id, MIN(c.created), MAX(c.created)
FROM events_guest g
JOIN events_event e ON g.event_id = e.id
JOIN commitments_commitment c ON g.contributor_id = c.contributor_id
GROUP BY g.contributor_id, e.default_survey_id, e.creator_id;

DROP TABLE events_commitment, events_guest_old, events_survey;

ALTER TABLE source_tracking_usersource ADD created datetime;
ALTER TABLE source_tracking_usersource ADD updated datetime;
UPDATE source_tracking_usersource t
JOIN auth_user u ON t.user_id = u.id
SET created = u.date_joined, updated = u.date_joined;
ALTER TABLE source_tracking_usersource MODIFY created datetime NOT NULL;
ALTER TABLE source_tracking_usersource MODIFY updated datetime NOT NULL;

UPDATE messaging_message
SET body = '{% extends \'rah/base_email.html\' %}\r\n{% block email_content %}\r\nThe following user has just registered for a RAH account:\r\n    <a href=\"http://{{ domain }}{{ content_object.get_absolute_url }}\">{{ content_object.get_full_name }}</a>\r\n    Location: {{ content_object.get_profile.location }}\r\n    {% with content_object.usersource_set.all.0 as usersource %}\r\n    Source: {{ usersource.source }}\r\n    Subsource: {{ usersource.subsource }}\r\n    Referrer: {{ usersource.referrer }}\r\n    {% endwith %}\r\n{% endblock %}'
WHERE name = 'New Account';

INSERT INTO actions_actionform (action_id, form_name, var_name, created, updated)
SELECT a.id, "VampirePowerWorksheetForm2", "vampire_worksheet_form", NOW(), NOW()
FROM actions_action a
WHERE a.name = "Eliminate vampire power"