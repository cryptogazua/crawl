CREATE TABLE `quote` (
  `currency` char(10) NOT NULL,
  `datetime` datetime NOT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  PRIMARY KEY (`currency`,`datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
