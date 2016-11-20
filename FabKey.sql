-- Database structure:

CREATE TABLE `keyList` (
  `keyValue` varchar(6) NOT NULL COMMENT 'The KEY, this format: [A-Z-0-9]{6}',
  `keyComment` varchar(255) NOT NULL COMMENT 'Comment on key, who have it.. Etc..',
  `keyType` varchar(127) NOT NULL COMMENT 'Key type: ! Admin, 1 One time use, @:HH-MN Hour check, %:DD-MM-YY Expiry'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Indexes for table `keyList`:
ALTER TABLE `keyList`
  ADD UNIQUE KEY `keyValue` (`keyValue`);
