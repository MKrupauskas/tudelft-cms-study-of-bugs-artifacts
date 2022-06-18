import fs from 'fs/promises'

let interpolated = { symptomsByRootCauses: {}, impactLevelByImpactConsequence: {}, codeFixByConceptualFix: {} }

async function interpolate(iteration) {
	const content = await fs.readFile(`categorizations/iteration-${iteration}.tsv`)
	const rows = content.toString().split('\n').map(row => row.split('\t').map(value => value.trim()))
	const [header, ...data] = rows
	const symptomsIndex = header.indexOf('symptoms')
	const rootCausesIndex = header.indexOf('root causes')
	const impactLevelIndex = header.indexOf('impact level')
	const impactConsequencesIndex = header.indexOf('impact consequences')
	const codeFixIndex = header.indexOf('code fix')
	const conceptualFixIndex = header.indexOf('conceptual fix')

	for (const item of data) {
		const symptom = item[symptomsIndex]
		const rootCause = item[rootCausesIndex]

		if (!interpolated.symptomsByRootCauses[symptom]) {
			interpolated.symptomsByRootCauses[symptom] = {}
		}

		interpolated.symptomsByRootCauses[symptom][rootCause] = (interpolated.symptomsByRootCauses[symptom][rootCause] ?? 0) + 1

		const impactLevel = item[impactLevelIndex]
		const impactConsequence = item[impactConsequencesIndex]

		if (!interpolated.impactLevelByImpactConsequence[impactLevel]) {
			interpolated.impactLevelByImpactConsequence[impactLevel] = {}
		}

		interpolated.impactLevelByImpactConsequence[impactLevel][impactConsequence] = (interpolated.impactLevelByImpactConsequence[impactLevel][impactConsequence] ?? 0) + 1

		const codeFix = item[codeFixIndex]
		const conceptualFix = item[conceptualFixIndex]

		if (!interpolated.codeFixByConceptualFix[codeFix]) {
			interpolated.codeFixByConceptualFix[codeFix] = {}
		}

		interpolated.codeFixByConceptualFix[codeFix][conceptualFix] = (interpolated.codeFixByConceptualFix[codeFix][conceptualFix] ?? 0) + 1
	}
}

await interpolate(1)
await interpolate(2)
await interpolate(3)
await interpolate(4)
await interpolate(5)

const filename = "interpolated.json"
console.log(`writing aggregations to ${filename}`)
fs.writeFile(filename, JSON.stringify(interpolated, null, 2))
