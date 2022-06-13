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
      item['system dependent'],
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
                <option value="Low">
                  System works overall besides in specific edge cases.
                </option>
                <option value="Medium">
                  System starts and works for the majority of cases but fails
                  when performing one important task.
                </option>
                <option value="High">
                  System won’t compile or start and it fails performing two or
                  more important tasks.
                </option>
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
                <option value="CNTOC">Container operation crash</option>
                <option value="SH">Security hazard</option>
                <option value="PD">Performance degradation</option>
                <option value="LOGRF">Logs reporting failure</option>
                <option value="TCF">Target configuration failed</option>
                <option value="TCFC">CMS operation crash</option>
                <option value="TCIA">Target configuration inaccurate</option>
                <option value="TCIN">Target configuration incomplete</option>
                <option value="CUX">Confusing user experience</option>
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
                <option value="CDDI">
                  Change on data declaration/initialization
                </option>
                <option value="CAS">Change on assignment statements</option>
                <option value="AC">Add class</option>
                <option value="RC">Remove class</option>
                <option value="CC">Change class</option>
                <option value="AM">Add method</option>
                <option value="RM">Remove method</option>
                <option value="CM">Change method</option>
                <option value="CLS">Change loop statements</option>
                <option value="CBS">Change branch statements</option>
                <option value="CRS">Change return statement</option>
                <option value="IM">Invoke a method</option>
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
                <option value="FEC">Fix execution component</option>
                <option value="FPC">Fix parser component</option>
                <option value="FCC">Fix connectivity component</option>
                <option value="EEF">Expand execution feature</option>
                <option value="EPF">Expand parser feature</option>
                <option value="ECF">Expand connectivity feature</option>
                <option value="CDEP">Change dependencies</option>
                <option value="CSS">Change system structure</option>
                <option value="CCONF">Change configuration</option>
                <option value="DDM">
                  Displaying a diagnostic message to the user
                </option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={2}>
            <Form.Group>
              <Form.Label>system dependent</Form.Label>
              <Form.Select
                value={getValue('system dependent')}
                onChange={(event: any) =>
                  setValue(event.target.value, 'system dependent')
                }
              >
                <option value="">select option</option>
                <option value="True">True</option>
                <option value="False">False</option>
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
                <option value="LE">Logic Errors</option>
                <option value="AE">Algorithmic Errors</option>
                <option value="CE">Configuration Errors</option>
                <option value="PE">Programming Errors</option>
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
                <option value="CLIC">CLI commands</option>
                <option value="CLICCC">Container command</option>
                <option value="CLICDMO">Dependency module operation</option>
                <option value="ENVS">Environment setup</option>
                <option value="FDEPU">Faulty Dependency Usage</option>
                <option value="OSSE">OS specific execution</option>
                <option value="TC">Test case</option>
                <option value="SI">Specific Invocation</option>
                <option value="SITMCE">Target machine control execution</option>
                <option value="SIIMI">Internal module invocation</option>
                <option value="SICMI">Custom module invocation</option>
                <option value="SITMRP">Target machine related parsing</option>
                <option value="SICRP">Config/Runbook Parsing</option>
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
