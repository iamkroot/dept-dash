const axios = require("axios");
const jwtDecode = require("jwt-decode");

let getToken = (accessToken, callback) => {
  axios
    .post("/api/auth/google-oauth2/", { access_token: accessToken })
    .then(res => {
      if (res.status === 200) {
        sessionStorage.setItem("token", res.data.token);
        callback(null, res.data.token);
      } else {
        callback(res.data, null);
      }
    })
    .catch(err => {
      callback(err, null);
    });
};

let checkToken = () => {
  try {
    let decoded = jwtDecode(sessionStorage.getItem("token"));
    return decoded.exp * 1000 > +new Date();
  } catch (err) {
    return false;
  }
};

let getDecodedToken = () => {
  try {
    return jwtDecode(sessionStorage.getItem("token"));
  } catch (e) {
    return null;
  }
};

module.exports = {
  getToken,
  checkToken,
  getDecodedToken
};
