-- --------------------------------------------------------

--
-- Table structure for table `bugs_fixes`
--

CREATE TABLE bugs_fixes
(
  `id` INT NOT NULL AUTO_INCREMENT,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `system` VARCHAR(50) NOT NULL DEFAULT 'moby',
  PRIMARY KEY (id)
)
SELECT
issue.`issue_id`,
pull_request.`pull_request_id`,
issue.`number`,
issue.`title`,
pull_request.`body`,
issue.`url` AS `issue_url`,
pull_request.`url` AS `pull_request_url`,
issue.`created_at`,
issue.`closed_at`,
issue.`updated_at`,
issue.`state`,
issue.`labels`,
pull_request.`comments`,
pull_request.`comments_url`,
pull_request.`commits`,
pull_request.`additions`,
pull_request.`deletions`,
pull_request.`changed_files`,
pull_request.`commits_data`
FROM issue INNER JOIN pull_request WHERE issue.number = pull_request.number AND issue.state = "closed" AND pull_request.state = "closed";
