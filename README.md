# Collection Process

## Fetching Data

### Installing perceval

python 3 and pip are a prerequisite.

```
pip install perceval
```

### Github Pull Requests

Get the secret personal access token from Github settings.

```
perceval github --category pull_request puppetlabs puppet --output github-pull-requests-full.json --api-token <SECRET> --sleep-for-rate
```

Around 500MB of data. To reduce this filter with the `--from-date '2022-04-01'` flag of `perceval`.

### Jira

```
perceval jira 'https://tickets.puppetlabs.com' --project PUP --output jira-issues-full.json
```

Around 1500MB of data. To reduce this filter with the `--from-date '2022-04-01'` flag of `perceval`.

## Data Processing

Having node 18>= installed is a prerequisite.

### Data Mapping and Filtering

Some parameters can be changed inside the script `map-filter.js`.

Only relevant data is filtered and mapped to the common bug schema.

Only Jira issues with the `Bug` type are kept.

```
node map-filter.js
```

### Data Joining

We must join Jira issues with the pull requests for the analysis step.

By convention pull requests which are related to a Jira issue must have the Jira issue number in the title. We use this convention to associate both issues and pull requests to each other.

```
node join.js
```

### Data Statistics

To get issue and pull request counts as well as other misc statistics run the stats script.

```
node stats.js
```

### Data Sampling

To get a random sample of issues to analyze run the sampling script and it will randomly select 100 issues.

```
node sample.js
```

### Data Inspection

```
jq -C . joined/issues-filtered.json | less -R

jq -C . joined/issues.json | less -R

jq -C . joined/pull-requests.json | less -R
```
