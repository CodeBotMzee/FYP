/**
 * Authentication utility functions
 * Handles JWT token storage and retrieval
 */

const TOKEN_KEY = 'deepfake_token';
const USER_KEY = 'deepfake_user';

/**
 * Save authentication token to localStorage
 */
export const saveToken = (token) => {
  localStorage.setItem(TOKEN_KEY, token);
};

/**
 * Get authentication token from localStorage
 */
export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

/**
 * Remove authentication token from localStorage
 */
export const removeToken = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
};

/**
 * Save user data to localStorage
 */
export const saveUser = (user) => {
  localStorage.setItem(USER_KEY, JSON.stringify(user));
};

/**
 * Get current user from localStorage
 */
export const getCurrentUser = () => {
  const user = localStorage.getItem(USER_KEY);
  return user ? JSON.parse(user) : null;
};

/**
 * Check if user is authenticated
 * Validates that token exists and is not empty
 */
export const isAuthenticated = () => {
  const token = getToken();
  if (!token || token.trim() === '') {
    return false;
  }
  
  // Basic token format validation (JWT tokens have 3 parts separated by dots)
  const parts = token.split('.');
  if (parts.length !== 3) {
    return false;
  }
  
  return true;
};

/**
 * Logout user (clear all auth data)
 */
export const logout = () => {
  removeToken();
};

/**
 * Auth object with all authentication methods
 */
export const auth = {
  setToken: saveToken,
  getToken,
  removeToken,
  setUser: saveUser,
  getUser: getCurrentUser,
  isAuthenticated,
  logout,
};
