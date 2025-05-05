const authErrorMap: { [key: string]: string } = {
    'Invalid login credentials': 'Incorrect email or password. Please try again.',
    'Email not confirmed': 'Please confirm your email address before logging in.',
    'Password should be at least 6 characters.': 'Password must be at least 6 characters long.',
    'User already exists': 'An account with this email already exists. Please log in.',
    // Add more mappings as needed
  };
  
  export function getUserFriendlyErrorMessage(backendErrorMessage: string): string {
    // Return the mapped message or the original message if no mapping exists
    return authErrorMap[backendErrorMessage] || 'An unexpected error occurred. Please try again.';
  }