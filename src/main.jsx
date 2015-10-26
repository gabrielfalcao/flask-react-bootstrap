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
    },
    askForConsole(){
        console.log("ask for ping " + (new Date()).toUTCString());
        socket.emit('publisher_spawn', {date: (new Date()).toUTCString});
    },
    render() {
        socket.on('connect', function(){
            socket.emit("hello", {data: "React is ready!"});
            socket.emit("zeromq");
        })
            socket.on('ready', function(data){
                jQuery("#recv").text("Socket.IO connected to Flask at "+ data.ready);
                console.log("READY");
            });
        socket.on('shell', function(stdout){
            if (stdout.clear) {
                jQuery("#recv").empty();
            }
            jQuery("#recv").append(stdout.line);
        });
        socket.on('zeromq', function(data){
            jQuery("#zeromq-container").append(data);
            socket.emit("zeromq");
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
                    <div className="col-md-8">
                        <h3>socket.io area receiving data</h3>
                        <Panel header="shell output" bsStyle="primary">
                            <pre id="recv">waiting for connection</pre>
                            <pre id="zeromq-container"></pre>
                        </Panel>

                    </div>
                    <div className="col-md-4">
                        <h3>invoke zeromq publisher subprocess</h3>
                        <Panel header="spawn publisher" bsStyle="info">
                            <Button bsStyle="warning" onClick={this.askForConsole}>python publisher.py</Button>
                        </Panel>
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
    })
