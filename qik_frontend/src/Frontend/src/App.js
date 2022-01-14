import './App.css';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import QikRepository from './Table/qik-repository-index';
import QikResult from './Table/qik-results-index';
import DemoQueryBuilder from './QueryBuilder/demo';
import KG from './Graph';
import CaseSearch from './Table/case-search-index'

function App() {
  return (
    <div className="App">
      <header className="App-header">
      <Router>
        <div>
          <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <ul className="navbar-nav mr-auto">
            <li><Link to={'/'} className="nav-link"> QIK Results </Link></li>
            <li><Link to={'/case-search'} className="nav-link">Case Search</Link></li>
            <li><Link to={'/qik-repository'} className="nav-link">QIK Repository</Link></li>
          </ul>
          </nav>
          <hr />
          <Switch>
              <Route exact path='/' component={QikResult} />
              <Route path='/qik-repository' component={QikRepository} />
              <Route path='/query-builder' component={DemoQueryBuilder} />
              <Route path='/knowledge-graph' component={KG} />
              <Route path='/case-search' component={CaseSearch} />
          </Switch>
        </div>
      </Router>
      </header>
    </div>
  );
}

export default App;
