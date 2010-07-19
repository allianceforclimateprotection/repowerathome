-- Add a new column, to store the a user's facebook access token
ALTER TABLE rah_profile ADD facebook_access_token VARCHAR(255) AFTER twitter_access_token;

-- Add a new column, to indicate whether or not a user can login via facebook only
ALTER TABLE rah_profile ADD facebook_connect_only TINYINT(1) AFTER facebook_access_token;