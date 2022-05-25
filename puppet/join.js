import fs from 'fs/promises';

const ghData = await fs.readFile('output/gh-full.json');
const pullRequests = JSON.parse(ghData)

const jiraData = await fs.readFile('output/jira-full.json');
const issues = JSON.parse(jiraData)

const commitData = await fs.readFile('commits.json');
const commits = JSON.parse(commitData)
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

  for (const commit of commits) {
    if (!commit.message.includes(issue.number)) {
      continue
    }

    counter++
    console.log(`Issue ${issue.number} and commit ${commit.commit} are associated (count: ${counter})`)

    issue.commit = commit.commit
  }
}

// the bug report in jira is the source of truth for the bug
await fs.writeFile('joined/issues.json', JSON.stringify(issues))
// filter out all pull requests which have no issue associated with them
await fs.writeFile('joined/pull-requests.json', JSON.stringify(pullRequests.filter(pr => pr.issue_number)))
// see how many issues have a pr attached.
await fs.writeFile('joined/issues-with-prs.json', JSON.stringify(issues.filter(issue => issue && issue.pull_request)))
// see how many issues have a pr or commit attached. We are only interested in bugs with fixes.
await fs.writeFile('joined/issues-filtered.json', JSON.stringify(issues.filter(issue => issue && (issue.pull_request || issue.commit))))
