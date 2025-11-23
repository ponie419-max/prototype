'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function EmployeeSection() {
  const [employees, setEmployees] = useState([]);
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    fetch('http://localhost:8000/api/employees', {
      credentials: 'include', // send cookies for session
    })
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch employees');
        return res.json();
      })
      .then(data => setEmployees(data))
      .catch(err => setError(err.message));
  }, []);

  const handleLogout = async () => {
    try {
      await fetch('http://localhost:8000/api/logout', {
        method: 'POST',
        credentials: 'include',
      });
    } catch (err) {
      console.error('Logout failed:', err);
    }
    router.push('/'); // redirect to homepage after logout
  };

  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <header className="flex justify-between items-center mb-4">
        <h1>Employees</h1>
        <button
          onClick={handleLogout}
          className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
        >
          Logout
        </button>
      </header>

      <ul>
        {employees.map((emp) => (
          <li key={emp[0]}>
            {emp[1]} {emp[2]} — {emp[4]} ({emp[5]})
          </li>
        ))}
      </ul>
    </div>
  );
}
