CREATE TABLE `events_event_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `event_id` (`event_id`,`group_id`),
  KEY `events_event_groups_e9b82f95` (`event_id`),
  KEY `events_event_groups_bda51c3c` (`group_id`),
  CONSTRAINT `event_id_refs_id_8356bd37` FOREIGN KEY (`event_id`) REFERENCES `events_event` (`id`),
  CONSTRAINT `group_id_refs_id_3bed3343` FOREIGN KEY (`group_id`) REFERENCES `groups_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
