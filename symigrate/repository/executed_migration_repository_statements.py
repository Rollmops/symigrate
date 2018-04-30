QUERY_FIND_MIGRATION_BY_SCOPE = \
    """
    SELECT version, description, timestamp, status, checksum, scope, script, filename
    FROM migration
    WHERE scope = ?
    ORDER BY version
    """

QUERY_FIND_ALL_MIGRATIONS = \
    """
    SELECT version, description, timestamp, status, checksum, scope, script, filename
    FROM migration
    ORDER BY version
    """

QUERY_INSERT_MIGRATION = \
    """
    INSERT INTO migration
    (version, description, timestamp, status, checksum, scope, script, filename)
    VALUES
    (?, ?, ?, ?, ?, ?, ?, ?)
    """

DDL_CREATE_MIGRATION_TABLE = \
    """
    CREATE TABLE migration 
    (
        version TEXT, 
        description TEXT, 
        timestamp TEXT, 
        status TEXT,
        checksum TEXT, 
        scope TEXT, 
        script TEXT, 
        filename TEXT
    )
    """

QUERY_FIND_MIGRATION_TABLE = "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='migration'"
