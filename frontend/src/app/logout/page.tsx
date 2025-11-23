'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function LogoutPage() {
  const router = useRouter();

  useEffect(() => {
    async function logout() {
      try {
        await fetch('http://localhost:8000/api/logout', {
          method: 'POST',
          credentials: 'include',
        });
      } catch (err) {
        console.error('Logout failed:', err);
      }
      router.push('/'); // Redirect after logout
    }
    logout();
  }, [router]);

  return (
    <main className="flex justify-center items-center min-h-screen">
      <p>Logging out...</p>
    </main>
  );
}
