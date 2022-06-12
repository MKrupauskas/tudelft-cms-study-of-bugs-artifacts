import type { NextPage } from 'next';
import Head from 'next/head';
import { useEffect, useState } from 'react';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';

function useLocalState<T>(key: string, initial: T) {
  const [state, setState] = useState<T>(initial);

  useEffect(() => {
    const local = localStorage.getItem(key);
    if (local) {
      setState(JSON.parse(local));
    }
  }, []);

  function update(value) {
    setState(value);
    localStorage.setItem(key, JSON.stringify(value));
  }

  return [state, update];
}

const Home: NextPage = () => {
  const [data, setData] = useLocalState('data', '');
  const [index, setIndex] = useLocalState('index', 0);
  const [categorizations, setCategorizations] = useLocalState<any[]>(
    'categorizations',
    [],
  );
  const bugs = data
    .split('\n')
    .filter((row) => row)
    .map((row) => row.split('\t'));
  const [issue, fix] = bugs[index] ?? [];
  const length = bugs.length || 1;

  function getValue(key: string) {
    if (!categorizations[index]) {
      return '';
    }
    return categorizations[index][key];
  }

  function setValue(value: string, key: string) {
    const updated = [...categorizations];
    updated[index] = { ...(updated[index] ?? {}), [key]: value };
    setCategorizations(updated);
  }

  function getOutput(index: number) {
    const item = categorizations[index] ?? {};
    return [
      item['root causes'],
      item['impact level'],
      item['impact consequences'],
      item['code fix'],
      item['conceptual fix'],
      item['system'],
      item['dependent'],
      item['trigger cause'],
      item['trigger reproduction'],
      item['notes'],
    ];
  }

  useEffect(() => {
    window.onbeforeunload = () => {
      return 'Are you sure you want to leave?';
    };
  }, []);

  return (
    <div>
      <Head>
        <title>study of bugs analyzer</title>
        <meta
          name="description"
          content="A study of bugs in configuration management systems analyzer."
        />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container fluid>
        <Row>
          <Col md={6}>
            <Form.Group>
              <Form.Label>
                Input (.tsv) (schema: issue url, fix url) <br />
                parsed bugs: {bugs.length}
              </Form.Label>
              <Form.Control
                as="textarea"
                value={data}
                onChange={(event: any) => setData(event.target.value)}
              />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group>
              <Form.Label>
                Output (.tsv) (schema: issue, fix symptoms, root causes, impact
                level, impact consequences, code fix, conceptual fix, system
                dependent, trigger cause, trigger reproduction, notes)
              </Form.Label>
              <Form.Control
                as="textarea"
                value={bugs
                  .map((bug, index) => [...bug, ...getOutput(index)].join('\t'))
                  .join('\n')}
              />
            </Form.Group>
          </Col>
        </Row>
        <Row>
          <Col>
            <div>Selected bug index</div>
            <div className="d-flex align-items-center gap-1">
              <div>
                <Button onClick={() => setIndex((index - 1 + length) % length)}>
                  Previous
                </Button>
              </div>
              <Form.Group>
                <Form.Control
                  type="number"
                  value={index}
                  onChange={(event: any) => setIndex(event.target.value)}
                />
              </Form.Group>
              <div>
                <Button onClick={() => setIndex((index + 1) % length)}>
                  Next
                </Button>
              </div>
            </div>
          </Col>
        </Row>
        <Row>
          <Col>
            <Form.Group>
              <Form.Label>root causes</Form.Label>
              <Form.Control
                value={getValue('root causes')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'root causes')
                }
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group>
              <Form.Label>impact level</Form.Label>
              <Form.Control
                value={getValue('impact level')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'impact level')
                }
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group>
              <Form.Label>impact consequences</Form.Label>
              <Form.Control
                value={getValue('impact consequences')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'impact consequences')
                }
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group>
              <Form.Label>code fix</Form.Label>
              <Form.Control
                value={getValue('code fix')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'code fix')
                }
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group>
              <Form.Label>conceptual fix</Form.Label>
              <Form.Control
                value={getValue('conceptual fix')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'conceptual fix')
                }
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group>
              <Form.Label>system</Form.Label>
              <Form.Control
                value={getValue('system')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'system')
                }
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group>
              <Form.Label>dependent</Form.Label>
              <Form.Control
                value={getValue('dependent')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'dependent')
                }
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group>
              <Form.Label>trigger cause</Form.Label>
              <Form.Control
                value={getValue('trigger cause')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'trigger cause')
                }
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group>
              <Form.Label>trigger reproduction</Form.Label>
              <Form.Control
                value={getValue('trigger reproduction')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'trigger reproduction')
                }
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group>
              <Form.Label>notes</Form.Label>
              <Form.Control
                value={getValue('notes')}
                onChange={(event: any) => setValue(event.target.value, 'notes')}
              />
            </Form.Group>
          </Col>
        </Row>
        <Row>
          <Col md={6}>
            <iframe className="w-100" src={issue}></iframe>
          </Col>
          <Col md={6}>
            <iframe className="w-100" src={fix}></iframe>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Home;
