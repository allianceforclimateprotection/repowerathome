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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;