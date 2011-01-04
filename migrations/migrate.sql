INSERT INTO commitments_contributor (first_name, last_name, email, location_id, user_id, created, updated)
SELECT u.first_name, u.last_name, u.email, p.location_id, u.id, NOW(), NOW()
FROM auth_user u
LEFT JOIN rah_profile p ON u.id = p.user_id
LEFT JOIN commitments_contributor c ON u.id = c.user_id
WHERE c.id IS NULL
