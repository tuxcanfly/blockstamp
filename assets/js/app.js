import React, { Component } from 'react'
import { HashRouter as Router, Route } from 'react-router-dom'; 
import { Switch, Link, IndexRoute, browserHistory } from 'react-router'

import { PageList, PageForm, PageDetail } from './page'

import css from './app.css'

class App extends Component {
  render() {
    return (
      <Router>
          <Switch>
              <Route name="page_new" path='/page/new' component={() => (<PageForm url="/api/pages/" />)} />
              <Route name="page_detail" path='/page/:id' component={PageDetail} />
              <Route name="page_list" path='/' component={() => (<PageList url="/api/pages" />)} />
          </Switch>
      </Router>
    )
  }
}

export default App
