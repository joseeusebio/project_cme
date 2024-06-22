import React from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';

const App = () => {
  return (
    <Router>
      <Switch>
        <Route path="/login" component={Login} />
        <ProtectedRoute path="/" component={Dashboard} />
        <Redirect from="*" to="/" />
      </Switch>
    </Router>
  );
};

export default App;
