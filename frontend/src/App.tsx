import { useEffect, useState } from 'react';
import { useStore } from './store';
import { authAPI } from './api';
import LoginPage from './components/LoginPage';
import ShichiFukujin from './components/ShichiFukujin';
import SystemStatus from './components/SystemStatus';

function App() {
  const { token, user, login, logout } = useStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in
    const checkAuth = async () => {
      if (token) {
        try {
          const response = await authAPI.getMe();
          login(token, response.data);
        } catch (error) {
          logout();
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center', 
        height: '100vh' 
      }}>
        <h2>Loading Gods Ping...</h2>
      </div>
    );
  }

  if (!user) {
    return <LoginPage />;
  }

  return (
    <>
      <ShichiFukujin />
      <SystemStatus />
    </>
  );
}

export default App;
