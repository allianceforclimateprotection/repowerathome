ALTER TABLE messaging_message ADD send_as_batch TINYINT(1) AFTER recipient_function;

ALTER TABLE messaging_message ADD batch_window INT(1) AFTER send_as_batch;

ALTER TABLE messaging_message ADD time_snap TIME DEFAULT NULL AFTER batch_window;

ALTER TABLE messaging_message CHANGE delta_type message_timing VARCHAR(20);

ALTER TABLE messaging_message CHANGE delta_value x_value INT(10);

ALTER TABLE messaging_stream ADD label VARCHAR(50) AFTER slug;

ALTER TABLE messaging_stream ADD description VARCHAR(255) AFTER label;

ALTER TABLE messaging_stream ADD can_unsubscribe TINYINT(1) AFTER description;

ALTER TABLE messaging_recipientmessage CHANGE token token VARCHAR(40);

ALTER TABLE messaging_messagelink CHANGE token token VARCHAR(40);

-- Add a new column, to indicate whether or not a user would like to share their activity on twitter
ALTER TABLE rah_profile ADD twitter_share TINYINT(1) DEFAULT 0 AFTER twitter_access_token;

-- Add a new column, to indicate whether or not a user would like to share their activity on facebook
ALTER TABLE rah_profile ADD facebook_share TINYINT(1) DEFAULT 0 AFTER facebook_connect_only;

-- Add a new column, to indicate whether or not we should ask the user to share their activity stream
ALTER TABLE rah_profile ADD ask_to_share TINYINT(1) DEFAULT 1 AFTER facebook_share;

-- ALTER TABLE messaging_message ADD batch_function VARCHAR(100) AFTER send_as_batch;

ALTER TABLE messaging_queue ADD batch_content_type_id int(11) AFTER object_pk;

ALTER TABLE messaging_queue ADD batch_object_pk int(10) UNSIGNED AFTER batch_content_type_id;