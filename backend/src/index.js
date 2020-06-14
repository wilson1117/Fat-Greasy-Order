import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App.js';
import BarApp from './components/BarApp.js'
import OrderCard from './components/OrderCard.js'
import NewOrder from './components/NewOrder.js'
import * as serviceWorker from './serviceWorker';

ReactDOM.render(
  <React.StrictMode>
    <BarApp/>
    <OrderCard/>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
