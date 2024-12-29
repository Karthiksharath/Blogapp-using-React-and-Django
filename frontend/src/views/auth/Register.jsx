import React, { useState } from "react";
import Header from "../partials/Header";
import Footer from "../partials/Footer";
import { Link, useNavigate } from "react-router-dom";

import { register } from "../../utils/auth"; // Ensure this function is correctly defined and imported
import { useAuthStore } from "../../store/auth";

function Register() {
    const [bioData, setBioData] = useState({ full_name: "", email: "", password: "", password2: "" });
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null); // To store error messages
    const navigate = useNavigate();

    const handleBioDataChange = (event) => {
        setBioData({
            ...bioData,
            [event.target.name]: event.target.value,
        });
    };

    const resetForm = () => {
        setBioData({
            full_name: "",
            email: "",
            password: "",
            password2: "",
        });
    };

    // Check if the form is valid
    const isValidEmail = /^\S+@\S+\.\S+$/.test(bioData.email);
    const isFormValid = bioData.password === bioData.password2 && isValidEmail;

    const handleRegister = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null); // Reset error state before trying to register

        // Validate passwords match
        if (bioData.password !== bioData.password2) {
            setError("Passwords do not match!");
            setIsLoading(false);
            return;
        }

        // Register the user
        const { error } = await register(bioData.full_name, bioData.email, bioData.password, bioData.password2);
        if (error) {
            setError(error.message || "An error occurred. Please try again.");
            console.log(error);
            resetForm();
        } else {
            navigate("/"); // Navigate to home page after successful registration
        }

        setIsLoading(false); // Reset loading state
    };

    return (
        <>
            <Header />
            <section className="container d-flex flex-column vh-100" style={{ marginTop: "150px" }}>
                <div className="row align-items-center justify-content-center g-0 h-lg-100 py-8">
                    <div className="col-lg-5 col-md-8 py-8 py-xl-0">
                        <div className="card shadow">
                            <div className="card-body p-6">
                                <div className="mb-4">
                                    <h1 className="mb-1 fw-bold">Sign up</h1>
                                    <span>
                                        Already have an account?
                                        <Link to="/login/" className="ms-1">
                                            Sign In
                                        </Link>
                                    </span>
                                </div>
                                {/* Form */}
                                <form className="needs-validation" onSubmit={handleRegister}>
                                    {/* Full Name */}
                                    <div className="mb-3">
                                        <label htmlFor="full_name" className="form-label">
                                            Full Name
                                        </label>
                                        <input
                                            type="text"
                                            onChange={handleBioDataChange}
                                            value={bioData.full_name}
                                            id="full_name"
                                            className="form-control"
                                            name="full_name"
                                            placeholder="John Doe"
                                            required
                                        />
                                    </div>
                                    
                                    {/* Email */}
                                    <div className="mb-3">
                                        <label htmlFor="email" className="form-label">
                                            Email Address
                                        </label>
                                        <input
                                            type="email"
                                            onChange={handleBioDataChange}
                                            value={bioData.email}
                                            id="email"
                                            className="form-control"
                                            name="email"
                                            placeholder="johndoe@gmail.com"
                                            required
                                        />
                                    </div>

                                    {/* Password */}
                                    <div className="mb-3">
                                        <label htmlFor="password" className="form-label">
                                            Password
                                        </label>
                                        <input
                                            type="password"
                                            onChange={handleBioDataChange}
                                            value={bioData.password}
                                            id="password"
                                            className="form-control"
                                            name="password"
                                            placeholder="**************"
                                            required
                                        />
                                    </div>

                                    {/* Confirm Password */}
                                    <div className="mb-3">
                                        <label htmlFor="password2" className="form-label">
                                            Confirm Password
                                        </label>
                                        <input
                                            type="password"
                                            onChange={handleBioDataChange}
                                            value={bioData.password2}
                                            id="password2"
                                            className="form-control"
                                            name="password2"
                                            placeholder="**************"
                                            required
                                        />
                                    </div>

                                    {/* Error message */}
                                    {error && <div className="alert alert-danger">{error}</div>}

                                    {/* Submit Button */}
                                    <div>
                                        <div className="d-grid">
                                            <button
                                                className="btn btn-primary w-100"
                                                type="submit"
                                                disabled={isLoading || !isFormValid}
                                            >
                                                {isLoading ? (
                                                    <>
                                                        <span className="mr-2">Processing...</span>
                                                        <i className="fas fa-spinner fa-spin" />
                                                    </>
                                                ) : (
                                                    <>
                                                        <span className="mr-2">Sign Up</span>
                                                        <i className="fas fa-user-plus" />
                                                    </>
                                                )}
                                            </button>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <Footer />
        </>
    );
}

export default Register;
