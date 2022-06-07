
CREATE TABLE `bugs_fixes` (
  `id` int(11) NOT NULL,
  `system` varchar(100) NOT NULL DEFAULT 'moby',
  `issue_id` int(11) NOT NULL,
  `pull_request_id` int(11) NOT NULL,
  `number` int(11) NOT NULL,
  `title` text,
  `body` text,
  `issue_url` text,
  `pull_request_url` text,
  `created_at` varchar(100) NOT NULL,
  `closed_at` varchar(100) DEFAULT NULL,
  `updated_at` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `labels` text,
  `comments` int(11) DEFAULT NULL,
  `comments_url` text,
  `commits` int(11) DEFAULT NULL,
  `additions` int(11) DEFAULT NULL,
  `deletions` int(11) DEFAULT NULL,
  `changed_files` int(11) DEFAULT NULL,
  `commits_data` text,
  `bug_report_url` varchar(250) DEFAULT NULL,
  `bug_fix_url` varchar(250) DEFAULT NULL,
  `symptoms` varchar(50) DEFAULT NULL,
  `root_causes` varchar(50) DEFAULT NULL,
  `impact` varchar(50) DEFAULT NULL,
  `consequences` varchar(50) DEFAULT NULL,
  `fixes` varchar(50) DEFAULT NULL,
  `system_dependent` varchar(50) DEFAULT NULL,
  `triggers` varchar(50) DEFAULT NULL,
  `characteristics` varchar(50) DEFAULT NULL,
  `notes` text
);

ALTER TABLE `bugs_fixes` ADD PRIMARY KEY (`id`);

ALTER TABLE `bugs_fixes` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2400;
