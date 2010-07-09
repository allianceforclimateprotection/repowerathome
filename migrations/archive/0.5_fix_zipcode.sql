-- This file was executed on the production database on July 9th, 2010

-- After updating the geo location codes in the produciton database with the 0.5 alpha release
-- (happening on July 1st, 2010) we noticed that the new geo location ids did not match up
-- with the old location ids.  This script is an attempt to fix the problem, by reseting all
-- users location id values if it hadn't changed since July 1st.

UPDATE rah_profile SET location_id=1624 WHERE user_id=99 AND location_id=1156;
UPDATE rah_profile SET location_id=1931 WHERE user_id=95 AND location_id=37007;
UPDATE rah_profile SET location_id=1959 WHERE user_id=71 AND location_id=32325;
UPDATE rah_profile SET location_id=2499 WHERE user_id=93 AND location_id=32875;
UPDATE rah_profile SET location_id=3511 WHERE user_id=94 AND location_id=33997;
UPDATE rah_profile SET location_id=4566 WHERE user_id=101 AND location_id=32952;
UPDATE rah_profile SET location_id=5956 WHERE user_id=46 AND location_id=17989;
UPDATE rah_profile SET location_id=6229 WHERE user_id=105 AND location_id=18104;
UPDATE rah_profile SET location_id=6372 WHERE user_id=70 AND location_id=1550;
UPDATE rah_profile SET location_id=6374 WHERE user_id=41 AND location_id=1552;
UPDATE rah_profile SET location_id=6374 WHERE user_id=43 AND location_id=1552;
UPDATE rah_profile SET location_id=6378 WHERE user_id=85 AND location_id=1556;
UPDATE rah_profile SET location_id=6379 WHERE user_id=25 AND location_id=1557;
UPDATE rah_profile SET location_id=6379 WHERE user_id=68 AND location_id=1557;
UPDATE rah_profile SET location_id=6380 WHERE user_id=5 AND location_id=1558;
UPDATE rah_profile SET location_id=6380 WHERE user_id=69 AND location_id=1558;
UPDATE rah_profile SET location_id=6382 WHERE user_id=104 AND location_id=1560;
UPDATE rah_profile SET location_id=10348 WHERE user_id=24 AND location_id=18663;
UPDATE rah_profile SET location_id=11308 WHERE user_id=13 AND location_id=19593;
UPDATE rah_profile SET location_id=16991 WHERE user_id=38 AND location_id=20929;
UPDATE rah_profile SET location_id=17185 WHERE user_id=89 AND location_id=7837;
UPDATE rah_profile SET location_id=17198 WHERE user_id=100 AND location_id=8026;
UPDATE rah_profile SET location_id=17209 WHERE user_id=91 AND location_id=7670;
UPDATE rah_profile SET location_id=17257 WHERE user_id=80 AND location_id=7793;
UPDATE rah_profile SET location_id=17258 WHERE user_id=84 AND location_id=8061;
UPDATE rah_profile SET location_id=17374 WHERE user_id=75 AND location_id=7891;
UPDATE rah_profile SET location_id=17490 WHERE user_id=98 AND location_id=8081;
UPDATE rah_profile SET location_id=17505 WHERE user_id=82 AND location_id=7905;
UPDATE rah_profile SET location_id=17511 WHERE user_id=59 AND location_id=8030;
UPDATE rah_profile SET location_id=17531 WHERE user_id=103 AND location_id=8177;
UPDATE rah_profile SET location_id=17725 WHERE user_id=73 AND location_id=7682;
UPDATE rah_profile SET location_id=17725 WHERE user_id=79 AND location_id=7682;
UPDATE rah_profile SET location_id=17732 WHERE user_id=83 AND location_id=7689;
UPDATE rah_profile SET location_id=17732 WHERE user_id=87 AND location_id=7689;
UPDATE rah_profile SET location_id=17739 WHERE user_id=72 AND location_id=7696;
UPDATE rah_profile SET location_id=17744 WHERE user_id=81 AND location_id=7701;
UPDATE rah_profile SET location_id=19096 WHERE user_id=78 AND location_id=22236;
UPDATE rah_profile SET location_id=19120 WHERE user_id=96 AND location_id=22152;
UPDATE rah_profile SET location_id=25331 WHERE user_id=77 AND location_id=25813;
UPDATE rah_profile SET location_id=25334 WHERE user_id=61 AND location_id=25434;
UPDATE rah_profile SET location_id=25786 WHERE user_id=88 AND location_id=25500;
UPDATE rah_profile SET location_id=27178 WHERE user_id=67 AND location_id=26350;
UPDATE rah_profile SET location_id=27751 WHERE user_id=74 AND location_id=27025;
UPDATE rah_profile SET location_id=27763 WHERE user_id=54 AND location_id=27037;
UPDATE rah_profile SET location_id=27768 WHERE user_id=47 AND location_id=27042;
UPDATE rah_profile SET location_id=29444 WHERE user_id=90 AND location_id=11086;
UPDATE rah_profile SET location_id=29826 WHERE user_id=102 AND location_id=28713;
UPDATE rah_profile SET location_id=32613 WHERE user_id=92 AND location_id=12234;
UPDATE rah_profile SET location_id=35930 WHERE user_id=86 AND location_id=13276;
UPDATE rah_profile SET location_id=38371 WHERE user_id=66 AND location_id=13899;
UPDATE rah_profile SET location_id=39125 WHERE user_id=50 AND location_id=15934;
UPDATE rah_profile SET location_id=39129 WHERE user_id=52 AND location_id=15938;
UPDATE rah_profile SET location_id=40933 WHERE user_id=97 AND location_id=39589;
UPDATE rah_profile SET location_id=41370 WHERE user_id=76 AND location_id=39176;