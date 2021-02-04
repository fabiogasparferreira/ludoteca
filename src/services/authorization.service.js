import localStorageService from "@/services/localStorage.service";
import { unauthApi } from "@/services/api";
import router from "@/router";

const URL = "/api/token/";

export default {
  refreshToken,
  doLogin,
  logout,
  isAuthenticated
};

/**
 * Do login with the provided username and password
 * @param username
 * @param password
 * @returns {Promise<AxiosResponse<any>>}
 */
function doLogin(email, password) {
  return unauthApi.post(URL, {
    email: email,
    password: password
  });
}

function logout() {
  localStorageService.clearTokens();
}

/**
 * Call refresh token action, save new access token
 * @returns {Promise<((path: PathLike, mode: (number | undefined), callback: NoParamCallback) => void) | ((path: PathLike, callback: NoParamCallback) => void) | ((path: PathLike, mode?: number) => Promise<void>) | access | "public" | "private" | "protected">}
 */
function refreshToken() {
  // call API to get a new token
  return (
    unauthApi
      .post(URL + "refresh/", {
        refresh: localStorageService.getRefreshToken()
      })
      .then(response => {
        // save new token to LocalStorage
        localStorageService.setAccessToken(response.data.access);
        return Promise.resolve(response.data.access);
      })
      // In case refresh token call returns an error, clear tokens and redirect to login
      .catch(() => {
        //localStorageService.clearTokens();
        router.push({ name: "Login" });
      })
  );
}

/**
 * Checks if user is authenticated based on local storage tokens.
 * NOTE: Ideally it would call API to check token (and refresh token, if necessary)
 * @returns {boolean|boolean}
 */
function isAuthenticated() {
  //TODO: Call api to check tokens

  return (
    !!localStorageService.getAccessToken() &&
    !!localStorageService.getRefreshToken()
  );
}
