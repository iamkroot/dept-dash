import React, { Component } from "react";
import { Redirect } from "react-router";

export default class Logout extends Component {
  render() {
    sessionStorage.removeItem("token");
    this.props.setRouterToken(null);
    return <Redirect to="/login" />;
  }
}
