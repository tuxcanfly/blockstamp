import React, { Component } from 'react'
import { HashRouter as Router, Route } from 'react-router-dom'; 
import { Switch, Link, IndexRoute, browserHistory } from 'react-router'

import { PageForm, PageDetail } from './page'

class App extends Component {
  render() {
    return (
      <Router>
          <Switch>
              <Route name="page_detail" path='/page/:id' component={PageDetail} />
              <Route name="index" path='/' render={() => (<PageForm url="api/pages/" />)} />
          </Switch>
      </Router>
    )
  }
}

export default App
