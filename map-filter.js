import fs from 'fs';
import readline from 'readline';

const githubSampleFile = 'data/github-pull-requests-sample.json'
const githubFullFile = 'data/github-pull-requests-full-4.json'
const jiraSampleFile = 'data/jira-issues-sample.json'
const jiraFullFile = 'data/jira-issues-full-2.json'
const file = jiraFullFile;
const parse = parseJira;
const output = 'output/jira-full.json'
const rd = readline.createInterface({
  input: fs.createReadStream(file),
  console: false
});

let buffer = ""
let lastLine = ""
const list = []
let counter = 0

rd.on('line', function(line) {
  // see if the line is a new object
  if (line === '{' && lastLine === '}') {
    const obj = JSON.parse(buffer)
    const mapped = parse(obj)
    // do not push if parse returned null
    if (mapped) {
      list.push(mapped)
    }

    buffer = "{"
    return
  }

  buffer += line
  lastLine = line
});

function parseGithub(obj) {
  counter++
  console.log('parsing object ' + counter)
  return {
    pull_request_id: obj.data.id,
    title: obj.data.title,
    url: obj.data.html_url,
    created_at: obj.data.created_at,
    number: obj.data.number,
    body: obj.data.body,
    closed_at: obj.data.closed_at,
    comments: obj.data.comments,
    comments_url: obj.data.comments_url,
    labels: obj.data.labels.join(";"),
    pull_request: obj.data.patch_url,
    state: obj.data.state,
    commits: obj.data.commits,
    additions: obj.data.additions,
    deletions: obj.data.deletions,
    changed_files: obj.data.changed_files,
    commits_data: obj.data.commits_data.join(";"),
    updated_at: obj.data.updated_at,
    timestamp: obj.data.timestamp,
  }
}

function parseJira(obj) {
  if (obj.data.fields.issuetype.name !== 'Bug') {
    return null
  }
  counter++
  console.log('parsing object ' + counter)

  return {
    issue_id: obj.data.id,
    title: obj.data.fields.summary,
    url: `https://tickets.puppetlabs.com/browse/${obj.data.key}`,
    created_at: obj.data.fields.created,
    number: obj.data.key,
    body: obj.data.fields.description,
    closed_at: obj.data.fields.updated,
    comments: obj.data.comments_data.length,
    comments_url: `https://tickets.puppetlabs.com/browse/${obj.data.key}`,
    labels: obj.data.fields.labels.join(';'),
    state: obj.data.fields.status.name,
    // pull_request: null,
    // commits: null,
    // additions: null,
    // deletions: null,
    // changed_files: null,
    // commits_data: null,
    updated_at: obj.data.fields.updated,
    timestamp: obj.timestamp,
    // extension fields
    priority: obj.data.fields.priority.name,
    status_category: obj.data.fields.status.statusCategory.name,
  }
}

rd.on('close', function() {
  // clean out final buffer
  list.push(parse(JSON.parse(buffer)))
  console.log(list.length)
  fs.writeFile(output, JSON.stringify(list), () => {})
});
