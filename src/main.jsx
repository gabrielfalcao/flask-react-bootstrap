import React from 'react'
import { render } from 'react-dom'

// First we import some components...
import { Router, Route, Link } from 'react-router'
import { Input, Panel, Button, Navbar, NavBrand, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';


import  '../styles/app.less'

var jQuery = require('jquery');
var io = require('socket.io-client');
var socket = io.connect('http://' + document.domain + ':' + location.port);
var connections = [];

// Then we delete a bunch of code from App and
// add some <Link> elements...
const App = React.createClass({
    getInitialState(){
	return {stdout: []};
    },
    askForConsole(){
        console.log("ask for ping " + (new Date()).toUTCString());
        socket.emit('publisher_spawn', {date: (new Date()).toUTCString});
    },
    render() {
        socket.on('connect', function(){
            socket.emit("hello", {connection_attempt: connections.length});
            socket.emit("zeromq");
        })
        socket.on('ready', function(data){
            jQuery("#recv").text("Socket.IO connected to Flask at "+ data.ready);
            console.log("READY");
        });
        socket.on('zeromq', function(response){
            var data = response.data;
            switch (response.topic) {
                case "in":
                    var parts = [
                        "[from client: ", data.client_id, "]",
                        " ",
                        data.message
                    ];
                    jQuery("#zeromq-in-container").prepend(parts.join("") + "\n");
                    break;

                case "out":
                    var parts = [
                        "[from server: ", data.server_id, "]",
                        " ",
                        data.message
                    ];
                    jQuery("#zeromq-out-container").prepend(parts.join("") + "\n");
                    break;
                default:
                    jQuery("#zeromq-default-container").prepend(JSON.stringify(data));
            }

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
                    <div className="col-md-6">
                        <Panel header="monitor in" bsStyle="success">
                            <pre id="zeromq-in-container"></pre>
                        </Panel>
                    </div>
                    <div className="col-md-6">
                        <Panel header="monitor out" bsStyle="danger">
                            <pre id="zeromq-out-container"></pre>
                        </Panel>
                    </div>
                    <div className="col-md-12">
                        <Panel header="monitor extra" bsStyle="info">
                            <pre id="zeromq-default-container"></pre>
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
