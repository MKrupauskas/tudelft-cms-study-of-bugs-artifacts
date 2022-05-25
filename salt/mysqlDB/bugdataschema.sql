SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `cse3000saltbugdb` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `cse3000saltbugdb`;

-- issue_id will be the id field in the issue JSON returned by github
-- url is html url
CREATE TABLE `salt_issue` (
  `id` int(11) NOT NULL,
  `issue_id` int(11) NOT NULL,
  `title` text,
  `url` text,
  `created_at` varchar(100) NOT NULL,
  `number` int(11) NOT NULL,
  `closed_at` varchar(100) DEFAULT NULL,
  `comments` int(11) DEFAULT NULL,
  `comments_url` text,
  `labels` text,
  `state` varchar(100) DEFAULT NULL,
  `updated_at` varchar(100) DEFAULT NULL,
  `CMS` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for table `issue`
--
ALTER TABLE `salt_issue`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `issue_id` (`issue_id`);
  
--
ALTER TABLE `salt_issue`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--

CREATE TABLE `salt_pr` (
  `id` int(11) NOT NULL,
  `pull_request_id` int(11) NOT NULL, -- id
  `attempts_to_fix_issue_number` int(11) NOT NULL, -- move to last column
  `title` text, -- "title"
  `url` text, -- html url
  `created_at` varchar(100) NOT NULL,
  `number` int(11) NOT NULL,
  `closed_at` varchar(100) DEFAULT NULL,
  `merged_at` varchar(100) DEFAULT NULL,
  `merge_commit_sha` text,
  `comments` int(11) DEFAULT NULL,
  `comments_url` text,
  `labels` text,
  `state` varchar(100) DEFAULT NULL,
  `commits` int(11) DEFAULT NULL,
  `additions` int(11) DEFAULT NULL,
  `deletions` int(11) DEFAULT NULL,
  `changed_files` int(11) DEFAULT NULL,
  `commits_data` text,
  `updated_at` varchar(100) DEFAULT NULL,
  `CMS` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for table `pull_request`
--
ALTER TABLE `salt_pr`
  ADD PRIMARY KEY (`id`);
  -- ADD UNIQUE KEY `pull_request_id` (`pull_request_id`);

--
-- AUTO_INCREMENT for table `pull_request`
--
ALTER TABLE `salt_pr`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

CREATE TABLE `salt_commit` (
  `id` int(11) NOT NULL,
  `attempts_to_fix_issue_number` int(11) NOT NULL,
  `url` text,
  `commit_id_used_to_get_JSON` text,
  `CMS` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `salt_commit`
  ADD PRIMARY KEY (`id`);
  
--
ALTER TABLE `salt_commit`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
