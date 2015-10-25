import React from 'react'
import { render } from 'react-dom'

// First we import some components...
import { Router, Route, Link } from 'react-router'
import { Input, Panel, Button, Navbar, NavBrand, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';


import  '../styles/app.less'

var jQuery = require('jquery');
var io = require('socket.io-client');
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Then we delete a bunch of code from App and
// add some <Link> elements...
const App = React.createClass({
    getInitialState(){
	return {stdout: []};
    },
    onShellReceived(stdout) {
        if (stdout.clear) {
            jQuery("#recv").empty();
        }
        jQuery("#recv").append(stdout.line);
    },
    askForConsole(){
        socket.emit('ping', {domain: 'google.com'});
    },
    render() {
        socket.on('connect', function(){
            socket.emit("hello", {data: "React is ready!"});
        })
            socket.on('ready', function(data){
                jQuery("#recv").text("Socket.IO connected to Flask at "+ data.ready);
                console.log("READY");
            });

        socket.on('shell', this.onShellReceived);
        return (
            <div className="container-fluid">
                <Navbar>
                    <NavBrand>Flask ReactJS</NavBrand>
                    <Nav>
                        <NavItem eventKey={1} href="#">with a hint of Socket.IO and ZeroMQ</NavItem>
                    </Nav>
                </Navbar>

                <div className="row">
                    <div className="col-md-12">

                        <h3>Socket IO baby</h3>
                        <div className="col-md-8">
                            <Panel header="Stuff coming from Flask" bsStyle="primary">
                                <pre id="recv">waiting</pre>
                            </Panel>
                        </div>
                        <div className="col-md-4">
                            <Panel header="Send stuff to Flask" bsStyle="info">
                                <Button bsStyle="warning" onClick={this.askForConsole}>ping google.com</Button>
                            </Panel>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
})

    jQuery(function(){
        render((
            <Router>
                <Route path="/" component={App}>
                </Route>
            </Router>
        ), document.getElementById('app-container'))
    }, 1000);
