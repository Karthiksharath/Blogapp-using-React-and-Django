
import { create } from 'zustand';

// used to mount ur store to browser's developer tools
import { mountStoreDevtool } from 'simple-zustand-devtools';


// this particular store is created to manage and store authentication related state in react

const useAuthStore = create((set, get) => ({

    allUserData: null, // Use this to store all user data

    loading: false,

    user: () => ({
        user_id: get().allUserData?.user_id || null,
        username: get().allUserData?.username || null,
    }),


    setUser: (user) => set({ allUserData: user }),

    setLoading: (loading) => set({ loading }),

    isLoggedIn: () => get().allUserData !== null,
}));



// environment variable that checks if the app is running in developemtn mode. if true mount store
if (import.meta.env.DEV) {
    mountStoreDevtool('Store', useAuthStore);
}


export { useAuthStore };
