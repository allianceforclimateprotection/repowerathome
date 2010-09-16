ALTER TABLE messaging_message ADD generic_relation_content_type_id int(11) AFTER minimum_duration;
UPDATE messaging_message SET generic_relation_content_type_id=48 WHERE name='Event invite';
UPDATE messaging_message SET generic_relation_content_type_id=30 WHERE name='Team invite';

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
	(22,17,34);