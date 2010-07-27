ALTER TABLE messaging_message ADD send_as_batch TINYINT(1) AFTER recipient_function;

ALTER TABLE messaging_message ADD batch_window INT(1) AFTER send_as_batch;

ALTER TABLE messaging_message ADD time_snap TIME DEFAULT NULL AFTER batch_window;

ALTER TABLE messaging_message CHANGE delta_type message_timing VARCHAR(20);

ALTER TABLE messaging_message CHANGE delta_value x_value INT(10);

# Add UNIQUE CONSTRAINT and DB_INDEX to name field in messaging.message table

ALTER TABLE messaging_stream ADD label VARCHAR(50) AFTER slug;

ALTER TABLE messaging_stream ADD description VARCHAR(255) AFTER label;

ALTER TABLE messaging_stream ADD can_unsubscribe TINYINT(1) AFTER description;