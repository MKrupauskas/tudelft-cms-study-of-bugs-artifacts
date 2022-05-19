import fs from 'fs/promises';

const data = await fs.readFile('joined/issues-filtered.json');
const issues = JSON.parse(data)

const sampleSize = 100
const sample = []

for (let i = 0; i < sampleSize; i++) {
  const index = Math.floor(Math.random() * issues.length)
  sample.push(issues[index])
}

console.log(sample)
await fs.writeFile(`sample/sample-${new Date().toISOString()}.json`, JSON.stringify(sample, null, 2))
