// Import the Axios library to make HTTP requests.
import axios from 'axios';

// Create an instance of Axios and store it in the 'apiInstance' variable. This instance will have specific configuration options.
const apiInstance = axios.create({
    
    baseURL: 'http://127.0.0.1:8000/api/v1/',

    timeout: 50000, 

    // Define headers that will be included in every request made using this instance. This is common for specifying the content type and accepted response type.
    headers: {
        'Content-Type': 'application/json', // The request will be sending data in JSON format.
        Accept: 'application/json', // The request expects a response in JSON format.
    },
});

export default apiInstance;
