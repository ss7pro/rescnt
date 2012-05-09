
CREATE TABLE resources (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    parent  BIGINT UNSIGNED,
    type VARCHAR(255) NOT NULL,
    value VARCHAR(255) NOT NULL,
    zone VARCHAR(255) NOT NULL,
    added TIMESTAMP,
    INDEX (type,value,zone),
    INDEX (type,parent)
) ENGINE=INNODB;


CREATE TABLE counters (
    resource BIGINT UNSIGNED NOT NULL,
    type VARCHAR(255) NOT NULL,
    value BIGINT UNSIGNED,
    delta BIGINT UNSIGNED,
    added DATETIME NOT NULL,
    prev DATETIME,
    INDEX (resource,type,added),
    INDEX (resource,type),
    FOREIGN KEY (resource) REFERENCES resources(id) ON DELETE RESTRICT
) ENGINE=INNODB;
