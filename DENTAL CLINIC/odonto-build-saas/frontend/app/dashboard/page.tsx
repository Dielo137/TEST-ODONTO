// UBICACIÓN: frontend/app/dashboard/page.tsx
'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const [appointments, setAppointments] = useState<any[]>([]);
  const router = useRouter();

  // 1. Cargar citas al entrar
  useEffect(() => {
    const fetchAppointments = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        router.push('/'); 
        return;
      }
      try {
        const res = await fetch('http://localhost:8000/appointments/', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setAppointments(data);
        }
      } catch (error) {
        console.error("Error cargando citas", error);
      }
    };
    fetchAppointments();
  }, [router]);

  // 2. Función de cerrar sesión
  const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/');
  };

  // 3. Función para pintar cada celda (AQUÍ SOLÍA ESTAR EL ERROR)
  const renderAppointment = (day: number, hour: string) => {
    const appointment = appointments.find(app => {
      const appDate = new Date(app.start_time);
      // Validamos Día y Hora (formato 09, 10, 11...)
      return appDate.getDay() === day && appDate.getHours().toString().padStart(2, '0') === hour;
    });

    if (appointment) {
      return (
        <div className="bg-blue-100 p-2 rounded border-l-4 border-blue-500 text-blue-800 text-xs shadow-sm cursor-pointer hover:bg-blue-200 transition">
          <strong className="block text-blue-900">{appointment.patient_name}</strong>
          <span className="text-blue-600">Control Rutinario</span>
        </div>
      );
    }
    return <div className="hover:bg-gray-50 transition h-full rounded"></div>; 
  };
  
  // 4. El HTML visual
  return (
    <div className="min-h-screen bg-gray-50 flex font-sans text-gray-800">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 text-white p-6 flex flex-col shadow-xl z-10">
        <h2 className="text-2xl font-bold mb-10 flex items-center gap-2 tracking-tight">
           🦷 OdontoBuild
        </h2>
        <nav className="space-y-3 flex-grow">
            <div className="flex items-center gap-3 py-3 px-4 bg-blue-600 rounded-lg shadow-md cursor-pointer font-medium transition-transform transform hover:scale-105">
                📅 Agenda Semanal
            </div>
            <div className="flex items-center gap-3 py-3 px-4 text-slate-400 hover:bg-slate-800 rounded-lg cursor-not-allowed transition">
                👤 Pacientes
            </div>
            <div className="flex items-center gap-3 py-3 px-4 text-slate-400 hover:bg-slate-800 rounded-lg cursor-not-allowed transition">
                🛡️ Auditoría Legal
            </div>
        </nav>
        <button onClick={handleLogout} className="text-sm text-red-400 mt-8 text-left hover:text-red-300 transition font-semibold">
            ← Cerrar Sesión
        </button>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-y-auto">
        <header className="flex justify-between items-center mb-8 bg-white p-4 rounded-xl shadow-sm border border-gray-100">
            <div>
                <h1 className="text-2xl font-bold text-gray-800">Agenda Clínica</h1>
                <p className="text-sm text-gray-500">Semana del 15 de Diciembre, 2025</p>
            </div>
            <div className="flex items-center gap-3">
                <div className="text-right mr-2">
                    <p className="text-sm font-bold text-gray-900">Dr. Gregory House</p>
                    <p className="text-xs text-green-600 font-medium bg-green-50 px-2 py-0.5 rounded-full inline-block">● Disponible</p>
                </div>
                <div className="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-700 font-bold border border-blue-200">
                    GH
                </div>
            </div>
        </header>

        <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
            {/* Encabezados */}
            <div className="grid grid-cols-6 gap-0 bg-gray-50 border-b border-gray-200">
                <div className="py-4 text-center text-xs font-bold text-gray-400 uppercase tracking-wider border-r">Hora</div>
                <div className="py-4 text-center text-sm font-semibold text-gray-700 border-r">LUN 15</div>
                <div className="py-4 text-center text-sm font-semibold text-gray-700 bg-blue-50/50 border-r">MAR 16</div> 
                <div className="py-4 text-center text-sm font-semibold text-gray-700 border-r">MIE 17</div>
                <div className="py-4 text-center text-sm font-semibold text-gray-700 border-r">JUE 18</div>
                <div className="py-4 text-center text-sm font-semibold text-gray-700">VIE 19</div>
            </div>
            
            {/* Filas */}
            <div className="divide-y divide-gray-100">
                {/* 09:00 */}
                <div className="grid grid-cols-6 gap-0 h-24">
                    <div className="text-gray-400 text-xs font-bold flex items-center justify-center border-r bg-gray-50/50">09:00</div>
                    <div className="border-r p-1"></div>
                    <div className="border-r p-1 bg-blue-50/30">
                        {renderAppointment(2, '09')} {/* Martes 09:00 */}
                    </div>
                    <div className="border-r p-1"></div>
                    <div className="border-r p-1"></div>
                    <div className="p-1"></div>
                </div>

                {/* 10:00 */}
                <div className="grid grid-cols-6 gap-0 h-24">
                    <div className="text-gray-400 text-xs font-bold flex items-center justify-center border-r bg-gray-50/50">10:00</div>
                    <div className="border-r p-1"></div>
                    <div className="border-r p-1 bg-blue-50/30"></div>
                    <div className="border-r p-1"></div>
                    <div className="border-r p-1"></div>
                    <div className="p-1"></div>
                </div>
                
                {/* 11:00 */}
                <div className="grid grid-cols-6 gap-0 h-24">
                    <div className="text-gray-400 text-xs font-bold flex items-center justify-center border-r bg-gray-50/50">11:00</div>
                    <div className="border-r p-1"></div>
                    <div className="border-r p-1 bg-blue-50/30"></div>
                    <div className="border-r p-1"></div>
                    <div className="border-r p-1"></div>
                    <div className="p-1">
                         {renderAppointment(5, '11')} {/* Viernes 11:00 */}
                    </div>
                </div>
            </div>
        </div>
      </main>
    </div>
  );
}