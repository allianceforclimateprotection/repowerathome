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
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='12';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='13';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='14';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='15';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='16';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='17';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='18';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='19';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='20';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='21';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='22';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='23';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='24';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='25';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='26';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='27';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='28';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='29';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='30';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='31';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='32';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='33';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='34';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='35';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='36';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='37';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='38';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='39';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='40';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='41';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='42';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='43';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='44';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='45';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='46';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='47';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='48';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='49';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='50';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='51';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='52';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='53';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='54';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='55';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='56';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='57';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='58';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='59';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='60';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='61';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='62';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='63';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='64';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='65';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='66';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='67';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='68';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='69';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='70';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='71';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='72';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='73';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='74';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='75';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='76';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='77';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='78';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='79';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='80';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='81';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='82';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='83';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='84';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='85';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='86';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='87';
UPDATE events_event SET `title`='Pilot Energy Meeting' WHERE `id`='88';
UPDATE events_event SET `title`='Fun department event' WHERE `id`='1';
UPDATE events_event SET `title`='Demo event' WHERE `id`='2';

-- Table to link groups to events --
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
    WHEN g.id=43 THEN 6578 -- code for Washington, DC
    WHEN g.id=67 THEN 6578 -- code for Washington, DC
    WHEN g.id=96 THEN 6578 -- code for Washington, DC
    WHEN g.id=106 THEN 6578 -- code for Washington, DC
    WHEN g.id=127 THEN 17257 -- code for Catonsville, MD
    WHEN g.id=166 THEN 17726 -- code for Baltimore, MD
    WHEN g.id=178 THEN 17268 -- code for Towson, MD
    WHEN g.id=181 THEN 6578 -- code for Washington, DC
    WHEN g.id=182 THEN 29830 -- code for Toledo, OH
    WHEN g.id=203 THEN 17447 -- code for Columbia, MD
    WHEN g.id=214 THEN 4415 -- code for San Francisco, CA
    WHEN g.id=215 THEN 17726 -- code for Baltimore, MD
    WHEN g.id=218 THEN 7585 -- code for Miami, FL
    WHEN g.id=236 THEN 41628 -- code for Madison, WI
    WHEN g.id=237 THEN 17726 -- code for Baltimore, MD
    WHEN g.id=245 THEN 40973 -- code for Seattle, WA
    WHEN g.id=247 THEN 3439 -- code for San Gabriel, CA
    WHEN g.id=306 THEN 17726 -- code for Baltimore, MD
    WHEN g.id=365 THEN 17418 -- code for Bel Air, MD
    WHEN g.id=884 THEN 25331 -- code for Wyckoff, NJ
    WHEN g.id=898 THEN 6578 -- code for Washington, DC
    WHEN g.id=1189 THEN 25331 -- code for Wyckoff, NJ
    WHEN g.id=1190 THEN 25331 -- code for Wyckoff, NJ
    WHEN g.id=1286 THEN 19622 -- code for Watertown, MN
    WHEN s.id THEN s.id
    WHEN l.id THEN l.id
    ELSE 6578 -- if we can't guest, set the default to Washington, DC
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

-- Add new columns, lon & lat, to the groups table
ALTER TABLE groups_group ADD lat DOUBLE PRECISION NULL AFTER headquarters_id;
ALTER TABLE groups_group ADD lon DOUBLE PRECISION NULL AFTER headquarters_id;
-- Add lat,lon data for all non geo groups
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='26';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='43';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='67';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='89';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='96';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='106';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='115';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='127';
UPDATE `groups_group` SET `lat`='38.9906657', `lon`='-77.026088' WHERE `id`='156';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='166';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='178';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='181';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='182';
UPDATE `groups_group` SET `lat`='39.203', `lon`='-76.857981' WHERE `id`='203';
UPDATE `groups_group` SET `lat`='38.8048355', `lon`='-77.0469214' WHERE `id`='212';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='214';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='215';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='218';
UPDATE `groups_group` SET `lat`='42.583645', `lon`='-83.2454883' WHERE `id`='234';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='236';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='237';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='240';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='241';
UPDATE `groups_group` SET `lat`='42.583645', `lon`='-83.2454883' WHERE `id`='244';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='245';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='247';
UPDATE `groups_group` SET `lat`='38.8048355', `lon`='-77.0469214' WHERE `id`='248';
UPDATE `groups_group` SET `lat`='38.9906657', `lon`='-77.026088' WHERE `id`='249';
UPDATE `groups_group` SET `lat`='39.6067789', `lon`='-75.8332718' WHERE `id`='266';
UPDATE `groups_group` SET `lat`='38.2526647', `lon`='-85.7584557' WHERE `id`='278';
UPDATE `groups_group` SET `lat`='38.8048355', `lon`='-77.0469214' WHERE `id`='305';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='306';
UPDATE `groups_group` SET `lat`='41.6005448', `lon`='-93.6091064' WHERE `id`='317';
UPDATE `groups_group` SET `lat`='39.0181651', `lon`='-77.2085914' WHERE `id`='322';
UPDATE `groups_group` SET `lat`='38.9906657', `lon`='-77.026088' WHERE `id`='338';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='357';
UPDATE `groups_group` SET `lat`='38.9906657', `lon`='-77.026088' WHERE `id`='359';
UPDATE `groups_group` SET `lat`='39.2720509', `lon`='-76.7319161' WHERE `id`='360';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='365';
UPDATE `groups_group` SET `lat`='39.2903848', `lon`='-76.6121893' WHERE `id`='367';
UPDATE `groups_group` SET `lat`='41.5628294', `lon`='-83.6538244' WHERE `id`='494';
UPDATE `groups_group` SET `lat`='40.7607793', `lon`='-111.8910474' WHERE `id`='583';
UPDATE `groups_group` SET `lat`='39.6428362', `lon`='-84.2866083' WHERE `id`='660';
UPDATE `groups_group` SET `lat`='41.2381', `lon`='-85.8530469' WHERE `id`='712';
UPDATE `groups_group` SET `lat`='36.6850612', `lon`='-93.1199012' WHERE `id`='765';
UPDATE `groups_group` SET `lat`='41.7354861', `lon`='-111.834388' WHERE `id`='800';
UPDATE `groups_group` SET `lat`='38.646991', `lon`='-90.224967' WHERE `id`='811';
UPDATE `groups_group` SET `lat`='39.0181651', `lon`='-77.2085914' WHERE `id`='864';
UPDATE `groups_group` SET `lat`='38.9784453', `lon`='-76.4921829' WHERE `id`='867';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='884';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='885';
UPDATE `groups_group` SET `lat`='41.012833', `lon`='-81.6051221' WHERE `id`='886';
UPDATE `groups_group` SET `lat`='38.9342776', `lon`='-77.1774801' WHERE `id`='890';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='891';
UPDATE `groups_group` SET `lat`='38.8048355', `lon`='-77.0469214' WHERE `id`='892';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='898';
UPDATE `groups_group` SET `lat`='38.8048355', `lon`='-77.0469214' WHERE `id`='902';
UPDATE `groups_group` SET `lat`='47.6062095', `lon`='-122.3320708' WHERE `id`='909';
UPDATE `groups_group` SET `lat`='39.178889', `lon`='-76.957778' WHERE `id`='914';
UPDATE `groups_group` SET `lat`='39.9611755', `lon`='-82.9987942' WHERE `id`='1016';
UPDATE `groups_group` SET `lat`='35.6009452', `lon`='-82.554015' WHERE `id`='1023';
UPDATE `groups_group` SET `lat`='39.4212175', `lon`='-76.6260805' WHERE `id`='1028';
UPDATE `groups_group` SET `lat`='37.9357576', `lon`='-122.3477486' WHERE `id`='1041';
UPDATE `groups_group` SET `lat`='43.2081366', `lon`='-71.5375718' WHERE `id`='1046';
UPDATE `groups_group` SET `lat`='43.2081366', `lon`='-71.5375718' WHERE `id`='1070';
UPDATE `groups_group` SET `lat`='39.2903848', `lon`='-76.6121893' WHERE `id`='1106';
UPDATE `groups_group` SET `lat`='39.2903848', `lon`='-76.6121893' WHERE `id`='1131';
UPDATE `groups_group` SET `lat`='43.2081366', `lon`='-71.5375718' WHERE `id`='1141';
UPDATE `groups_group` SET `lat`='38.9806658', `lon`='-77.100256' WHERE `id`='1142';
UPDATE `groups_group` SET `lat`='43.13194', `lon`='-71.54972' WHERE `id`='1146';
UPDATE `groups_group` SET `lat`='38.9906657', `lon`='-77.026088' WHERE `id`='1152';
UPDATE `groups_group` SET `lat`='40.75839', `lon`='-82.5154471' WHERE `id`='1163';
UPDATE `groups_group` SET `lat`='42.0411414', `lon`='-87.6900587' WHERE `id`='1166';
UPDATE `groups_group` SET `lat`='39.3702773', `lon`='-94.7824609' WHERE `id`='1172';
UPDATE `groups_group` SET `lat`='37.365833', `lon`='-76.313889' WHERE `id`='1182';
UPDATE `groups_group` SET `lat`='40.7989473', `lon`='-81.378447' WHERE `id`='1185';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='1189';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='1190';
UPDATE `groups_group` SET `lat`='47.7623204', `lon`='-122.2054035' WHERE `id`='1198';
UPDATE `groups_group` SET `lat`='42.8614748', `lon`='-71.6253487' WHERE `id`='1199';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='1206';
UPDATE `groups_group` SET `lat`='36.2326362', `lon`='-80.7081209' WHERE `id`='1210';
UPDATE `groups_group` SET `lat`='38.8048355', `lon`='-77.0469214' WHERE `id`='1245';
UPDATE `groups_group` SET `lat`='41.3259134', `lon`='-75.7893604' WHERE `id`='1253';
UPDATE `groups_group` SET `lat`='47.3073228', `lon`='-122.2284532' WHERE `id`='1271';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='1286';
UPDATE `groups_group` SET `lat`='33.1192068', `lon`='-117.086421' WHERE `id`='1290';
UPDATE `groups_group` SET `lat`='39.4014955', `lon`='-76.6019125' WHERE `id`='1294';
UPDATE `groups_group` SET `lat`='39.2667819', `lon`='-74.644881' WHERE `id`='1317';
UPDATE `groups_group` SET `lat`='39.2903848', `lon`='-76.6121893' WHERE `id`='1321';
UPDATE `groups_group` SET `lat`='44.8927439', `lon`='-93.034938' WHERE `id`='1375';
UPDATE `groups_group` SET `lat`='35.4675602', `lon`='-97.5164276' WHERE `id`='1438';
UPDATE `groups_group` SET `lat`='39.0992752', `lon`='-76.8483061' WHERE `id`='1457';
UPDATE `groups_group` SET `lat`='39.9403453', `lon`='-82.0131924' WHERE `id`='1468';
UPDATE `groups_group` SET `lat`='33.6839473', `lon`='-117.7946942' WHERE `id`='1487';
UPDATE `groups_group` SET `lat`='39.1637984', `lon`='-119.7674034' WHERE `id`='1503';
UPDATE `groups_group` SET `lat`='38.8951118', `lon`='-77.0363658' WHERE `id`='1522';

-- Migrate comments to threadedcomments --
INSERT INTO threadedcomments_comment (comment_ptr_id, title, parent_id, last_child_id, tree_path)
SELECT id, '', NULL, NULL, LPAD(id, 10, '0')
FROM django_comments;

-- Attach all of the previsous ratings to the new threadedcomments --
UPDATE rateable_ratings r, django_content_type ct
SET r.content_type_id = ct.id
WHERE ct.app_label = 'threadedcomments' AND ct.model = 'threadedcomment';

-- Attach all of the previous flags to the new threadedcomments --
UPDATE flagged_flags f, django_content_type ct
SET f.content_type_id = ct.id
WHERE ct.app_label = 'threadedcomments' AND ct.model = 'threadedcomment';


-- Feature two communities for the home page --
UPDATE `groups_group` SET `is_featured`='1' WHERE `id`='106';
UPDATE `groups_group` SET `is_featured`='1' WHERE `id`='1141';

--create action badges
INSERT INTO brabeion_badgeaward (user_id, awarded_at, slug, level)
SELECT uap.user_id, NOW(), CONCAT(a.slug, '-action-badge'), 0
FROM actions_useractionprogress uap
JOIN actions_action a ON uap.action_id = a.id
WHERE uap.is_completed = 1;

--create trendsetter badges
INSERT INTO brabeion_badgeaward (user_id, awarded_at, slug, level)
SELECT cn.user_id, NOW(), 'trendsetter-badge', 0
FROM commitments_commitment cm
JOIN commitments_contributor cn ON cm.contributor_id = cn.id
WHERE cm.question = 'pledge' AND cm.answer = 'True' AND cn.user_id IS NOT NULL;

--create hosting hero badges
INSERT INTO brabeion_badgeaward (user_id, awarded_at, slug, level)
SELECT DISTINCT e.creator_id, NOW(), 'hosting-hero-badge', 0
FROM events_event e;

--create gift of gab badges
INSERT INTO brabeion_badgeaward (user_id, awarded_at, slug, level)
SELECT c.user_id, NOW(), 'gift-of-gab', 
CASE 
    WHEN COUNT(c.user_id) >= 15 THEN 3
    WHEN COUNT(c.user_id) >= 5 THEN 2
    ELSE 1
END
FROM django_comments c
GROUP BY c.user_id;

--create paparazzi badges
INSERT INTO brabeion_badgeaward (user_id, awarded_at, slug, level)
SELECT DISTINCT u.id, NOW(), 'paparazzi-badge', 0
FROM media_widget_stickerimage s
JOIN auth_user u on s.email = u.email;

--create momentum builder badges
INSERT INTO brabeion_badgeaward (user_id, awarded_at, slug, level)
SELECT DISTINCT i.user_id, NOW(), 'momentum-builder-badge', 0
FROM invite_invitation i;

--create social media maven badges
INSERT INTO brabeion_badgeaward (user_id, awarded_at, slug, level)
SELECT p.user_id, NOW(), 'social-media-maven-badge',
CASE
    WHEN p.twitter_access_token IS NOT NULL AND p.facebook_access_token IS NOT NULL THEN 2
    WHEN p.twitter_access_token IS NOT NULL OR p.facebook_access_token IS NOT NULL THEN 1
END
FROM rah_profile p
WHERE p.twitter_access_token IS NOT NULL OR p.facebook_access_token IS NOT NULL;

--create follow through badges
INSERT INTO brabeion_badgeaward (user_id, awarded_at, slug, level)
SELECT s.entered_by_id, NOW(), 'follow-through-badge',
CASE
    WHEN COUNT(s.entered_by_id) >= 30 THEN 3
    WHEN COUNT(s.entered_by_id) >= 15 THEN 2
    WHEN COUNT(s.entered_by_id) >= 5 THEN 1
END
FROM commitments_contributorsurvey s
GROUP BY s.entered_by_id
HAVING COUNT(s.entered_by_id) >= 5;

--create shout out badges
INSERT INTO brabeion_badgeaward (user_id, awarded_at, slug, level)
SELECT p.user_id, NOW(), 'shout-out-badge', 0
FROM rah_profile p
WHERE p.twitter_share = 1 or p.facebook_share = 1;

--create storyteller badges
INSERT INTO brabeion_badgeaward (user_id, awarded_at, slug, level)
SELECT p.user_id, NOW(), 'storyteller-badge', 0
FROM rah_profile p
JOIN auth_user u ON p.user_id = u.id
WHERE p.location_id IS NOT NULL AND p.building_type IS NOT NULL AND p.about IS NOT NULL
AND u.first_name != '' AND u.last_name != '';

--create dogged badges
INSERT INTO brabeion_badgeaward (user_id, awarded_at, slug, level)
SELECT uap.user_id, NOW(), 'dogged-badge',
CASE
    WHEN COUNT(uap.user_id) >= 5 THEN 3
    WHEN COUNT(uap.user_id) >= 3 THEN 2
    ELSE 1
END
FROM actions_useractionprogress uap
WHERE uap.is_completed = 1 AND uap.date_committed IS NOT NULL
GROUP BY uap.user_id;

--create unbelievable badges
INSERT INTO brabeion_badgeaward (user_id, awarded_at, slug, level)
SELECT uap.user_id, NOW(), 'unbelievable-badge', 0
FROM actions_useractionprogress uap
WHERE uap.is_completed = 1
GROUP BY uap.user_id
HAVING COUNT(uap.user_id) = (SELECT COUNT(*) FROM actions_action);




# Sequel Pro dump
# Version 2492
# http://code.google.com/p/sequel-pro
#
# Host: 127.0.0.1 (MySQL 5.1.42-log)
# Database: rah_poccuo
# Generation Time: 2011-04-06 17:22:21 -0400
# ************************************************************

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table django_flatpage
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_flatpage`;

CREATE TABLE `django_flatpage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(100) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `enable_comments` tinyint(1) NOT NULL,
  `template_name` varchar(70) NOT NULL,
  `registration_required` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_flatpage_a4b49ab` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

LOCK TABLES `django_flatpage` WRITE;
/*!40000 ALTER TABLE `django_flatpage` DISABLE KEYS */;
INSERT INTO `django_flatpage` (`id`,`url`,`title`,`content`,`enable_comments`,`template_name`,`registration_required`)
VALUES
	(1,'/about/','About [project name]','<h2>[project name] is dedicated to empowering communities and individuals to save energy.</h2>\n <br>\n<h3>Why save energy?</h3>\n<p>Our personal energy choices have a huge impact on our health, our environment and our wallets. By saving energy, we can minimize the need to burn dirty fuels in our communities. That means cleaner air and water for us &mdash; not to mention lower bills and better, more comfortable homes.</p>\n\n<h3>From your home to your community</h3>\n<p>[project name] helps you save energy. But taking action in your own home is just the beginning. To grow our impact, we need to organize our friends, family, and community to save energy and think big.</p>\n\n<p>Spread the message by hosting an energy meeting in your community. You can also get the word out by <a href=\"/teams/\">starting a team</a>. Teams let you and your friends track your progress and support one another as you empower your community.</p>\n\n<h3>Our moment</h3>\n<p>People all over the country are showing their support for a better tomorrow &mdash; are you ready to join them? Get started by <a href=\"/register/\">creating an account</a>. </p>\n',0,'',0),
	(2,'/terms/','Terms of Use','<h2>\n    1. Your Acceptance\n</h2>\n<ul>\n    <li>\n        By using and/or visiting this website (collectively, including all content and functionality available\n        through [project site] the  domain name, the \"Website\"), you signify your agreement to (1) these terms and\n        conditions (the \"Terms of Use\"), and (2) the privacy policy, found at <a\n        href=\"http://[project site]/privacy/\">http://[project site]/privacy/</a> and incorporated here by\n        reference. If you do not agree to any of these terms or the privacy policy, please do not use the Website.\n    </li>\n    <li>\n        Although we may attempt to notify you when major changes are made to these Terms of Use, you should\n        periodically review the most up-to-date version on the Website. We may, in our sole discretion, modify or\n        revise these Terms of Use and policies at any time, and you agree to be bound by such modifications or\n        revisions. Nothing in this Agreement shall be deemed to confer any third-party rights or benefits.\n    </li>\n</ul>\n<h2>\n    2. [project name] Website\n</h2>\n<ul>\n    <li>\n        These Terms of Use apply to all users of the Website, including users who are also contributors of video\n        content, information, and other materials or services on the Website.\n    </li>\n    <li>\n        The Website is owned by the [project owner] (\"we\", \"our\", or \"us\").\n    </li>\n    <li>\n        The Website may contain links to third party websites that are not owned or controlled by us. We have no\n        control over, and assume no responsibility for, the content, privacy policies, or practices of any third\n        party websites. In addition, we will not and cannot censor or edit the content of any third-party site. By\n        using the Website, you expressly relieve the [project owner] from any and all liability arising from your use of\n        any third-party website.\n    </li>\n    <li>\n        Accordingly, we encourage you to be aware when you leave the Website and to read the terms and conditions\n        and privacy policy of each other website that you visit.\n    </li>\n    <li>\n        We have the right but not the obligation to block links from or to the Website at any time.\n    </li>\n</ul>\n<h2>\n    3. General Use of the Website—Permissions and Restrictions\n</h2>\n<p>\n    The [project owner] hereby grants you permission to access and use the Website as set forth in these Terms of Use,\n    provided that:\n</p>\n<ul>\n    <li>\n        You agree not to distribute in any medium any part of the Website, including but not limited to User\n        Submissions (defined below), without our prior written authorization.\n    </li>\n    <li>\n        You agree not to alter or modify any part of the Website.\n    </li>\n    <li>\n        You agree not to access User Submissions (defined below) or Website Content (defined below) through any\n        technology or means other than through the Website itself, or other explicitly authorized means we may\n        designate.\n    </li>\n    <li>\n        You agree not to use the Website for any commercial or non-commercial use without the prior written\n        authorization of the [project owner].\n    </li>\n    <li>\n        In your use of the Website, you will otherwise comply with the terms and conditions of these Terms of Use\n        and all applicable local, national, and international laws and regulations.\n    </li>\n    <li>\n        We reserve the right to discontinue any aspect of the Website at any time.\n    </li>\n</ul>\n<h2>\n    4. Your Use of Content on the Website\n</h2>\n<p>\n    In addition to the general restrictions above, the following restrictions and conditions apply specifically to\n    your use of content on the Website:\n</p>\n<ul>\n    <li>\n        The content on the Website, except all User Submissions (as defined below), including without limitation,\n        the text, software, scripts, graphics, photos, sounds, music, videos, interactive features and the like\n        (\"Content\") and the trademarks, service marks and logos contained therein (\"Marks\"), are owned by or\n        licensed to the [project owner], subject to copyright and other intellectual property rights under the law. Content\n        on the Website is provided to you AS IS for your information and personal use only and may not be\n        downloaded, copied, reproduced, distributed, transmitted, broadcast, displayed, sold, licensed, or otherwise\n        exploited for any other purposes whatsoever without the prior written consent of the respective owners. The\n        [project owner] reserves all rights not expressly granted in and to the Website and the Content.\n    </li>\n    <li>\n        You may access User Submissions for your information and personal use solely as intended through the\n        provided functionality of the Website. You shall not copy or download any User Submission.\n    </li>\n    <li>\n        User Submissions are made available to you for your information and personal use solely as intended through\n        the normal functionality of the Website. User Submissions are made available \"as is\", and may not be used,\n        copied, reproduced, distributed, transmitted, broadcast, displayed, sold, licensed, downloaded, or otherwise\n        exploited in any manner not intended by the normal functionality of the Website or otherwise as prohibited\n        under this Agreement.\n    </li>\n    <li>\n        You may access Content, User Submissions and other content only as permitted under this Agreement. We\n        reserve all rights not expressly granted in and to the Content and the Website.\n    </li>\n    <li>\n        You agree to not engage in the use, copying, or distribution of any of the Content other than expressly\n        permitted herein, including any use, copying, or distribution of User Submissions of third parties obtained\n        through the Website for any commercial purposes.\n    </li>\n    <li>\n        You agree not to circumvent, disable or otherwise interfere with security-related features of the Website or\n        features that prevent or restrict use or copying of any Content or enforce limitations on use of the Website\n        or the Content therein.\n    </li>\n    <li>\n        You understand that when using the Website, you will be exposed to User Submissions from a variety of\n        sources, and that we are not responsible for the accuracy, usefulness, safety, or intellectual property\n        rights of or relating to such User Submissions. You further understand and acknowledge that you may be\n        exposed to User Submissions that are inaccurate, offensive, indecent, or objectionable, and you agree to\n        waive, and hereby do waive, any legal or equitable rights or remedies you have or may have against the\n        [project owner] with respect thereto, and agree to indemnify and hold the [project owner], its directors, officers,\n        employees, agents, affiliates, and/or licensors, harmless to the fullest extent allowed by law regarding all\n        matters related to your use of the site.\n    </li>\n</ul>\n<h2>\n    5. Your User Submissions and Conduct\n</h2>\n<ul>\n    <li>\n        As a user you may submit video content (\"User Videos\") and textual and photo content (\"User Comments\"). User\n        Videos and User Comments are collectively referred to as \"User Submissions.\" You understand that whether or\n        not such User Submissions are published, we do not guarantee any confidentiality with respect to any User\n        Submissions.\n    </li>\n    <li>\n        You shall be solely responsible for your own User Submissions and the consequences of posting or publishing\n        them. In connection with User Submissions, you affirm, represent, and/or warrant that: you own or have the\n        necessary licenses, rights, consents, and permissions to use and authorize us to use all patent, trademark,\n        trade secret, copyright or other proprietary rights in and to any and all User Submissions to enable\n        inclusion and use of the User Submissions in the manner contemplated by the Website and these Terms of Use.\n        </li>\n    <li>\n        For clarity, you retain all of your ownership rights in your User Submissions. However, by submitting User\n        Submissions to us, you hereby grant the [project owner] a worldwide, non-exclusive, royalty-free, sublicenseable\n        and transferable license to use, reproduce, distribute, prepare derivative works of, display, and perform\n        the User Submissions in connection with the Website and our (and our successors\' and affiliates\') business,\n        including without limitation for promoting and redistributing part or all of the Website (and derivative\n        works thereof) in any media formats and through any media channels. You also hereby grant each user of the\n        Website a non-exclusive license to access your User Submissions through the Website, and to use such User\n        Submissions as permitted through the functionality of the Website and under these Terms of Use. The above\n        licenses granted by you in User Submissions terminate within a commercially reasonable time after you remove\n        or delete your User Submission from the Website. You understand and agree, however, that we may retain, but\n        not display, distribute, or perform, server copies of User Submissions that have been removed or deleted.\n        The above licenses granted by you in User Submissions are perpetual and irrevocable.\n    </li>\n    <li>\n        In connection with User Submissions, you further agree that you will not submit material that is\n        copyrighted, protected by trade secret or otherwise subject to third party proprietary rights, including\n        privacy and publicity rights, unless you are the owner of such rights or have permission from their rightful\n        owner to post the material and to grant us all of the license rights granted herein.\n    </li>\n    <li>\n        You further agree that you will not, in connection with User Submissions, submit material that is contrary\n        to the following guidelines, which may be updated from time to time, or contrary to applicable local,\n        national, and international laws and regulations:\n    </li>\n    <li>\n        <ul>\n            <li>\n                We are a non-partisan organization. Do not post videos or comments that include partisan content.\n            </li>\n            <li>\n                Do not post videos or comments that include political electoral content. We seek to provide a forum\n                to discuss policy – not to advance the interests of any particular political party or candidate for\n                office.\n            </li>\n            <li>\n                Do not post videos or comments that include pornographic or sexually explicit content.\n            </li>\n            <li>\n                Do not post videos or comments that include showing graphic or gratuitous violence.\n            </li>\n            <li>\n                Only upload videos or comments that you made or that you are authorized to use. This means don\'t\n                upload videos or comments you didn\'t make, or use content in your videos or comments that someone\n                else owns the copyright to, such as music tracks, snippets of copyrighted programs, or videos made\n                by other users, without necessary authorizations.\n            </li>\n            <li>\n                Do not post videos or comments that include hate speech (speech which attacks or demeans a group\n                based on race or ethnic origin, religion, disability, gender, age, veteran status, and sexual\n                orientation/gender identity).\n            </li>\n            <li>\n                Do not post videos or comments intended to solicit business or promote any products for use or sale.\n            </li>\n        </ul>\n    </li>\n    <li>\n        We do not endorse any User Submission or any opinion, recommendation, or advice expressed therein, and we\n        expressly disclaim any and all liability in connection with User Submissions. We do not permit copyright\n        infringing activities and infringement of intellectual property rights on the Website, and we will remove\n        all Content and User Submissions if properly notified that such Content or User Submission infringes on\n        another\'s intellectual property rights. We reserve the right in our sole discretion to remove Content and\n        User Submissions without prior notice.\n    </li>\n</ul>\n<h2>\n    6. Claims of Copyright Infringement\n</h2>\n<p>\n    The Digital Millennium Copyright Act of 1998 (the \"DMCA\") provides recourse for copyright owners who believe\n    that material appearing on the Internet infringes their rights under U.S. copyright law. If you believe in good\n    faith that materials hosted by us infringe your copyright, you (or your agent) may send us a notice requesting\n    that the material be removed, or access to it blocked. Notices and counter-notices must meet the then-current\n    statutory requirements imposed by the DMCA; see <a href=\"http://www.loc.gov/copyright/\">\n    http://www.loc.gov/copyright/</a> for details. Notices and counter-notices with respect to [project site] \n    should be sent by email to:\n</p>\n<p>\n    feedback@[project site]\n</p>\n<h2>\n    7. Warranty Disclaimer\n</h2>\n<p>\n    YOU AGREE THAT YOUR USE OF THE WEBSITE SHALL BE AT YOUR SOLE RISK. TO THE FULLEST EXTENT PERMITTED BY LAW, THE\n    [project owner], ITS OFFICERS, DIRECTORS, EMPLOYEES, AND AGENTS DISCLAIM ALL WARRANTIES, EXPRESS OR IMPLIED, IN\n    CONNECTION WITH THE WEBSITE AND YOUR USE THEREOF. WE MAKE NO WARRANTIES OR REPRESENTATIONS ABOUT THE ACCURACY OR\n    COMPLETENESS OF THIS WEBSITE\'S CONTENT OR THE CONTENT OF ANY WEBSITES LINKED TO THIS SITE AND ASSUME NO\n    LIABILITY OR RESPONSIBILITY FOR ANY (I) ERRORS, MISTAKES, OR INACCURACIES OF CONTENT, (II) PERSONAL INJURY OR\n    PROPERTY DAMAGE, OF ANY NATURE WHATSOEVER, RESULTING FROM YOUR ACCESS TO AND USE OF OUR WEBSITE, (III) ANY\n    UNAUTHORIZED ACCESS TO OR USE OF OUR SECURE SERVERS AND/OR ANY AND ALL PERSONAL INFORMATION AND/OR FINANCIAL\n    INFORMATION STORED THEREIN, (IV) ANY INTERRUPTION OR CESSATION OF TRANSMISSION TO OR FROM OUR WEBSITE, (IV) ANY\n    BUGS, VIRUSES, TROJAN HORSES, OR THE LIKE WHICH MAY BE TRANSMITTED TO OR THROUGH OUR WEBSITE BY ANY THIRD PARTY,\n    AND/OR (V) ANY ERRORS OR OMISSIONS IN ANY CONTENT OR FOR ANY LOSS OR DAMAGE OF ANY KIND INCURRED AS A RESULT OF\n    THE USE OF ANY CONTENT POSTED, EMAILED, TRANSMITTED, OR OTHERWISE MADE AVAILABLE VIA THE WEBSITE.\n</p>\n<h2>\n    8. Limitation of Liability\n</h2>\n<p>\n    IN NO EVENT SHALL THE [project owner], ITS OFFICERS, DIRECTORS, EMPLOYEES, OR AGENTS, BE LIABLE TO YOU FOR ANY DIRECT,\n    INDIRECT, INCIDENTAL, SPECIAL, PUNITIVE, OR CONSEQUENTIAL DAMAGES WHATSOEVER RESULTING FROM ANY (I) ERRORS,\n    MISTAKES, OR INACCURACIES OF CONTENT, (II) PERSONAL INJURY OR PROPERTY DAMAGE, OF ANY NATURE WHATSOEVER,\n    RESULTING FROM YOUR ACCESS TO AND USE OF OUR WEBSITE, (III) ANY UNAUTHORIZED ACCESS TO OR USE OF OUR SECURE\n    SERVERS AND/OR ANY AND ALL PERSONAL INFORMATION AND/OR FINANCIAL INFORMATION STORED THEREIN, (IV) ANY\n    INTERRUPTION OR CESSATION OF TRANSMISSION TO OR FROM OUR WEBSITE, (IV) ANY BUGS, VIRUSES, TROJAN HORSES, OR THE\n    LIKE, WHICH MAY BE TRANSMITTED TO OR THROUGH OUR WEBSITE BY ANY THIRD PARTY, AND/OR (V) ANY ERRORS OR OMISSIONS\n    IN ANY CONTENT OR FOR ANY LOSS OR DAMAGE OF ANY KIND INCURRED AS A RESULT OF YOUR USE OF ANY CONTENT POSTED,\n    EMAILED, TRANSMITTED, OR OTHERWISE MADE AVAILABLE VIA THE WEBSITE, WHETHER BASED ON WARRANTY, CONTRACT, TORT, OR\n    ANY OTHER LEGAL THEORY, AND WHETHER OR NOT WE ARE ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. THE FOREGOING\n    LIMITATION OF LIABILITY SHALL APPLY TO THE FULLEST EXTENT PERMITTED BY LAW IN THE APPLICABLE JURISDICTION.\n</p>\n<p>\n    YOU SPECIFICALLY ACKNOWLEDGE THAT WE SHALL NOT BE LIABLE FOR USER SUBMISSIONS OR THE DEFAMATORY, OFFENSIVE, OR\n    ILLEGAL CONDUCT OF ANY THIRD PARTY AND THAT THE RISK OF HARM OR DAMAGE FROM THE FOREGOING RESTS ENTIRELY WITH\n    YOU.\n</p>\n<p>\n    The Website is controlled and offered by us from our facilities in the United States of America. We make no\n    representations that the Website is appropriate or available for use in other locations. Those who access or use\n    the Website from other jurisdictions do so at their own volition and are responsible for compliance with local\n    law.\n</p>\n<h2>\n    9. Indemnity\n</h2>\n<p>\n    You agree to defend, indemnify and hold harmless the [project owner], its officers, directors, employees and agents,\n    from and against any and all claims, damages, obligations, losses, liabilities, costs or debt, and expenses\n    (including but not limited to attorney\'s fees) arising from: (i) your use of and access to the Website; (ii)\n    your violation of any term of these Terms of Use; (iii) your violation of any third party right, including\n    without limitation any copyright, property, or privacy right; or (iv) any claim that one of your User\n    Submissions caused damage to a third party. This defense and indemnification obligation will survive these Terms\n    of Use and your use of the Website.\n</p>\n<h2>\n    10. Ability to Accept Terms of Use\n</h2>\n<p>\n    You affirm that you are either more than 18 years of age, or an emancipated minor, or possess legal parental or\n    guardian consent, and are fully able and competent to enter into the terms, conditions, obligations,\n    affirmations, representations, and warranties set forth in these Terms of Use, and to abide by and comply with\n    these Terms of Use. In any case, you affirm that you are over the age of 13, as the Website is not intended for\n    children under 13. If you are under 13 years of age, then please do not use the Website.\n</p>\n<h2>\n    11. Assignment\n</h2>\n<p>\n    These Terms of Use, and any rights and licenses granted hereunder, may not be transferred or assigned by you,\n    but may be assigned by us without restriction.\n</p>\n<h2>\n    12. General\n</h2>\n<p>\n    You agree that: (i) the Website shall be deemed solely based in the District of Columbia; and (ii) the Website\n    shall be deemed a passive website that does not give rise to personal jurisdiction over us, either specific or\n    general, in jurisdictions other than the District of Columbia. These Terms of Use shall be governed by the\n    internal substantive laws of the District of Columbia, without respect to its conflict of laws principles. Any\n    claim or dispute between you and us that arises in whole or in part from your use of the Website shall be\n    decided exclusively by a court of competent jurisdiction located in the District of Columbia. These Terms of\n    Use, together with the Privacy Policy at <a\n    href=\"http://[project site]/privacy/\">http://[project site]/privacy/</a> and any other legal notices\n    published by use on the Website, shall constitute the entire agreement between you and us concerning the\n    Website. If any provision of these Terms of Use is deemed invalid by a court of competent jurisdiction, the\n    invalidity of such provision shall not affect the validity of the remaining provisions of these Terms of Use,\n    which shall remain in full force and effect. No waiver of any term of these Terms of Use shall be deemed a\n    further or continuing waiver of such term or any other term, and our failure to assert any right or provision\n    under these Terms of Use shall not constitute a waiver of such right or provision. We reserve the right to amend\n    these Terms of Use at any time and without notice, and it is your responsibility to review these Terms of Use\n    for any changes. Your use of the Website following any amendment of these Terms of Use will signify your assent\n    to and acceptance of its revised terms. YOU AND US AGREE THAT ANY CAUSE OF ACTION ARISING OUT OF OR RELATED TO\n    THE WEBSITE MUST COMMENCE WITHIN ONE (1) YEAR AFTER THE CAUSE OF ACTION ACCRUES. OTHERWISE, SUCH CAUSE OF ACTION\n    IS PERMANENTLY BARRED.\n</p>\n\n',0,'',0),
	(3,'/privacy/','Privacy Policy','<p>\n    We are very sensitive to online privacy concerns. This online privacy statement describes how we treat all user data\n    collected, if any, during your visit to the [project owner]\'s [project name] website (the\n    \"Website\").\n</p>\n<h2>\n    Collection of personally identifiable information\n</h2>\n<p>\n    On this Website, you can request more information about our goals and programs, download materials and enjoy other\n    interactive services. The types of personally identifiable information that may be collected on these pages include:\n    name, address, email address, telephone number, fax number, and information about your preferences.\n</p>\n<h2>\n    Privacy of our email list and personal information\n</h2>\n<p>\n    The [project owner] for Climate Protection (\"we,\" \"our\", or \"us\") maintains an email list to keep\n    interested parties informed about its various activities. Individuals can unsubscribe from the email list at\n    anytime. We collect and use your personal information to operate the Website and to deliver any services you have\n    requested. These services may include the display of customized content based upon the information we have collected\n    (for example, special information for users living in a particular region or state).\n</p>\n<p>\n    Only [project owner] staff and our authorized agents have access to personally identifiable information provided by\n    visitors to this Website in order to better serve you. People who affirmatively submit their contact information\n    through the Website may be contacted by [project owner] staff or authorized agents.\n</p>\n<p>\n    We do not share the information you\'ve given us with unaffiliated groups without your explicit permission. We may\n    share some of your personal information with the following affiliated groups:\n</p>\n<ul>\n    <li>\n        Affiliated Third Parties — for example, our database administrators (for the sole purpose of helping us do our\n        work) or affiliated campaigns, which share our mission and privacy concerns.\n    </li>\n    <li>\n        Third Party Administrators, such as organizations we engage to facilitate large distribution of messages.\n    </li>\n</ul>\n<h2>\n    Collection and Use of Children\'s Personal Information\n</h2>\n<p>\n    We do not solicit personally identifying information from children. Visitors who are under 13 years of age should\n    ask their parent or legal guardian for assistance when using the Website and should not submit any personally\n    identifying information to the Website.\n</p>\n<h2>\n    Use of Cookies\n</h2>\n<p>\n    We may use cookies to tailor your experience on this Website according to the preferences you have specified. When\n    you visit the Website, your browser may save a tiny piece of information on your computer. This information\n    personalizes and improves your experience online. It is not possible and we do not attempt to access information\n    from other websites. Our cookies do not contain any personal identifiable information. You have the ability to\n    accept or decline cookies. Most Web browsers automatically accept cookies, but you can usually modify your browser\n    setting to decline cookies if you prefer. If you chose to decline cookies, you may not be able to fully experience\n    all features of [project site].\n</p>\n<h2>\n    IP Addresses, Log Files, and Data Analysis\n</h2>\n<p>\n    As with any website operator, we analyze our Website logs to constantly improve the value of Website. We use an\n    external service to provide real-time reporting to us and our authorized agents of browser accesses to our Website.\n    This includes page views, unique visitors, repeat visitors, frequency of visits, and peak-volume traffic periods. We\n    do not use this service to gather, request, record, require, collect, or track any Internet users\' personally\n    identifiable information.\n</p>\n<p>\n    We log IP addresses which describe the location of your computer or network on the Internet. This information is\n    helpful for systems administration and troubleshooting purposes. We may also use third-party services such as Google\n    Analytics. These practices help us understand traffic patterns and know if there are problems with our Website. We\n    may also use embedded images in emails to track open rates for our mailings. This practice helps us determine which\n    mailings appeal most to our members.\n</p>\n<p>\n    URLs contained in emails may contain an ID that enables us to correctly identify the person who takes an action\n    using a web page. We use URLs to simplify the process of signing petitions and filling out surveys. We may\n    occasionally present a shortened URL that references a longer URL that contains an ID. We do this to simplify the\n    display, to prevent links from becoming broken when copied, and to ensure compatibility with email programs that do\n    not handle long URLs. When shortened URL is displayed in an email, you will see the full URL in the browser\'s\n    address bar when you access the page.\n</p>\n<h2>\n    Petitions and Surveys\n</h2>\n<p>\n    For petitions and surveys you\'ve signed or completed, we treat your name, city, state, and comments as public\n    information &ndash; for example, we may provide compilations of petitions, with your comments, to the intended recipient\n    of the petition or survey. We will not make your street address publicly available, but we may transmit it to the\n    intended recipient of the petition or survey as part of the petition or survey. This is standard industry practice\n    in such situations. In no such case will we disclose your email address or phone number, without your permission. We\n    may also make your comments, along with your first name, city and state available to the press and public online.\n</p>\n<h2>\n    Changes to this Statement\n</h2>\n<p>\n    We may occasionally update this privacy statement especially as new features are added to this Website. If there are\n    material changes to this statement or in how we will use your personal information, we will prominently note such\n    changes prior to their implementation. We encourage you to periodically review this page to be informed of how we\n    are protecting your information.\n</p>',0,'',0),
	(4,'/coal-challenge/','The October 10th Coal Challenge','<p>October 10th, 2010 is an international day of action on climate change. To show our support, <strong>we’re challenging our members to reduce their energy use by the equivalent of <del>one million</del> seven million pounds of coal</strong>. Reaching this goal will demonstrate that thousands of people around the country are personally committed to a cleaner, healthier America.</p>\r\n\r\n<h2>Join the challenge</h2>\r\n<p>Join the challenge by <a href=\"/register/\">creating an account</a> and <a href=\"/actions/\">taking action</a> in your home. Each action you complete saves energy and earns points. For example, the annual energy savings from <a href=\"/actions/programmable-thermostat/\">programming your thermostat</a> is equivalent to diverting 870 pounds of coal from a power plant. By completing this action, you could earn 870 points and contribute 870 pounds to the challenge goal.</p>\r\n\r\n<h2>Bring the challenge to your community</h2>\r\n<p>We can only reach our ambitious goal by getting everyone involved. Engage members of your community by hosting an energy meeting. Energy meeting are a great way to introduce people to the challenge and get them excited about saving energy as part of <a href=\"/teams/\">team</a>.</p>\r\n\r\n<h2>Assumptions and methodology behind the numbers</h2>\r\n<h3>Turning energy savings into coal savings</h3>\r\n<p>The October 10th Coal Challenge has two major goals: to reduce energy and to help people better visualize the amount of energy they use in their home. Carbon dioxide and kilowatt-hours are pretty abstract (not to mention invisible) so we decided to instead use pounds of coal to represent energy savings.</p>\r\n\r\n<p>There are many uncertainties involved in estimating energy and coal savings. Each state has a different electricity mix, meaning that in some states almost 100% of the electricity comes from coal, whereas in other states a large percentage of electricity may come from natural gas, nuclear power, hydropower, etc. The electricity mix can vary throughout the day as well—for example, during the afternoon, when electricity demand is high, more natural gas plants might be turned on. There are also a lot of factors that vary among homes—size, number of occupants, energy consumption habits, appliance choices, location, etc. Many homes use natural gas (and some use oil) rather than electricity for heating purposes. </p>\r\n\r\n<p>Because of these reasons, we decided to keep it simple. In general, we used middle-of-the-road assumptions and a one-year timeframe to calculate energy savings. We used “points” to represent pounds of coal. One pound of coal would need to be burned in a power plant to provide one point’s worth of energy. This is a symbolic way to think about energy use. Because coal does not provide 100% of America’s residential energy, some of the energy you save in your home will not directly eliminate coal. It might mean your local power plant uses less natural gas (preventing carbon pollution) or fewer emissions are released from your home’s oil or gas burning furnace, for example. But for this Challenge, we use coal as our common measurement as a powerful symbol of the choice that we face as we seek to address climate change.</p>\r\n\r\n<h3>Detailed calculations</h3>\r\n<p>Feeling really wonky and ready to bust out your slide rule? Here is a more detailed explanation of our calculations. As explained above, our estimates for “pounds of coal saved” by a given action are directly proportional to the energy savings of that action. We derived energy savings estimates primarily from the U.S. Department of Energy and the U.S. Environmental Protection Agency. We used a streamlined conversion factor to determine how much coal would need to be burned in an average U.S. coal-fired power plant to provide the energy equivalent of one kWh of electricity to a home. Average energy savings from water and space heating were converted from BTUs to kWh. The average heat content of coal consumed in the U.S. is approximately 20 million BTUs per short ton ; the efficiency of the average U.S. coal plant is approximately 32% ; and transmission and distribution losses amount to about 6% . Thus:</p>\r\n\r\n<p>(2000 lbs/short ton) x (short ton/20,000,000 BTU) x (3412 BTU/kWh) / 0.32 / 0.94 = 1.13 lbs coal per kWh</p>\r\n\r\n',0,'',0),
	(5,'/faq/','Frequently Asked Questions','<h3>What are points? How are they calculated?</h3>\n<p>Points are estimates of the annual energy savings represented by each action. One point is equivalent to the energy of burning one pound of coal.</p>\n<p>Unfortunately, calculating typical energy savings is not an exact science and we’re often in the position of comparing apples and oranges ... or windows and light bulbs. As if that wasn\'t enough, every home is unique, and your results may vary significantly from the \"typical\" home we use in our calculations.</p>\n<p>Even though they\'re not precise estimates, points are still valuable. Points help users understand the relative impact of each action and symbolize the rising impact of our collective actions.</p>\n\n<h3>I have another question - how can I get in touch with you?</h3>\n<p>For general inquiries, drop us a line at <a href=\"mailto:feedback@[project site]\">feedback@[project site]</a>.\n\n',0,'',0),
	(7,'/hosting/','Meeting Materials','<p>These materials will help you plan and execute a great event!</p>\n<h3>Plan your event (start here!)</h3>\n<ul>\n<li><strong><a href=\"http://rahstatic.s3.amazonaws.com/meeting_materials/Host Guide.pdf\">Organizing guide</a></strong> (PDF): This guide will take you through the entire process of organizing a meeting, from creating an event, to inviting guests, to doing follow-up.</li>\n</ul>\n\n<h3>Spread the word</h3>\n<ul>\n<li><strong><a href=\"http://rahstatic.s3.amazonaws.com/meeting_materials/Flyer.doc\">Flyer</a></strong> (Microsoft Word): Download and edit this flyer with your meeting\'s details</li>\n</ul>\n\n<h3>Meeting presentation</h3>\n<ul>\n<li><strong><a href=\"http://rahstatic.s3.amazonaws.com/meeting_materials/Meeting Guide.pdf\">Presentation guide</a></strong> (PDF): This document will walk you through the meeting agenda and content, so you\'ll feel comfortable during the event.</li>\n<br />\n<li><strong>Presentation</strong>: Use this slide show during your energy meeting. </li>\n<ul>\n<li><a href=\"http://rahstatic.s3.amazonaws.com/meeting_materials/Home Energy Meeting.ppt\">Home Version</a> (Microsoft PowerPoint)</li>\n<li><a href=\"http://rahstatic.s3.amazonaws.com/meeting_materials/Apartment Energy Meeting.ppt\">Apartment Version</a> (Microsoft PowerPoint)</li>\n</ul>\n</ul>\n\n<h3>Attendee handouts</h3>\n<p>Download and print these materials before your energy meeting. You\'ll find separate sets for meetings aimed at apartment residents/renters and homeowners.</p>\n<ul>\n<li><strong><a href=\"http://rahstatic.s3.amazonaws.com/meeting_materials/Trendsetter Sticker.pdf\">Trendsetter Badge</a></strong> (PDF): A way for guests to proudly display their Trendsetter status!</li>\n<li><strong><a href=\"http://rahstatic.s3.amazonaws.com/meeting_materials/sign in sheet.pdf\">Sign-in Sheet</a></strong> (PDF): Keep track of who came to your event.</li>\n<br />\n<li><strong>Attendee Packet</strong>: A guide for your guests to take home that gives a little more information on completing the four core energy actions.</li>\n<ul>\n<li><a href=\"http://rahstatic.s3.amazonaws.com/meeting_materials/Home actions guide.pdf\">Home Actions</a> (PDF)</li>\n<li><a href=\"http://rahstatic.s3.amazonaws.com/meeting_materials/Apartment actions guide.pdf\">Apartment Actions</a> (PDF)</li>\n</ul>\n<li><strong>Pledge Cards</strong>: Guests use the card to sign the Trendsetter Pledge and take action by committing to energy actions. After your meeting, you enter the commitments on [project site], which loads up your guests\' accounts and sets them up for energy-saving success.</li>\n<ul>\n<li><a href=\"http://rahstatic.s3.amazonaws.com/meeting_materials/home pledge card.pdf\">Home Version</a> (PDF)</li>\n<li><a href=\"http://rahstatic.s3.amazonaws.com/meeting_materials/apartment pledge card.pdf\">Apartment Version</a> (PDF)</li>\n</ul>\n<li><strong><a href=\"http://rahstatic.s3.amazonaws.com/meeting_materials/activity sheet v2.pdf\">Activity Sheets</a></strong> (PDF): People who make plans are much more likely to follow through on those commitments. These sheets are meant to guide your guests in completing their actions. Use them when going over the actions.</li>\n</ul>\n\n<h2>Frequently asked questions</h2>\n<h3>How do I host?</h3>\n<p>\n    [project name]\'s toolkit makes it easy to invite guests, manage RSVPs, and hold a great event. Get started\n    by <a href=\"http://rahstatic.s3.amazonaws.com/meeting_materials/Host%20Guide.pdf\">downloading the host\n    guide</a>. You can also review other materials that will help you organize and run your event. Check out the\n    other materials at the top of this page.    \n</p>\n<h3>What happens at a meeting?</h3>\n<p>\n    The meeting introduces guests to <b>four actions</b> almost anyone can do. Guests <b>make commitments</b> to\n    take these actions, and <b>brainstorm next steps</b> they can take together to get even more people\n    involved.\n</p>\n\n<h3>Who hosts meetings?</h3>\n<p>\n    <b>Anyone, from engineers to English teachers, can host a meeting</b>. You don?t need to be an energy\n    efficiency expert to host &ndash; in fact, you don?t need to have any background in the topic at all.\n</p>\n<object width=\"432\" height=\"268\">\n    <param name=\"movie\" value=\"http://www.youtube.com/v/gcK06I0Jd9o&amp;hl=en_US&amp;fs=1?rel=0\"></param>\n    <param name=\"allowFullScreen\" value=\"true\"></param>\n    <param name=\"allowscriptaccess\" value=\"always\"></param>\n    <embed src=\"http://www.youtube.com/v/gcK06I0Jd9o&amp;hl=en_US&amp;fs=1?rel=0\"\n           type=\"application/x-shockwave-flash\" \n           allowscriptaccess=\"always\" \n           allowfullscreen=\"true\" \n           width=\"432\" \n           height=\"268\"></embed>\n</object>\n<p>\n    Listen to Elena talk about why she decided to host an energy meeting\n</p>',0,'',0),
	(8,'/why-save-energy/','Why save energy?','<h3>Saving energy will improve our environment</h3>\r\n<ul><li>More than one-fifth of U.S. greenhouse gas emissions come from the energy used by our homes.</li>\r\n<li>Around half of our electricity comes from coal &mdash; one of the dirtiest fuels. Coal power plants pollute our air and water, exasperating problems like asthma and smog in local communities.</li>\r\n<li>By saving energy, <strong>you can directly reduce the need to burn dirty fuels</strong> and help secure a cleaner future.</li></ul>\r\n\r\n<h3>Saving energy is a smart investment in our future.</h3>\r\n<ul><li>The U.S. has the potential to reduce annual non-transportation energy consumption by roughly 23 percent by 2020, <strong>eliminating more than $1.2 trillion in waste</strong> and making energy bills more affordable for families.</li>\r\n<li>This opportunity is on our doorsteps. We don’t need to wait for political action or new technologies &mdash; we can start saving right now.</li></ul>\r\n\r\n<h3>Saving energy sends a powerful message to local and national decision makers.</h3> \r\n<ul>\r\n<li>Actions speak louder than words. By saving energy in your own home, you’re demonstrating your personal commitment to a cleaner future.</li>\r\n<li>As individuals organize their communities to take action, it will become clear that there is broad, deep-rooted support for action. The message is that Americans aren’t waiting to solve the climate crisis, and <strong>our elected officials need to join us in being a part of the solution</strong>.</li></ul>\r\n',0,'',0),
	(11,'/about-pledge/','The Energy Trendsetter Pledge','<p align=\"center\" style=\"font-size:16pt\"><em>I pledge to save energy in my home<br /> and set the trend in my community.</em></p>\n\n<a href=\"https://[project site]/register/\"><img align=\"right\" src=\"http://prod.static.[project site]/images/theme/trendsetter_sticker.png?1289602783\"></a>\n<p><strong>What is an Energy Trendsetter?</strong><br />\nTrendsetters are people like you who are moving us towards a cleaner future by taking simple steps to save energy. Trendsetters take actions like installing efficient light bulbs, programming their thermostats and talking to their friends about eliminating energy waste. By doing their part, Trendsetters are setting an example for others in their community to follow.</p>\n\n<p><strong>Why take the pledge?</strong><br />\nThe Energy Trendsetter pledge is both a promise to yourself and to others. By taking the pledge, you’re publically demonstrating your commitment to being part of the clean energy solution.  The pledge connects you to a community of Trendsetters across the country who are all working to save energy. The pledge also serves as a reminder to continue your efforts to eliminate energy waste in your home and community. </p>\n\n<p><strong>What happens after I take the pledge?</strong><br />\nOnce you take the Trendsetter Pledge, you can use <a href=\"http://[project site]/actions\">[project name]’s resources</a> to find more ways to save energy in your own home, and help your friends turn their houses, schools and workplaces into models of clean, efficient living. <a href=\"http://[project site]/communities/\">Learn more about engaging your community</a>.</p>\n\n<p align=\"center\" style=\"font-size:17pt\"><strong><a href=\"https://[project site]/register/\">Take the Pledge Now</a></strong></p>',0,'',0),
	(12,'/comment-policy/','Comments Policy','<p>[project name] is powered by our members. The energy tips, pictures and organizing stories you share make [project name] a thriving community.</p>\n\n<p>We strive to keep the discussion here as open as possible. However, to keep this a fun, respectful place, we reserve the right to remove submissions that contain horrid language, personal attacks on other members, spam and other off-topic posts pushing products and services.</p>\n \n<p>For more information, see [project name]\'s <a href=\"http://[project site]/terms/\">Terms of Use</a>.</p>\n\n',0,'',0),
	(13,'/test/','test','<div style=\"float:left; width:300px\">\r\n<img src=\"http://rahstatic.s3.amazonaws.com/actionmedia/bat_med.png\">\r\n<div>\r\n<font size=\"2\">this would be the image caption this would be the image caption this would be the image caption</font>\r\n</div></div>\r\n<p>It’s that spooky time of year again! The wind is howling and that tapping on your window might actually be a witch on her broom. Yet the scariest supernatural creatures are not looming in the darkness of your backyard, but sitting in your home.\r\n\r\n\r\nVampires are hiding all over your house. No, these aren’t the blood-sucking kind. They’re worse — they’re the energy-hungry kind. Energy vampires use energy even when they’re turned “off.” These vampires use more energy when they are switched off than when they are on. They can even increase your electricity bill by 10%. So, what can you do to drive these vamps out of your home?\r\n\r\nWell, you may think that you need the help of Buffy, or even the keen senses of the Cullens, or rid your home of these vampires. But you can be your own slayer. Instead of picking up a wood stake, grab a smart power strip. These power strips will turn off the energy supply to your electronic devices when they aren’t in use. The vampires will then be starved of their precious energy and will leave your home for good.</p> ',0,'',0);

/*!40000 ALTER TABLE `django_flatpage` ENABLE KEYS */;
UNLOCK TABLES;





/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

