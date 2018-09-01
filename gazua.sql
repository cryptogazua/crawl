CREATE TABLE `quote` (
  `currency` char(10) NOT NULL,
  `datetime` datetime NOT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  PRIMARY KEY (`currency`,`datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Steemit_MT` (
  `author` varchar(255) NOT NULL COMMENT 'AUTHOR',
  `permlink` varchar(255) NOT NULL COMMENT 'PERMLINK',
  `LAST_UPDATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'LAST_UPDATE',
  `keyword` varchar(255) NOT NULL,
  `ID` varchar(255) DEFAULT NULL COMMENT 'ID',
  `CATEGORY` text COMMENT 'CATEGORY',
  `TITLE` text COMMENT 'TITLE',
  `BODY` text COMMENT 'BODY',
  `CREATED` datetime DEFAULT NULL COMMENT 'CREATED',
  `NET_VOTES` decimal(10,0) DEFAULT NULL COMMENT 'NET_VOTES',
  PRIMARY KEY (`author`,`permlink`,`LAST_UPDATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Steemit_MT';
