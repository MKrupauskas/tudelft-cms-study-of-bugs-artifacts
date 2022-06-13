import type { NextPage } from 'next';
import Head from 'next/head';
import { useEffect, useState } from 'react';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';

function useLocalState<T>(key: string, initial: T): [T, (value: T) => void] {
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

function proxy(url: string) {
  if (!url) {
    return '';
  }
  return url
    .replace('https://github.com', '/github')
    .replace('https://tickets.puppetlabs.com', 'jira');
}

const Home: NextPage = () => {
  const [data, setData] = useLocalState('data', '');
  const [index, setIndex] = useLocalState('index', 0);
  const [pages, setPages] = useState<{ bug: Window; fix: Window }[]>([]);
  const [categorizations, setCategorizations] = useState<any[]>([]);
  const bugs = data
    .split('\n')
    .filter((row) => row)
    .map((row) => row.split('\t'));
  const [issue, fix] = bugs[index] ?? [];
  const length = bugs.length || 1;

  function openPages() {
    closePages();
    const newPages = [...pages];
    newPages[index] = {
      bug: window.open(issue),
      fix: window.open(fix),
    };
    setPages(newPages);
  }

  function closePages() {
    const page = pages[index];
    if (!page) {
      return;
    }
    page.bug.close();
    page.fix.close();
    setPages(pages.map((p, i) => (index === i ? null : p)));
  }

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
      item['symptoms'],
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
                rows={5}
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
                (categorizations are lost on refresh)
              </Form.Label>
              <Form.Control
                as="textarea"
                rows={5}
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
              <div>
                <Button variant="success" onClick={openPages}>
                  Open pages
                </Button>
              </div>
              <div>
                <Button variant="danger" onClick={closePages}>
                  Close pages
                </Button>
              </div>
            </div>
          </Col>
        </Row>
        <Row>
          <Col md={2}>
            <Form.Group>
              <Form.Label>symptoms</Form.Label>
              <Form.Select
                value={getValue('symptoms')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'symptoms')
                }
              >
                <option value="">select option</option>
                <option value="URB">Unexpected Runtime Behavior</option>
                <option value="URBCIBE">Container Image Behavior Error</option>
                <option value="URBCDNP">
                  Configuration does not parse as expected
                </option>
                <option value="URBTM">Target misconfiguration</option>
                <option value="MR">Misleading Report</option>
                <option value="UDBE">
                  Unexpected Dependency Behavior Error
                </option>
                <option value="PI">Performance issue</option>
                <option value="C">Crash </option>
                <option value="CFNF">Feature/sub-feature non functional</option>
                <option value="CEC">Execution crash</option>
                <option value="CCP">Configuration parsing crash</option>
                <option value="CERE">Environment Related Error</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={2}>
            <Form.Group>
              <Form.Label>root causes</Form.Label>
              <Form.Select
                value={getValue('root causes')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'root causes')
                }
              >
                <option value="">select option</option>
                <option value="CILB">Container Image Life-cycle Bug</option>
                <option value="EHRB">Error Handler & Reporter Bugs</option>
                <option value="MC">Misconfiguration inside the codebase</option>
                <option value="MCDV">
                  Misconfiguration of default values inside the codebase
                </option>
                <option value="MCDP">
                  Misconfiguration of dependencies inside the codebase
                </option>
                <option value="TMO">Target machine operations</option>
                <option value="TMOFS">Incorrect filesystem operations</option>
                <option value="TMOD">
                  Target machine / remote host has dependency issues
                </option>
                <option value="TMOFTMF">
                  Fetch target machine variable/facts failure
                </option>
                <option value="TMOPI">Parsing issue target machine</option>
                <option value="TMOITE">
                  Instruction translation error / Abstraction layer error
                </option>
                <option value="CMO">Controller machine operations</option>
                <option value="CMOEP">Executor has problems</option>
                <option value="CMOCONP">Connection has problems</option>
                <option value="CMOPI">Parsing issue controller machine</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={2}>
            <Form.Group>
              <Form.Label>impact level</Form.Label>
              <Form.Select
                value={getValue('impact level')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'impact level')
                }
              >
                <option value="">select option</option>
                <option value="URB">URB</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={2}>
            <Form.Group>
              <Form.Label>impact consequences</Form.Label>
              <Form.Select
                value={getValue('impact consequences')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'impact consequences')
                }
              >
                <option value="">select option</option>
                <option value="URB">URB</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={2}>
            <Form.Group>
              <Form.Label>code fix</Form.Label>
              <Form.Select
                value={getValue('code fix')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'code fix')
                }
              >
                <option value="">select option</option>
                <option value="URB">URB</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={2}>
            <Form.Group>
              <Form.Label>conceptual fix</Form.Label>
              <Form.Select
                value={getValue('conceptual fix')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'conceptual fix')
                }
              >
                <option value="">select option</option>
                <option value="URB">URB</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={2}>
            <Form.Group>
              <Form.Label>system</Form.Label>
              <Form.Select
                value={getValue('system')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'system')
                }
              >
                <option value="">select option</option>
                <option value="URB">URB</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={2}>
            <Form.Group>
              <Form.Label>dependent</Form.Label>
              <Form.Select
                value={getValue('dependent')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'dependent')
                }
              >
                <option value="">select option</option>
                <option value="URB">URB</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={2}>
            <Form.Group>
              <Form.Label>trigger cause</Form.Label>
              <Form.Select
                value={getValue('trigger cause')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'trigger cause')
                }
              >
                <option value="">select option</option>
                <option value="URB">URB</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={2}>
            <Form.Group>
              <Form.Label>trigger reproduction</Form.Label>
              <Form.Select
                value={getValue('trigger reproduction')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'trigger reproduction')
                }
              >
                <option value="">select option</option>
                <option value="URB">URB</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={2}>
            <Form.Group>
              <Form.Label>notes</Form.Label>
              <Form.Control
                value={getValue('notes')}
                onChange={(event: any) => setValue(event.target.value, 'notes')}
              />
            </Form.Group>
          </Col>
        </Row>
        {/* exceedingly hard to display iframes these days https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors */}
        {/* <Row>
          <Col md={6}>
            <iframe
              className="w-100"
              style={{ height: '75vh' }}
              src={proxy(issue)}
            ></iframe>
          </Col>
          <Col md={6}>
            <iframe
              className="w-100"
              style={{ height: '75vh' }}
              src={proxy(fix)}
            ></iframe>
          </Col>
        </Row> */}
      </Container>
    </div>
  );
};

export default Home;
