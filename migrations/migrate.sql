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

-- Add a new column, headquarters, for the groups table
ALTER TABLE groups_group ADD headquarters_id int(11) NOT NULL AFTER is_featured;
-- Create temporary table to extract new headquarters from
CREATE TEMPORARY TABLE starting_headquarters AS
SELECT g.id, g.name,
CASE 
    WHEN s.id THEN s.id
    WHEN l.id THEN l.id
    ELSE 1
END AS location_id
FROM groups_group g
LEFT JOIN groups_groupusers m ON g.id = m.group_id AND m.is_manager = 1
LEFT JOIN auth_user u ON m.user_id = u.id
LEFT JOIN rah_profile p ON u.id = p.user_id
LEFT JOIN geo_location l ON p.location_id = l.id
LEFT JOIN geo_location s ON g.sample_location_id = s.id
GROUP BY g.id;
-- Set new headquaters field
UPDATE groups_group g
JOIN starting_headquarters h ON g.id = h.id
SET g.headquarters_id = h.location_id;
-- Delete the temporary table
DROP TEMPORARY TABLE starting_headquarters;
-- Add headquasters foreign key relationships
ALTER TABLE groups_group ADD KEY `groups_group_948a4cc7` (`headquarters_id`);
ALTER TABLE groups_group ADD CONSTRAINT `headquarters_id_refs_id_a1850736` FOREIGN KEY (`headquarters_id`) REFERENCES `geo_location` (`id`);
