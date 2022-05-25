-- Remove:
-- False positives with no files changes.
-- Entries without descriptions as they won’t offer much information for our analysis to be performed properly.
-- Entries without labels as they won’t offer much information for our analysis to be performed properly.

DELETE FROM `bugs_fixes` WHERE changed_files = 0 OR body = "" OR labels = "";
