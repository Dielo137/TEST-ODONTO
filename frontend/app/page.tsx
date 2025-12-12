// Archivo: frontend/app/page.tsx
'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
        const res = await fetch('http://localhost:8000/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ username: email, password: password }),
        });
        if (res.ok) {
            const data = await res.json();
            localStorage.setItem('token', data.access_token);
            router.push('/dashboard'); // <--- Esto te enviará al Dashboard con el token
        } else {
            alert('Credenciales incorrectas');
        }
    } catch (err) {
        alert('Error de conexión con el servidor');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 font-sans">
      <div className="bg-white p-8 rounded-xl shadow-lg w-96 border-t-4 border-blue-600">
        <div className="flex justify-center mb-6">
            <span className="text-4xl">🦷</span>
        </div>
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-2">OdontoBuild</h1>
        <p className="text-center text-gray-500 mb-6 text-sm">Sistema Operativo Dental Seguro</p>
        
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Email Corporativo</label>
            <input 
              type="email" value={email} onChange={(e) => setEmail(e.target.value)}
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
              placeholder="admin@dental.cl" required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Contraseña</label>
            <input 
              type="password" value={password} onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
              required
            />
          </div>
          <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition">
            Ingresar al Sistema
          </button>
        </form>
        <div className="mt-4 text-center text-xs text-gray-400 border-t pt-4">
            Protegido por Ley 21.663
        </div>
      </div>
    </div>
  );
}