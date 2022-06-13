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
  const [page, setPage] = useState<{ bug: Window; fix: Window }>(null);
  const [categorizations, setCategorizations] = useState<any[]>([]);
  const bugs = data
    .split('\n')
    .filter((row) => row)
    .map((row) => row.split('\t'));
  const [issue, fix] = bugs[index] ?? [];
  const length = bugs.length || 1;

  function openPages() {
    closePages();
    setPage({
      bug: window.open(issue),
      fix: window.open(fix),
    });
  }

  function closePages() {
    if (!page) {
      return;
    }
    page.bug.close();
    page.fix.close();
    setPage(null);
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
                <option value="URB">(URB) Unexpected Runtime Behavior</option>
                <option value="URBCIBE">
                  (URBCIBE) Container Image Behavior Error
                </option>
                <option value="URBCDNP">
                  (URBCDNP) Configuration does not parse as expected
                </option>
                <option value="URBTM">(URBTM) Target misconfiguration</option>
                <option value="MR">(MR) Misleading Report</option>
                <option value="UDBE">
                  (UDBE) Unexpected Dependency Behavior Error
                </option>
                <option value="PI">(PI) Performance issue</option>
                <option value="C">(C) Crash </option>
                <option value="CFNF">
                  (CFNF) Feature/sub-feature non functional
                </option>
                <option value="CEC">(CEC) Execution crash</option>
                <option value="CCP">(CCP) Configuration parsing crash</option>
                <option value="CERE">(CERE) Environment Related Error</option>
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
                <option value="CILB">
                  (CILB) Container Image Life-cycle Bug
                </option>
                <option value="EHRB">
                  (EHRB) Error Handler & Reporter Bugs
                </option>
                <option value="MC">
                  (MC) Misconfiguration inside the codebase
                </option>
                <option value="MCDV">
                  (MCDV) Misconfiguration of default values inside the codebase
                </option>
                <option value="MCDP">
                  (MCDP) Misconfiguration of dependencies inside the codebase
                </option>
                <option value="TMO">(TMO) Target machine operations</option>
                <option value="TMOFS">
                  (TMOFS) Incorrect filesystem operations
                </option>
                <option value="TMOD">
                  (TMOD) Target machine / remote host has dependency issues
                </option>
                <option value="TMOFTMF">
                  (TMOFTMF) Fetch target machine variable/facts failure
                </option>
                <option value="TMOPI">
                  (TMOPI) Parsing issue target machine
                </option>
                <option value="TMOITE">
                  (TMOITE) Instruction translation error / Abstraction layer
                  error
                </option>
                <option value="CMO">(CMO) Controller machine operations</option>
                <option value="CMOEP">(CMOEP) Executor has problems</option>
                <option value="CMOCONP">
                  (CMOCONP) Connection has problems
                </option>
                <option value="CMOPI">
                  (CMOPI) Parsing issue controller machine
                </option>
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
                  (Low) System works overall besides in specific edge cases.
                </option>
                <option value="Medium">
                  (Medium) System starts and works for the majority of cases but
                  fails when performing one important task.
                </option>
                <option value="High">
                  (High) System won’t compile or start and it fails performing
                  two or more important tasks.
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
                <option value="CNTOC">(CNTOC) Container operation crash</option>
                <option value="SH">(SH) Security hazard</option>
                <option value="PD">(PD) Performance degradation</option>
                <option value="LOGRF">(LOGRF) Logs reporting failure</option>
                <option value="TCF">(TCF) Target configuration failed</option>
                <option value="TCFC">(TCFC) CMS operation crash</option>
                <option value="TCIA">
                  (TCIA) Target configuration inaccurate
                </option>
                <option value="TCIN">
                  (TCIN) Target configuration incomplete
                </option>
                <option value="CUX">(CUX) Confusing user experience</option>
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
                  (CDDI) Change on data declaration/initialization
                </option>
                <option value="CAS">
                  (CAS) Change on assignment statements
                </option>
                <option value="AC">(AC) Add class</option>
                <option value="RC">(RC) Remove class</option>
                <option value="CC">(CC) Change class</option>
                <option value="AM">(AM) Add method</option>
                <option value="RM">(RM) Remove method</option>
                <option value="CM">(CM) Change method</option>
                <option value="CLS">(CLS) Change loop statements</option>
                <option value="CBS">(CBS) Change branch statements</option>
                <option value="CRS">(CRS) Change return statement</option>
                <option value="IM">(IM) Invoke a method</option>
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
                <option value="FEC">(FEC) Fix execution component</option>
                <option value="FPC">(FPC) Fix parser component</option>
                <option value="FCC">(FCC) Fix connectivity component</option>
                <option value="EEF">(EEF) Expand execution feature</option>
                <option value="EPF">(EPF) Expand parser feature</option>
                <option value="ECF">(ECF) Expand connectivity feature</option>
                <option value="CDEP">(CDEP) Change dependencies</option>
                <option value="CSS">(CSS) Change system structure</option>
                <option value="CCONF">(CCONF) Change configuration</option>
                <option value="DDM">
                  (DDM) Displaying a diagnostic message to the user
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
                <option value="True">(True) True</option>
                <option value="False">(False) False</option>
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
                <option value="LE">(LE) Logic Errors</option>
                <option value="AE">(AE) Algorithmic Errors</option>
                <option value="CE">(CE) Configuration Errors</option>
                <option value="PE">(PE) Programming Errors</option>
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
                <option value="CLIC">(CLIC) CLI commands</option>
                <option value="CLICCC">(CLICCC) Container command</option>
                <option value="CLICDMO">
                  (CLICDMO) Dependency module operation
                </option>
                <option value="ENVS">(ENVS) Environment setup</option>
                <option value="FDEPU">(FDEPU) Faulty Dependency Usage</option>
                <option value="OSSE">(OSSE) OS specific execution</option>
                <option value="TC">(TC) Test case</option>
                <option value="SI">(SI) Specific Invocation</option>
                <option value="SITMCE">
                  (SITMCE) Target machine control execution
                </option>
                <option value="SIIMI">
                  (SIIMI) Internal module invocation
                </option>
                <option value="SICMI">(SICMI) Custom module invocation</option>
                <option value="SITMRP">
                  (SITMRP) Target machine related parsing
                </option>
                <option value="SICRP">(SICRP) Config/Runbook Parsing</option>
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
        <Row>
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
        </Row>
      </Container>
    </div>
  );
};

export default Home;
