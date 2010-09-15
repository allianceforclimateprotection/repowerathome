LOCK TABLES `events_survey` WRITE;
UPDATE `events_survey` SET `is_active` = 0 WHERE `id` IN (1,4);
INSERT INTO `events_survey` (`id`,`name`,`event_type_id`,`form_name`,`template_name`,`is_active`,`created`,`updated`)
VALUES
	(5,'Energy Meeting Commitment Card Version 2',1,'EnergyMeetingCommitmentCardVersion2','events/_energy_commitment_card.html',1,'2010-09-07 15:57:00','2010-09-07 15:57:00'),
	(6,'Apartment Energy Meeting Commitment Card Version 2',5,'ApartmentEnergyMeetingCommitmentCardVersion2','events/_energy_commitment_card.html',1,'2010-09-07 15:57:00','2010-09-07 15:57:00');
UNLOCK TABLES;