import React, { Component } from "react";
import { Redirect } from "react-router";
import { GoogleLogin } from "react-google-login";
import { getToken, checkToken } from "../utils/jwt";

export default class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      authenticated: checkToken(),
      failed: false
    };
  }
  render() {
    let googleSucess = data => {
      getToken(data.tokenObj.access_token, (err, token) => {
        if (err) {
          return this.setState({
            failed: true
          });
        }
        this.props.setRouterToken(token);
        this.setState({ authenticated: true });
      });
    };
    let googleFailure = data => {
      this.setState({
        failed: true
      });
    };
    if (this.state.authenticated)
      return <Redirect to="/" />;
    return <div>
      <GoogleLogin
        clientId="102664725186-6k754cqieqagh8ia3sfi8b2666uifrl7.apps.googleusercontent.com"
        onSuccess={googleSucess}
        onFailure={googleFailure}
        theme="dark"
        icon={false}
        buttonText="Login with BITSMail"
      />
      {this.state.failed && <font color="red">Account not found.</font>}
    </div>
  }
}
