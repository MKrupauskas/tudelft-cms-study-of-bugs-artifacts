import fs from 'fs/promises'

let aggregated = {}

async function aggregate(iteration) {
	const content = await fs.readFile(`categorizations/iteration-${iteration}.tsv`)
	const rows = content.toString().split('\n').map(row => row.split('\t').map(value => value.trim()))
	const [header, ...data] = rows

	for (const key of header.slice(2)) {
		if (!aggregated[key]) {
			aggregated[key] = {}
		}
	}
	for (const item of data) {
		for (let i = 2; i < header.length; i++) {
			const key = header[i]
			const value = item[i]
			for (const subval of value.split(',')) {
				aggregated[key][subval] = (aggregated[key][subval] ?? 0) + 1
			}
		}
	}
}

await aggregate(1)
await aggregate(2)
await aggregate(3)
await aggregate(4)
await aggregate(5)

const filename = "aggregated-categorization.json"
console.log(`writing aggregations to ${filename}`)
fs.writeFile(filename, JSON.stringify(aggregated, null, 2))
