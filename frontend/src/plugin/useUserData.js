import React from "react";
import Cookies from "js-cookie";
import jwtDecode from "jwt-decode";


function useUserData() {
    try {
        let access_token = Cookies.get("access_token");
        let refresh_token = Cookies.get("refresh_token");

        if (access_token && refresh_token) {
            const token = refresh_token;
            const decoded = jwtDecode(token);
            return decoded;
        } else {
            console.log("Access token or refresh token is missing.");
            return undefined;
        }
        
    } catch (error) {
        console.error("An error occurred while retrieving user data:", error);
        return undefined;
    }
}



export default useUserData;
