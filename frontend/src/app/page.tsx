'use client';
import Link from 'next/link';
import Navbar from '../components/Navbar';

export default function Home() {
  return (
    <>
      <Navbar />
      <main className="flex flex-col items-center justify-center min-h-screen">
        <h1 className="text-4xl font-bold mb-4">Welcome to Our prototype</h1>
        <div className="space-x-4">
          <Link href="/login" className="bg-blue-500 text-white px-4 py-2 rounded">
            Login
          </Link>
          <Link href="/signup" className="bg-green-500 text-white px-4 py-2 rounded">
            Signup
          </Link>
        </div>
      </main>
    </>
  );
}
