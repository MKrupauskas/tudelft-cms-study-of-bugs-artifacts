import fs from 'fs';

// max mysql text field length
const MAX_TEXT_LENGTH = 65535

function escape(str) {
  if (!str) {
    return ''
  }

  const replaced = str.replaceAll("'", '"').replaceAll('\n', '\\n').replaceAll('\r', '\\r');


  if (replaced.length > MAX_TEXT_LENGTH) {
    return replaced.substring(0, MAX_TEXT_LENGTH)
  }

  return replaced
}

function parseNumber(number) {
  if (!number) {
    return 0
  }
  const parsed = parseInt(number)
  if (!parsed) {
    return 0
  }
  return parsed
}

function entry(issue) {
  return `('puppet', ${parseNumber(issue.issue_id)}, ${parseNumber(issue.pull_request.pull_request_id)}, ${parseNumber(issue.pull_request.number)}, '${escape(issue.title)}', '${escape(issue.body)}', '${escape(issue.url)}', '${escape(issue.pull_request.url)}', '${escape(issue.created_at)}', '${escape(issue.closed_at)}', '${escape(issue.updated_at)}', '${escape(issue.state)}', '${escape(issue.labels)}', ${parseNumber(issue.comments)}, '${parseNumber(issue.comments_url)}', ${parseNumber(issue.pull_request.commits)}, ${parseNumber(issue.pull_request.additions)}, ${parseNumber(issue.pull_request.deletions)}, ${parseNumber(issue.pull_request.changed_files)}, '${escape(issue.commit.commit)}', '${escape(issue.url)}', '${escape(issue.pull_request.url || `https://github.com/puppetlabs/puppet/commit/${issue.commit.commit}`)}'),
`
}

function readFile(file) {
  return new Promise((resolve, reject) => {
    fs.readFile(file, (err, data) => {
      console.log(`reading ${file}`)
      const list = JSON.parse(data)
      resolve(list)
    });
  })
}


const header =
  'INSERT INTO `bugs_fixes` (`system`, `issue_id`, `pull_request_id`, `number`, `title`, `body`, `issue_url`, `pull_request_url`, `created_at`, `closed_at`, `updated_at`, `state`, `labels`, `comments`, `comments_url`, `commits`, `additions`, `deletions`, `changed_files`, `commits_data`, `bug_report_url`, `bug_fix_url`) VALUES\n';
let insert = ''
let count = 0
let number = 0
const list = await readFile('joined/issues-filtered.json')

for (const issue of list) {
  if (!issue.pull_request) {
    issue.pull_request = {}
  }

  if (!issue.commit) {
    issue.commit = {}
  }

  if (count === 0) {
    insert += header
  }

  insert += entry(issue)
  count++;

  if (count === 500) {
    insert = insert.substring(0, insert.length - 2) + ';\n'
    fs.writeFile(`sql/insert-${number}.sql`, insert, () => { })
    insert = ''
    count = 0
    number++
  }
}

// replace last comma with a semicolon
insert = insert.substring(0, insert.length - 2) + ';\n'

fs.writeFile(`sql/insert-${number}.sql`, insert, () => { })


