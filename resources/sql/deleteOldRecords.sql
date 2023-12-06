delete FROM backups WHERE base = '_base' AND path NOT in (
    SELECT path FROM backups WHERE base = '_base'
    ORDER BY backupdate desc limit _retention)
RETURNING *;