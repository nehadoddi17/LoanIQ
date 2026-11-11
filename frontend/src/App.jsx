
import { useEffect, useState } from 'react'
import axios from 'axios'
import {
  LayoutDashboard, Users, FileText, ShieldAlert,
  RefreshCw, CheckCircle, Clock, XCircle,
  Activity, Wallet, Search
} from 'lucide-react'
import {
  ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend
} from 'recharts'

const API = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

const navigation = [
  { name: 'Overview', icon: LayoutDashboard },
  { name: 'Applicants', icon: Users },
  { name: 'Loan Applications', icon: FileText },
  { name: 'Risk Intelligence', icon: ShieldAlert },
]

function getRows(response) {
  const data = response?.data
  if (Array.isArray(data)) return data
  if (Array.isArray(data?.items)) return data.items
  if (Array.isArray(data?.results)) return data.results
  return []
}

function App() {
  const [page, setPage] = useState('Overview')
  const [applicants, setApplicants] = useState([])
  const [applications, setApplications] = useState([])
  const [anomalies, setAnomalies] = useState([])
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [scanning, setScanning] = useState(false)
  const [error, setError] = useState('')
  const [search, setSearch] = useState('')

  async function loadDashboard() {
    setLoading(true)
    setError('')
    try {
      const results = await Promise.allSettled([
        axios.get(`${API}/api/applicants/`),
        axios.get(`${API}/api/applications/`),,
        axios.get(`${API}/api/anomalies/`),
        axios.get(`${API}/api/anomaly-evaluation/metrics`)
      ])
      console.log("APPLICANTS API:", results[0])
      console.log("APPLICATIONS API:", results[1])
      console.log("ANOMALIES API:", results[2])
      console.log("METRICS API:", results[3])

      if (results[0].status === 'fulfilled') setApplicants(getRows(results[0].value))
      if (results[1].status === 'fulfilled') setApplications(getRows(results[1].value))
      if (results[2].status === 'fulfilled') setAnomalies(getRows(results[2].value))
      if (results[3].status === 'fulfilled') setMetrics(results[3].value.data)

      if (results.every(r => r.status === 'rejected')) {
        setError('Cannot connect to the LoanIQ API. Make sure the FastAPI server is running.')
      }
    } catch {
      setError('Unable to load dashboard data.')
    } finally {
      setLoading(false)
    }
  }

  async function runScan() {
    setScanning(true)
    try {
      await axios.post(`${API}/api/anomalies/scan`)
      await loadDashboard()
    } catch {
      setError('Anomaly scan failed. Check the backend API.')
    } finally {
      setScanning(false)
    }
  }

  useEffect(() => {
    loadDashboard()
  }, [])

  const approved = applications.filter(a => a.application_status === 'APPROVED').length
  const pending = applications.filter(a => a.application_status === 'PENDING').length
  const rejected = applications.filter(a => a.application_status === 'REJECTED').length

  const chartData = [
    { name: 'Approved', value: approved, color: '#16a36a' },
    { name: 'Pending', value: pending, color: '#e9a23b' },
    { name: 'Rejected', value: rejected, color: '#e15b64' },
  ].filter(x => x.value > 0)


const filteredApplicants = applicants.filter(a =>
  `${a.first_name || ''} ${a.last_name || ''} ${a.applicant_id || ''} ${a.email || ''}`
    .toLowerCase().includes(search.toLowerCase())
)

const filteredApplications = applications.filter(a =>
  `${a.application_id || ''} ${a.applicant_id || ''} ${a.application_status || a.status || ''}`
    .toLowerCase().includes(search.toLowerCase())
)

  const money = value => value == null ? '—' :
    new Intl.NumberFormat('en-IN', {
      style: 'currency', currency: 'INR', maximumFractionDigits: 0
    }).format(value)

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">L</div>
          <div>
            <h2>LoanIQ</h2>
            <span>INTELLIGENT LENDING</span>
          </div>
        </div>

        <div className="nav-label">WORKSPACE</div>
        <nav>
          {navigation.map(item => {
            const Icon = item.icon
            return (
              <button
                key={item.name}
                className={`nav-item ${page === item.name ? 'active' : ''}`}
                onClick={() => { setPage(item.name); setSearch('') }}
              >
                <Icon size={18} />
                {item.name}
              </button>
            )
          })}
        </nav>

        <div className="sidebar-bottom">
          <div className="system-status">
            <span className="status-dot" />
            LoanIQ System
            <small>Monitoring enabled</small>
          </div>
          <div className="user-profile">
            <div className="avatar">AD</div>
            <div><strong>Administrator</strong><small>Loan Operations</small></div>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <div className="breadcrumb">LoanIQ / {page}</div>
            <h1>{page}</h1>
          </div>
          <div className="top-actions">
            <span className="live-label"><span className="status-dot" /> LIVE SYSTEM</span>
            <button className="icon-button" onClick={loadDashboard} title="Refresh">
              <RefreshCw size={17} />
            </button>
          </div>
        </header>

        <section className="page-content">
          {error && <div className="error-banner">{error}</div>}

          {page === 'Overview' && (
            <>
              <div className="welcome-row">
                <div>
                  <h2>Good day, Administrator</h2>
                  <p>Here's what's happening across your lending operations.</p>
                </div>
                <button className="primary-button" onClick={runScan} disabled={scanning}>
                  <Activity size={16} />
                  {scanning ? 'Scanning...' : 'Run Anomaly Scan'}
                </button>
              </div>

              <div className="stats-grid">
                <Stat icon={Users} label="Total Applicants" value={applicants.length.toLocaleString('en-IN')} color="blue" />
                <Stat icon={FileText} label="Loan Applications" value={applications.length.toLocaleString('en-IN')} color="purple" />
                <Stat icon={CheckCircle} label="Approved Loans" value={approved.toLocaleString('en-IN')} color="green" />
                <Stat icon={ShieldAlert} label="Detected Anomalies" value={anomalies.length.toLocaleString('en-IN')} color="orange" />
              </div>

              <div className="content-grid">
                <div className="panel">
                  <div className="panel-heading">
                    <div><h3>Application Overview</h3><p>Distribution by decision status</p></div>
                  </div>
                  {chartData.length ? (
                    <div className="chart-area">
                      <ResponsiveContainer width="100%" height={250}>
                        <PieChart>
                          <Pie data={chartData} dataKey="value" nameKey="name"
                            cx="50%" cy="50%" innerRadius={65} outerRadius={95} paddingAngle={4}>
                            {chartData.map(entry => <Cell key={entry.name} fill={entry.color} />)}
                          </Pie>
                          <Tooltip />
                          <Legend />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  ) : <Empty loading={loading} text="No application status data available." />}
                </div>

                <div className="panel">
                  <div className="panel-heading">
                    <div><h3>Risk Intelligence</h3><p>Synthetic anomaly evaluation</p></div>
                    <ShieldAlert size={20} />
                  </div>
                  <div className="risk-score">
                    <span>{metrics?.precision != null ? `${(metrics.precision * 100).toFixed(1)}%` : '—'}</span>
                    <small>Detection precision</small>
                  </div>
                  <div className="metric-row">
                    <span>Recall</span>
                    <strong>{metrics?.recall != null ? `${(metrics.recall * 100).toFixed(1)}%` : '—'}</strong>
                  </div>
                  <div className="metric-row">
                    <span>Accuracy</span>
                    <strong>{metrics?.accuracy != null ? `${(metrics.accuracy * 100).toFixed(1)}%` : '—'}</strong>
                  </div>
                  <div className="metric-row">
                    <span>Ground truth cases</span>
                    <strong>{metrics?.ground_truth_cases?.toLocaleString('en-IN') ?? '—'}</strong>
                  </div>
                  <p className="footnote">Metrics are based on the generated synthetic evaluation dataset.</p>
                </div>
              </div>

              <div className="panel">
                <div className="panel-heading">
                  <div><h3>Recent Loan Applications</h3><p>Latest records in the lending system</p></div>
                  <button className="text-button" onClick={() => setPage('Loan Applications')}>View all</button>
                </div>
                <ApplicationTable rows={applications.slice(0, 6)} money={money} />
              </div>
            </>
          )}

          {page === 'Applicants' && (
            <div className="panel">
              <div className="panel-heading">
                <div><h3>Applicant Directory</h3><p>{applicants.length.toLocaleString('en-IN')} registered applicants</p></div>
                <SearchBox value={search} onChange={setSearch} />
              </div>
              {loading ? <Empty loading /> : (
                <div className="table-wrap">
                  <table>
                    <thead><tr><th>Applicant ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Credit Score</th></tr></thead>
                    <tbody>
                      {filteredApplicants.slice(0, 100).map(a => (
                        <tr key={a.applicant_id}>
                          <td>{a.applicant_id}</td>
                          <td>{`${a.first_name || ''} ${a.last_name || ''}`}</td>
                          <td>{a.email || '—'}</td>
                          <td>{a.phone || '—'}</td>
                          <td>{a.credit_score ?? '—'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {!filteredApplicants.length && <p className="empty-text">No applicants found.</p>}
                </div>
              )}
            </div>
          )}

          {page === 'Loan Applications' && (
            <div className="panel">
              <div className="panel-heading">
                <div><h3>Loan Applications</h3><p>{applications.length.toLocaleString('en-IN')} applications in the system</p></div>
                <SearchBox value={search} onChange={setSearch} />
              </div>
              {loading ? <Empty loading /> : <ApplicationTable rows={filteredApplications.slice(0, 100)} money={money} />}
            </div>
          )}

          {page === 'Risk Intelligence' && (
            <>
              <div className="welcome-row">
                <div><h2>Anomaly Detection Centre</h2><p>Identify inconsistencies and suspicious lending records.</p></div>
                <button className="primary-button" onClick={runScan} disabled={scanning}>
                  <RefreshCw size={16} /> {scanning ? 'Scanning...' : 'Scan Data'}
                </button>
              </div>
              <div className="stats-grid">
                <Stat icon={ShieldAlert} label="Detected Anomalies" value={anomalies.length.toLocaleString('en-IN')} color="orange" />
                <Stat icon={CheckCircle} label="True Positives" value={metrics?.true_positives?.toLocaleString('en-IN') ?? '—'} color="green" />
                <Stat icon={XCircle} label="False Positives" value={metrics?.false_positives?.toLocaleString('en-IN') ?? '—'} color="red" />
                <Stat icon={Clock} label="False Negatives" value={metrics?.false_negatives?.toLocaleString('en-IN') ?? '—'} color="purple" />
              </div>
              <div className="panel">
                <div className="panel-heading"><div><h3>Detected Anomaly Cases</h3><p>Records flagged by the rules-based detection engine</p></div></div>
                <div className="table-wrap">
                  <table>
                    <thead><tr><th>Anomaly ID</th><th>Application ID</th><th>Anomaly Type</th><th>Status</th></tr></thead>
                    <tbody>
                      {anomalies.slice(0, 100).map(a => (
                        <tr key={a.anomaly_id}>
                          <td>{a.anomaly_id}</td><td>{a.application_id}</td>
                          <td>{(a.anomaly_type || '').replaceAll('_', ' ')}</td>
                          <td><span className="status-pill flagged">Detected</span></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {!anomalies.length && <Empty loading={loading} text="No anomalies detected." />}
                </div>
              </div>
            </>
          )}
        </section>
      </main>
    </div>
  )
}

function Stat({ icon: Icon, label, value, color }) {
  return (
    <div className="stat-card">
      <div className={`stat-icon ${color}`}><Icon size={20} /></div>
      <div><p>{label}</p><h2>{value}</h2></div>
    </div>
  )
}

function SearchBox({ value, onChange }) {
  return (
    <div className="search-box">
      <Search size={16} />
      <input value={value} onChange={e => onChange(e.target.value)} placeholder="Search records..." />
    </div>
  )
}

function Empty({ loading, text = 'Loading data...' }) {
  return <p className="empty-text">{loading ? 'Loading data...' : text}</p>
}


function ApplicationTable({ rows, money }) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Application ID</th>
            <th>Applicant ID</th>
            <th>Loan Amount</th>
            <th>Tenure</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(a => {
            const status = a.application_status || a.status || 'Unknown'
            return (
              <tr key={a.application_id}>
                <td>{a.application_id}</td>
                <td>{a.applicant_id}</td>
                <td>{money(Number(a.requested_amount))}</td>
                <td>{a.requested_term_months ? `${a.requested_term_months} months` : '—'}</td>
                <td>
                  <span className={`status-pill ${status.toLowerCase()}`}>
                    {status}
                  </span>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
      {!rows.length && <p className="empty-text">No applications available.</p>}
    </div>
  )
}


export default App
