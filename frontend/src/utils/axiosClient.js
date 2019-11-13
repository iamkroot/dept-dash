const axios = require("axios");

let axiosMethod = (method, others) => {
  let options = {
    method,
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem("token")}`
    },
    ...others
  };
  return axios(options);
};

export const axiosGET = url => axiosMethod("GET", { url });
export const axiosPOST = (url, data) => axiosMethod("POST", { url, data });
export const axiosDELETE = url => axiosMethod("DELETE", { url });
