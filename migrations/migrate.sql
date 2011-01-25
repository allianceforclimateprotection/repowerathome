INSERT INTO commitments_contributor (first_name, last_name, email, location_id, user_id, created, updated)
SELECT u.first_name, u.last_name, u.email, p.location_id, u.id, NOW(), NOW()
FROM auth_user u
LEFT JOIN rah_profile p ON u.id = p.user_id
LEFT JOIN commitments_contributor c ON u.id = c.user_id
WHERE c.id IS NULL;

INSERT INTO `messaging_message` (`id`,`name`,`subject`,`body`,`sends`,`message_timing`,`x_value`,`recipient_function`,`send_as_batch`,`batch_window`,`time_snap`,`minimum_duration`,`generic_relation_content_type_id`,`created`,`updated`)
VALUES
    (24,'You\'ve created a team','Organizing your Repower at Home team','{% extends \'rah/base_email.html\' %}\r\n{% block email_content %}\r\n<p>\r\nHi {{ recipient.first_name }},\r\n</p>\r\n\r\n<p>\r\n I’m Shira, the Field Director for Repower at Home. My job is to bring the enthusiasm for saving energy that you find on repowerathome.com into the real world by working with leaders like you.\r\n</p>\r\n\r\n<p>\r\nI see you recently created a team on repowerathome.com, <a href=”http://{{ domain }}{{ content_object.get_absolute_url }}”>{{ content_object}}</a>. Nice! Teams are a great way for  a community  to share ideas, compete with friends and work together to save energy. \r\n</p>\r\n\r\n<p>\r\nAs the team administrator, you can invite people to your team, moderate discussions and more by using the tools on your team’s page. <strong>Get started by inviting some friends to join your team</strong>. <a href=”http://{{ domain }}{{ content_object.get_absolute_url }}”>Try it out now</a>.\r\n</p> \r\n\r\n<p>\r\nRepower at Home teams often work to organize events in their communities, like <a href=”http://{{ domain }}/events/”>energy meetings</a> and challenges to recruit  <a href=”http://{{ domain }}/about-pledge/”>Trendsetters</a>. The Repower at Home field team can tell you more about these opportunities. To get in touch, drop us a line at <mailto:”field@repowerathome.com”>field@repowerathome.com</a>.  We’d love to hear your ideas for getting others energized about saving energy.\r\n</p>\r\n\r\n<p>\r\nHappy energy savings,<br />\r\nShira Miller<br />\r\nField Director, Repower at Home \r\n</p>\r\n{% endblock %}',0,'send_immediately',0,'lambda x: x.managers()',0,NULL,NULL,NULL,NULL,'2011-01-13 09:44:23','2011-01-13 09:46:53');

INSERT INTO `messaging_message_content_types` (`id`,`message_id`,`contenttype_id`)
VALUES
    (88,24,30);

INSERT INTO `messaging_abtest` (`id`,`message_id`,`test_message_id`,`test_percentage`,`is_enabled`,`stream_id`,`created`,`updated`)
VALUES
    (23,24,NULL,0,1,15,'2011-01-13 09:55:11','2011-01-13 09:55:11');


-- Changes to Events --
ALTER TABLE `events_event` DROP FOREIGN KEY `event_type_id_refs_id_3d343b5b`;
ALTER TABLE `events_event` DROP COLUMN `event_type_id`;
DROP TABLE `events_eventtype`;
ALTER TABLE `events_event` CHANGE `place_name` `title` VARCHAR (100);
ALTER TABLE `events_event` ADD lat DOUBLE PRECISION NULL;
ALTER TABLE `events_event` ADD lon DOUBLE PRECISION NULL;
UPDATE events_event SET `where`='Zinc Pyatt Rd, Blythe, AR, USA', `lat`='36.271337', `lon`='-92.8713761' WHERE `id`='1';
UPDATE events_event SET `where`='Sarasota, FL 34235, USA', `lat`='27.3664703', `lon`='-82.4757766' WHERE `id`='2';
UPDATE events_event SET `where`='9712 28th Ave SW, Seattle, WA 98126, USA', `lat`='47.5163126', `lon`='-122.3685685' WHERE `id`='3';
UPDATE events_event SET `where`='7400 Arlington Rd, Bethesda, MD 20814, USA', `lat`='38.9837604', `lon`='-77.098589' WHERE `id`='4';
UPDATE events_event SET `where`='6600 Cradlerock Way, Columbia, MD 21045, USA', `lat`='39.1901207', `lon`='-76.8467884' WHERE `id`='5';
UPDATE events_event SET `where`='Toledo, OH 43659, USA', `lat`='41.65', `lon`='-83.54' WHERE `id`='6';
UPDATE events_event SET `where`='5885 Robert Oliver Pl, Columbia, MD 21045, USA', `lat`='39.2101946', `lon`='-76.8470737' WHERE `id`='7';
UPDATE events_event SET `where`='6 Westwick Ct, Annapolis, MD 21403, USA', `lat`='38.944522', `lon`='-76.506615' WHERE `id`='8';
UPDATE events_event SET `where`='901 E St NE, Washington, DC 20002, USA', `lat`='38.896101', `lon`='-76.9931589' WHERE `id`='9';
UPDATE events_event SET `where`='1540 Pointer Ridge Pl, Bowie, MD 20716, USA', `lat`='38.9097524', `lon`='-76.7190033' WHERE `id`='10';
UPDATE events_event SET `where`='9321 Ocala St, Silver Spring, MD 20901, USA', `lat`='39.008894', `lon`='-77.01136' WHERE `id`='11';
UPDATE events_event SET `where`='Cockeysville, MD, USA', `lat`='39.4812172', `lon`='-76.6438598' WHERE `id`='12';
UPDATE events_event SET `where`='Annapolis, MD, USA', `lat`='38.9784453', `lon`='-76.4921829' WHERE `id`='13';
UPDATE events_event SET `where`='Crownsville, MD, USA', `lat`='39.0284438', `lon`='-76.6013536' WHERE `id`='14';
UPDATE events_event SET `where`='Des Moines, IA 50314, USA', `lat`='41.601551', `lon`='-93.6283531' WHERE `id`='15';
UPDATE events_event SET `where`='Des Moines, IA 50314, USA', `lat`='41.601551', `lon`='-93.6283531' WHERE `id`='16';
UPDATE events_event SET `where`='Rockville, MD 20853, USA', `lat`='39.1078147', `lon`='-77.0993194' WHERE `id`='17';
UPDATE events_event SET `where`='Cedar Rapids, IA 52407, USA', `lat`='41.9799999', `lon`='-91.66' WHERE `id`='18';
UPDATE events_event SET `where`='Creston, IA 50801, USA', `lat`='41.0591667', `lon`='-94.3644444' WHERE `id`='19';
UPDATE events_event SET `where`='Bellevue, IA, USA', `lat`='42.2591667', `lon`='-90.4263889' WHERE `id`='20';
UPDATE events_event SET `where`='Charles City, IA 50616, USA', `lat`='43.0663612', `lon`='-92.6724112' WHERE `id`='21';
UPDATE events_event SET `where`='Indianola, IA 50125, USA', `lat`='41.3580484', `lon`='-93.5574376' WHERE `id`='22';
UPDATE events_event SET `where`='Baltimore, MD 21218, USA', `lat`='39.3281059', `lon`='-76.6043205' WHERE `id`='23';
UPDATE events_event SET `where`='Iowa City, IA 52245, USA', `lat`='41.6515693', `lon`='-91.4965515' WHERE `id`='24';
UPDATE events_event SET `where`='Des Moines, IA 50311, USA', `lat`='41.6004409', `lon`='-93.6643333' WHERE `id`='25';
UPDATE events_event SET `where`='Clive, IA 50325, USA', `lat`='41.6171073', `lon`='-93.8447875' WHERE `id`='26';
UPDATE events_event SET `where`='Reisterstown, MD, USA', `lat`='39.4695489', `lon`='-76.8294213' WHERE `id`='27';
UPDATE events_event SET `where`='Silver Spring, MD 20910, USA', `lat`='39.0040855', `lon`='-77.0383911' WHERE `id`='28';
UPDATE events_event SET `where`='Bethesda, MD, USA', `lat`='38.9806658', `lon`='-77.100256' WHERE `id`='29';
UPDATE events_event SET `where`='Rockville, MD, USA', `lat`='39.0839973', `lon`='-77.1527578' WHERE `id`='30';
UPDATE events_event SET `where`='Silver Spring, MD 20901, USA', `lat`='39.0176639', `lon`='-77.0083923' WHERE `id`='31';
UPDATE events_event SET `where`='Des Moines, IA 50311, USA', `lat`='41.6004409', `lon`='-93.6643333' WHERE `id`='32';
UPDATE events_event SET `where`='Catonsville, MD 21228, USA', `lat`='39.2693023', `lon`='-76.7320671' WHERE `id`='33';
UPDATE events_event SET `where`='Dysart, IA 52224, USA', `lat`='42.171659', `lon`='-92.3062978' WHERE `id`='34';
UPDATE events_event SET `where`='Des Moines, IA 50311, USA', `lat`='41.6004409', `lon`='-93.6643333' WHERE `id`='35';
UPDATE events_event SET `where`='Rockville, MD, USA', `lat`='39.0839973', `lon`='-77.1527578' WHERE `id`='36';
UPDATE events_event SET `where`='Riverdale Park, MD, USA', `lat`='38.963444', `lon`='-76.9316408' WHERE `id`='37';
UPDATE events_event SET `where`='Bethesda, MD 20814, USA', `lat`='39.0284233', `lon`='-77.0961494' WHERE `id`='38';
UPDATE events_event SET `where`='Chevy Chase, MD, USA', `lat`='38.9805556', `lon`='-77.0838889' WHERE `id`='39';
UPDATE events_event SET `where`='Silver Spring, MD 20901, USA', `lat`='39.0176639', `lon`='-77.0083923' WHERE `id`='40';
UPDATE events_event SET `where`='Rockville, MD 20852, USA', `lat`='39.0525588', `lon`='-77.1222572' WHERE `id`='41';
UPDATE events_event SET `where`='Takoma Park, MD, USA', `lat`='38.9778882', `lon`='-77.0074765' WHERE `id`='42';
UPDATE events_event SET `where`='Columbia, MD 21045, USA', `lat`='39.2098903', `lon`='-76.8265151' WHERE `id`='43';
UPDATE events_event SET `where`='Bethesda, MD 20816, USA', `lat`='38.9548034', `lon`='-77.1149139' WHERE `id`='44';
UPDATE events_event SET `where`='Iowa City, IA 52246, USA', `lat`='41.6505851', `lon`='-91.6071548' WHERE `id`='45';
UPDATE events_event SET `where`='Bethesda, MD 20814, USA', `lat`='39.0284233', `lon`='-77.0961494' WHERE `id`='46';
UPDATE events_event SET `where`='Baltimore, MD 21211, USA', `lat`='39.3320007', `lon`='-76.6381835' WHERE `id`='47';
UPDATE events_event SET `where`='Slater, IA, USA', `lat`='41.879021', `lon`='-93.686974' WHERE `id`='48';
UPDATE events_event SET `where`='Des Moines, IA 50310, USA', `lat`='41.6413478', `lon`='-93.6846237' WHERE `id`='49';
UPDATE events_event SET `where`='Ankeny, IA 50021, USA', `lat`='41.6977958', `lon`='-93.616764' WHERE `id`='50';
UPDATE events_event SET `where`='Waverly, IA 50677, USA', `lat`='42.7272032', `lon`='-92.4668511' WHERE `id`='51';
UPDATE events_event SET `where`='Dubuque, IA 52001, USA', `lat`='42.5556869', `lon`='-90.6984405' WHERE `id`='52';
UPDATE events_event SET `where`='Arnold, MD 21012, USA', `lat`='39.0413894', `lon`='-76.5037155' WHERE `id`='53';
UPDATE events_event SET `where`='Des Moines, IA 50314, USA', `lat`='41.601551', `lon`='-93.6283531' WHERE `id`='54';
UPDATE events_event SET `where`='Burtonsville, MD, USA', `lat`='39.1112193', `lon`='-76.9324752' WHERE `id`='55';
UPDATE events_event SET `where`='Annapolis, MD, USA', `lat`='38.9784453', `lon`='-76.4921829' WHERE `id`='56';
UPDATE events_event SET `where`='Halethorpe, MD 21227, USA', `lat`='39.2411041', `lon`='-76.6743278' WHERE `id`='57';
UPDATE events_event SET `where`='Gaithersburg, MD, USA', `lat`='39.1434406', `lon`='-77.2013705' WHERE `id`='58';
UPDATE events_event SET `where`='Silver Spring, MD 20901, USA', `lat`='39.0176639', `lon`='-77.0083923' WHERE `id`='59';
UPDATE events_event SET `where`='Catonsville, MD 21228, USA', `lat`='39.2693023', `lon`='-76.7320671' WHERE `id`='60';
UPDATE events_event SET `where`='Rockville, MD, USA', `lat`='39.0839973', `lon`='-77.1527578' WHERE `id`='61';
UPDATE events_event SET `where`='Takoma Park, MD, USA', `lat`='38.9778882', `lon`='-77.0074765' WHERE `id`='62';
UPDATE events_event SET `where`='Columbia, MD 21045, USA', `lat`='39.2098903', `lon`='-76.8265151' WHERE `id`='63';
UPDATE events_event SET `where`='Maryland 21207, USA', `lat`='39.3250465', `lon`='-76.7144317' WHERE `id`='64';
UPDATE events_event SET `where`='Baltimore, MD 21210, USA', `lat`='39.3593959', `lon`='-76.6505976' WHERE `id`='65';
UPDATE events_event SET `where`='Parkville, MD, USA', `lat`='39.3773292', `lon`='-76.5396875' WHERE `id`='66';
UPDATE events_event SET `where`='Annapolis, MD, USA', `lat`='38.9784453', `lon`='-76.4921829' WHERE `id`='67';
UPDATE events_event SET `where`='Annapolis, MD, USA', `lat`='38.9784453', `lon`='-76.4921829' WHERE `id`='68';
UPDATE events_event SET `where`='La Porte City, IA 50651, USA', `lat`='42.3149911', `lon`='-92.1921275' WHERE `id`='69';
UPDATE events_event SET `where`='Chevy Chase, MD, USA', `lat`='38.9805556', `lon`='-77.0838889' WHERE `id`='70';
UPDATE events_event SET `where`='Urbandale, IA 50322, USA', `lat`='41.632656', `lon`='-93.7382698' WHERE `id`='71';
UPDATE events_event SET `where`='Washington, DC 20015, USA', `lat`='38.9675674', `lon`='-77.0655899' WHERE `id`='72';
UPDATE events_event SET `where`='Ankeny Regional Airport (IKV), 3700 SE Convenience Blvd, Ankeny, IA 50021, USA', `lat`='41.6904355', `lon`='-93.5676539' WHERE `id`='73';
UPDATE events_event SET `where`='Des Moines, IA 50314, USA', `lat`='41.601551', `lon`='-93.6283531' WHERE `id`='74';
UPDATE events_event SET `where`='Washington, DC 20004, USA', `lat`='38.8943996', `lon`='-77.0267715' WHERE `id`='75';
UPDATE events_event SET `where`='Columbia, MD 21045, USA', `lat`='39.2098903', `lon`='-76.8265151' WHERE `id`='76';
UPDATE events_event SET `where`='Des Moines, IA 50314, USA', `lat`='41.601551', `lon`='-93.6283531' WHERE `id`='77';
UPDATE events_event SET `where`='Des Moines, IA 50314, USA', `lat`='41.601551', `lon`='-93.6283531' WHERE `id`='78';
UPDATE events_event SET `where`='Des Moines, IA 50314, USA', `lat`='41.601551', `lon`='-93.6283531' WHERE `id`='79';
UPDATE events_event SET `where`='Burtonsville, MD, USA', `lat`='39.1112193', `lon`='-76.9324752' WHERE `id`='80';
UPDATE events_event SET `where`='Baltimore, MD 21212, USA', `lat`='39.3813896', `lon`='-76.6216697' WHERE `id`='81';
UPDATE events_event SET `where`='Rockville, MD 20853, USA', `lat`='39.1078147', `lon`='-77.0993194' WHERE `id`='82';
UPDATE events_event SET `where`='Kensington, MD 20895, USA', `lat`='39.0256651', `lon`='-77.0763669' WHERE `id`='83';
UPDATE events_event SET `where`='Des Moines, IA 50314, USA', `lat`='41.601551', `lon`='-93.6283531' WHERE `id`='84';
UPDATE events_event SET `where`='Des Moines, IA 50311, USA', `lat`='41.6004409', `lon`='-93.6643333' WHERE `id`='85';
UPDATE events_event SET `where`='Baltimore, MD 21209, USA', `lat`='39.3668174', `lon`='-76.670948' WHERE `id`='86';
UPDATE events_event SET `where`='Silver Spring, MD 20904, USA', `lat`='39.0646591', `lon`='-76.9827995' WHERE `id`='87';
UPDATE events_event SET `where`='Des Moines, IA 50314, USA', `lat`='41.601551', `lon`='-93.6283531' WHERE `id`='88';
UPDATE events_event SET `where`='317 W 23rd St, Tucson, AZ 85713, USA', `lat`='32.20525', `lon`='-110.97388' WHERE `id`='89';
UPDATE events_event SET `where`='11803 Rosalinda Dr, Potomac, MD 20854, USA', `lat`='39.049563', `lon`='-77.173385' WHERE `id`='90';
UPDATE events_event SET `where`='1735 Galleria Blvd, Franklin, TN 37067, USA', `lat`='35.96321', `lon`='-86.81242' WHERE `id`='91';
UPDATE events_event SET `where`='317 W 23rd St, Tucson, AZ 85713, USA', `lat`='32.20525', `lon`='-110.97388' WHERE `id`='92';
UPDATE events_event SET `where`='4545 Connecticut Ave NW #515, Washington, DC 20008, USA', `lat`='38.949069', `lon`='-77.066222' WHERE `id`='93';
UPDATE events_event SET `where`='2431 St Paul St, Baltimore, MD 21218, USA', `lat`='39.3171374', `lon`='-76.6153156' WHERE `id`='94';
UPDATE events_event SET `where`='4825 Cordell Ave #200, Bethesda, MD 20814, USA', `lat`='38.9908959', `lon`='-77.0967795' WHERE `id`='95';
UPDATE events_event SET `where`='10701 Old Georgetown Rd, Rockville, MD 20852, USA', `lat`='39.03176', `lon`='-77.125073' WHERE `id`='96';
UPDATE events_event SET `where`='Geneva Day School, 11931 7 Locks Rd, Potomac, MD 20854-3341, USA', `lat`='39.05429', `lon`='-77.16259' WHERE `id`='98';
UPDATE events_event SET `where`='14175 Castle Blvd, Silver Spring, MD 20904, USA', `lat`='39.0883057', `lon`='-76.939823' WHERE `id`='99';
UPDATE events_event SET `where`='18831 Castle Blvd, Silver Spring, MD 20904, USA', `lat`='39.0899472', `lon`='-76.9394907' WHERE `id`='100';
UPDATE events_event SET `where`='Tragara Ristorante, 4935 Cordell Ave, Bethesda, MD 20814-2509, USA', `lat`='38.9884526', `lon`='-77.0991597' WHERE `id`='101';
UPDATE events_event SET `where`='Bradley Hills Presbyterian Church Nursery School, 6601 Bradley Blvd, Bethesda, MD 20817, USA', `lat`='39.0026098', `lon`='-77.1316454' WHERE `id`='102';
UPDATE events_event SET `where`='227 E 4th St, Frederick, MD 21701, USA', `lat`='39.4188596', `lon`='-77.4067006' WHERE `id`='103';
UPDATE events_event SET `where`='8000 York Rd, Towson, MD 21286, USA', `lat`='39.393447', `lon`='-76.604349' WHERE `id`='104';
UPDATE events_event SET `where`='12801 Columbia Pike, Silver Spring, MD 20904, USA', `lat`='39.0623166', `lon`='-76.9629396' WHERE `id`='106';
UPDATE events_event SET `where`='11931 7 Locks Rd, Potomac, MD 20854, USA', `lat`='39.054012', `lon`='-77.162175' WHERE `id`='107';
UPDATE events_event SET `where`='40 Rhode Island Ave NE, Washington, DC 20002, USA', `lat`='38.9166713', `lon`='-77.0091902' WHERE `id`='108';
UPDATE events_event SET `where`='1735 Galleria Blvd, Franklin, TN 37067, USA', `lat`='35.96321', `lon`='-86.81242' WHERE `id`='110';
UPDATE events_event SET `where`='1735 Galleria Blvd, Franklin, TN 37067, USA', `lat`='35.96321', `lon`='-86.81242' WHERE `id`='111';
UPDATE events_event SET `where`='611 Central Ave, Towson, MD 21204, USA', `lat`='39.4033299', `lon`='-76.609151' WHERE `id`='112';
UPDATE events_event SET `where`='333 Dubois Rd, Annapolis, MD 21401, USA', `lat`='38.9990219', `lon`='-76.523816' WHERE `id`='113';
UPDATE events_event SET `where`='Catonsville Plumbing, 300 N Charles St, Baltimore, MD 21201-4305, USA', `lat`='39.292318', `lon`='-76.615587' WHERE `id`='114';
UPDATE events_event SET `where`='4825 Cordell Ave #200, Bethesda, MD 20814, USA', `lat`='38.9908959', `lon`='-77.0967795' WHERE `id`='115';
UPDATE events_event SET `where`='University of Maryland, 1401 Marie Mt Hall, College Park, MD 20742-7505, USA', `lat`='38.9849416', `lon`='-76.9408099' WHERE `id`='116';
UPDATE events_event SET `where`='5051 Pierce Ave, College Park, MD 20740, USA', `lat`='38.9874534', `lon`='-76.9271732' WHERE `id`='117';
UPDATE events_event SET `where`='Mt Vernon Ave, Baltimore, MD 21215, USA', `lat`='39.3507965', `lon`='-76.7136251' WHERE `id`='118';
UPDATE events_event SET `where`='Freedom Plaza, Washington, DC 20004, USA', `lat`='38.8958333', `lon`='-77.0307222' WHERE `id`='119';
UPDATE events_event SET `where`='1017 W 38th St, Baltimore, MD 21211, USA', `lat`='39.3340109', `lon`='-76.634112' WHERE `id`='120';
UPDATE events_event SET `where`='509 South St, Bow, NH 03304, USA', `lat`='43.1715003', `lon`='-71.5346065' WHERE `id`='121';
UPDATE events_event SET `where`='University of Maryland, 1401 Marie Mt Hall, College Park, MD 20742-7505, USA', `lat`='38.9849416', `lon`='-76.9408099' WHERE `id`='122';
UPDATE events_event SET `where`='585 Russell Ave, Wyckoff, NJ 07481, USA', `lat`='40.992548', `lon`='-74.183569' WHERE `id`='123';
UPDATE events_event SET `where`='8210 Postoak Rd, Potomac, MD 20854, USA', `lat`='39.052645', `lon`='-77.169513' WHERE `id`='124';
UPDATE events_event SET `where`='333 Dubois Rd, Annapolis, MD 21401, USA', `lat`='38.9990219', `lon`='-76.523816' WHERE `id`='125';
UPDATE events_event SET `where`='Towson, MD 21204, USA', `lat`='39.4003791', `lon`='-76.6345252' WHERE `id`='126';
UPDATE events_event SET `where`='905 Frederick Rd, Catonsville, MD 21228, USA', `lat`='39.2708129', `lon`='-76.7356' WHERE `id`='127';
UPDATE events_event SET `where`='Bethesda, MD 20814, USA', `lat`='39.0284233', `lon`='-77.0961494' WHERE `id`='128';
UPDATE events_event SET `where`='Milford, NH, USA', `lat`='42.8353641', `lon`='-71.6489604' WHERE `id`='129';
UPDATE events_event SET `where`='Druid Hill Park, Madison Ave, Baltimore, MD 21217, USA', `lat`='39.3237103', `lon`='-76.6438965' WHERE `id`='130';
UPDATE events_event SET `where`='Russett Common, Laurel, MD 20724, USA', `lat`='39.1024161', `lon`='-76.8038511' WHERE `id`='131';
UPDATE events_event SET `where`='Washington, DC 20010, USA', `lat`='38.9323043', `lon`='-77.0278511' WHERE `id`='132';
UPDATE events_event SET `where`='800 St Paul St, Baltimore, MD 21202, USA', `lat`='39.298752', `lon`='-76.614237' WHERE `id`='133';
UPDATE events_event SET `where`='3460 14th St NW, Washington, DC 20010, USA', `lat`='38.9323996', `lon`='-77.0327566' WHERE `id`='134';
UPDATE events_event SET `where`='509 South St, Bow, NH 03304, USA', `lat`='43.1715003', `lon`='-71.5346065' WHERE `id`='136';
UPDATE events_event SET `where`='901 E St NW, Washington, DC 20004, USA', `lat`='38.896398', `lon`='-77.024192' WHERE `id`='138';
UPDATE events_event SET `where`='Woodstock, NH 03293, USA', `lat`='44.0062942', `lon`='-71.6864345' WHERE `id`='139';
UPDATE events_event SET `where`='194 Pollard Rd, Lincoln, NH 03251, USA', `lat`='44.0489499', `lon`='-71.6641016' WHERE `id`='140';
UPDATE events_event SET `where`='509 South St, Bow, NH 03304, USA', `lat`='43.1715003', `lon`='-71.5346065' WHERE `id`='141';
UPDATE events_event SET `where`='509 South St, Bow, NH 03304, USA', `lat`='43.1715003', `lon`='-71.5346065' WHERE `id`='142';
UPDATE events_event SET `where`='2095 Walnut Ave, Owings Mills, MD 21117, USA', `lat`='39.4617313', `lon`='-76.746456' WHERE `id`='143';
UPDATE events_event SET `where`='325 Pleasant St, Concord, NH 03301, USA', `lat`='43.197152', `lon`='-71.573632' WHERE `id`='144';
UPDATE events_event SET `where`='Baltimore, MD 21239, USA', `lat`='39.3685989', `lon`='-76.5885925' WHERE `id`='145';
UPDATE events_event SET `where`='2601 Powder Mill Rd, Hyattsville, MD 20783, USA', `lat`='39.0263628', `lon`='-76.9653081' WHERE `id`='146';
UPDATE events_event SET `where`='135 E Main St, Woodstock, GA 30188, USA', `lat`='34.099471', `lon`='-84.5196322' WHERE `id`='147';
UPDATE events_event SET `where`='1735 Galleria Blvd, Franklin, TN 37067, USA', `lat`='35.96321', `lon`='-86.81242' WHERE `id`='148';
UPDATE events_event SET `where`='1700 Forum Blvd, Columbia, MO 65203, USA', `lat`='38.933175', `lon`='-92.360687' WHERE `id`='149';
UPDATE events_event SET `where`='201 Ethan Allen Ave, Takoma Park, MD 20912, USA', `lat`='38.9778846', `lon`='-77.0058769' WHERE `id`='150';
UPDATE events_event SET `where`='Littleton, NH, USA', `lat`='44.3061725', `lon`='-71.7700885' WHERE `id`='151';
UPDATE events_event SET `where`='N Main St, Hanover, NH 03755, USA', `lat`='43.697328', `lon`='-72.289923' WHERE `id`='152';
UPDATE events_event SET `where`='1 Crusader Way, Manchester, NH 03103, USA', `lat`='42.9647093', `lon`='-71.434432' WHERE `id`='153';
UPDATE events_event SET `where`='7700 Old Georgetown Rd, Bethesda, MD 20814, USA', `lat`='38.986367', `lon`='-77.097759' WHERE `id`='154';
UPDATE events_event SET `where`='621 W Lombard St, Baltimore, MD 21201, USA', `lat`='39.2873409', `lon`='-76.6244223' WHERE `id`='155';
UPDATE events_event SET `where`='8601 Harford Rd, Parkville, MD 21234, USA', `lat`='39.38158', `lon`='-76.534677' WHERE `id`='156';
UPDATE events_event SET `where`='1166 U.S. 4, Canaan, NH 03741, USA', `lat`='43.6464285', `lon`='-72.0122511' WHERE `id`='157';
UPDATE events_event SET `where`='Manchester St, Concord, NH 03301, USA', `lat`='43.190038', `lon`='-71.508944' WHERE `id`='158';
UPDATE events_event SET `where`='210 Main St, Eliot, ME 03903, USA', `lat`='43.116516', `lon`='-70.792934' WHERE `id`='159';
UPDATE events_event SET `where`='6604 McCahill Terrace, Laurel, MD 20707, USA', `lat`='39.114322', `lon`='-76.892401' WHERE `id`='160';
UPDATE events_event SET `where`='12500 Fort Washington Rd, Fort Washington, MD 20744, USA', `lat`='38.718667', `lon`='-77.003976' WHERE `id`='161';
UPDATE events_event SET `where`='11825 7 Locks Rd, Potomac, MD 20854, USA', `lat`='39.051068', `lon`='-77.163374' WHERE `id`='162';
UPDATE events_event SET `where`='43 Bethlehem Rd, Littleton, NH 03561, USA', `lat`='44.2982767', `lon`='-71.7678364' WHERE `id`='163';
UPDATE events_event SET `where`='44 Pleasant St, Concord, NH 03301, USA', `lat`='43.203566', `lon`='-71.538146' WHERE `id`='164';
UPDATE events_event SET `where`='4963 Elm St, Bethesda, MD 20814, USA', `lat`='38.982389', `lon`='-77.097996' WHERE `id`='165';

