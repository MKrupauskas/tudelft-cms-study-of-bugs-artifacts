import fs from 'fs/promises';

const ghData = await fs.readFile('output/gh-full.json');
const pullRequests = JSON.parse(ghData)

const jiraData = await fs.readFile('output/jira-full.json');
const issues = JSON.parse(jiraData)
let counter = 0;
for (let issue of issues) {
  if (!issue) {
    continue
  }

  for (let pullRequest of pullRequests) {
    if (!pullRequest.title.includes(issue.number)) {
      continue
    }

    counter++
    console.log(`Issue ${issue.number} and PR #${pullRequest.number} (title: "${pullRequest.title}") are associated (count: ${counter})`)

    issue.pull_request = pullRequest.number
    pullRequest.issue_number = issue.number
  }
}

// the bug report in jira is the source of truth for the bug
await fs.writeFile('joined/issues.json', JSON.stringify(issues))
// filter out all pull requests which have no issue associated with them
await fs.writeFile('joined/pull-requests.json', JSON.stringify(pullRequests.filter(pr => pr.issue_number)))
// see how many issues have a pr attached. Are we interested in bugs with no PRs?
await fs.writeFile('joined/issues-filtered.json', JSON.stringify(issues.filter(issue => issue && issue.pull_request)))
