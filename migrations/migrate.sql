-- Add a new column, to store the a user's facebook access token
ALTER TABLE rah_profile ADD facebook_access_token VARCHAR(255) AFTER twitter_access_token;