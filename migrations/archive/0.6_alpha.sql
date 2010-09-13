INSERT INTO `events_eventtype` (`id`, `name`, `teaser`, `created`, `updated`, `description`) 
VALUES (5, "Apartment Energy Meeting", "", NOW(), NOW(), "Our energy choices at home have a huge impact on our health, our environment, and our pocketbooks.   At the energy meeting, we will explore ways to improve our community by using less energy at home.  We’ll learn about simple actions that tackle the main sources of home energy waste, and we’ll also brainstorm ways we can grow our impact by getting others involved in repowering their homes.");

INSERT INTO `events_survey` (`id`, `name`, `event_type_id`, `form_name`, `template_name`, `is_active`, `created`, `updated`)
VALUES (4, "Apartment Energy Meeting Commitment Card", 5, "ApartmentEnergyMeetingCommitmentCard", "events/_energy_commitment_card.html", 1, NOW(), NOW());

UPDATE groups_group SET image = "images/theme/default_group.png"
WHERE is_geo_group = 0 AND image = "";