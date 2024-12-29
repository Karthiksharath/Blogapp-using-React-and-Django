import { useEffect, useState } from 'react';
import { setUser } from '../utils/auth';

const MainWrapper = ({ children }) => {

    const [loading, setLoading] = useState(true);

    
    useEffect(() => {
        
        const handler = async () => {
            
            setLoading(true);

            //  asynchronous user authentication action
            await setUser();

            // Set the 'loading' state to 'false' to indicate the loading process has completed
            setLoading(false);
        };

        // Call the 'handler' function immediately after the component is mounted
        handler()
    }, []);

    // Render content conditionally based on the 'loading' state
    return <>{loading ? null : children}</>;
};

export default MainWrapper;
