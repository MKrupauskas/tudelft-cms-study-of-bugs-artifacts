import fs from 'fs';
import readline from 'readline';

function countTotalRaw(file) {
  return new Promise((resolve, reject) => {
    console.log(`reading ${file}`)
    const rd = readline.createInterface({
      input: fs.createReadStream(file),
      console: false
    });

    let lastLine = ''
    let counter = 0

    rd.on('line', function(line) {
      // see if the line is a new object
      if (line === '{' && lastLine === '}') {
        counter++
        return
      }

      lastLine = line
    });


    rd.on('close', function() {
      // account for the last object
      counter++
      resolve(counter)
    });
  });
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

async function countTotalFile(file) {
  const list = await readFile(file)
  return list.length
}

const totalRawIssues = await countTotalRaw('data/jira-issues-full-2.json')
const totalRawPRs = await countTotalRaw('data/github-pull-requests-full-4.json')
const totalMappedIssues = await countTotalFile('output/jira-full.json')
const totalMappedPRs = await countTotalFile('output/gh-full.json')
const totalJoinedIssues = await countTotalFile('joined/issues.json')
const totalJoinedPRs = await countTotalFile('joined/pull-requests.json')
const totalJoinedIssuesFiltered = await countTotalFile('joined/issues-filtered.json')

const prs = await readFile('joined/pull-requests.json')
const issueCount = {}

for (const pr of prs) {
  if (!issueCount[pr.issue_number]) {
    issueCount[pr.issue_number] = 0
  }

  issueCount[pr.issue_number]++
}

let totalIssuesWithMultiplePRs = 0
for (const count in Object.values(issueCount)) {
  if (count > 1) {
    totalIssuesWithMultiplePRs++
  }
}

const stats = {
  totalRawIssues,
  totalRawPRs,
  totalMappedIssues,
  totalMappedPRs,
  totalJoinedIssues,
  totalJoinedPRs,
  totalJoinedIssuesFiltered,
  totalIssuesWithMultiplePRs,
}
console.log(stats)
fs.writeFile('stats/stats.json', JSON.stringify(stats, null, 4), () => {})
