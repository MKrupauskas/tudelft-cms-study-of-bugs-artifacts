import fs from 'fs/promises'

const filename = 'aggregated-categorization-mattia.json'
const data = await fs.readFile(filename)

const counts = JSON.parse(data.toString())
const [name] = filename.split('.')

for (const [param, values] of Object.entries(counts)) {
	const rows = [`${param},count`]
	for (const [key, value] of Object.entries(values)) {
		rows.push(`${key},${value}`)
	}
	await fs.mkdir(`plots/${name}`, { recursive: true })
	await fs.writeFile(`plots/${name}/${param.replace(' ', '-')}.csv`, rows.join('\n'))
}