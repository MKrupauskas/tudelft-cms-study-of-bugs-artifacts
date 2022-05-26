-- Create the database

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cse3000`
--
CREATE DATABASE IF NOT EXISTS `cse3000` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `cse3000`;

-- --------------------------------------------------------

--
-- Table structure for table `issue`
--

CREATE TABLE `issue` (
  `id` int(11) NOT NULL,
  `issue_id` int(11) NOT NULL,
  `title` text,
  `url` text,
  `created_at` varchar(100) NOT NULL,
  `number` int(11) NOT NULL,
  `body` text,
  `closed_at` varchar(100) DEFAULT NULL,
  `comments` int(11) DEFAULT NULL,
  `comments_url` text,
  `labels` text,
  `pull_request` text,
  `state` varchar(100) DEFAULT NULL,
  `commits` int(11) DEFAULT NULL,
  `additions` int(11) DEFAULT NULL,
  `deletions` int(11) DEFAULT NULL,
  `changed_files` int(11) DEFAULT NULL,
  `commits_data` text,
  `updated_at` varchar(100) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `pull_request`
--

CREATE TABLE `pull_request` (
  `id` int(11) NOT NULL,
  `pull_request_id` int(11) NOT NULL,
  `title` text,
  `url` text,
  `created_at` varchar(100) NOT NULL,
  `number` int(11) NOT NULL,
  `body` text,
  `closed_at` varchar(100) DEFAULT NULL,
  `comments` int(11) DEFAULT NULL,
  `comments_url` text,
  `labels` text,
  `pull_request` text,
  `state` varchar(100) DEFAULT NULL,
  `commits` int(11) DEFAULT NULL,
  `additions` int(11) DEFAULT NULL,
  `deletions` int(11) DEFAULT NULL,
  `changed_files` int(11) DEFAULT NULL,
  `commits_data` text,
  `updated_at` varchar(100) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `issue`
--
ALTER TABLE `issue`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `issue_id` (`issue_id`);

--
-- Indexes for table `pull_request`
--
ALTER TABLE `pull_request`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `issue_id` (`pull_request_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `issue`
--
ALTER TABLE `issue`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `pull_request`
--
ALTER TABLE `pull_request`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
