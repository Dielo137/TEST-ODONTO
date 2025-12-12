// UBICACIÓN: frontend/app/site/[domain]/page.tsx
'use client';
import { useEffect, useState } from 'react';
import { Phone, MapPin, Calendar } from 'lucide-react';

// --- COMPONENTE WIDGET (El cuadro de la derecha) ---
const BookingWidget = ({ doctors, primaryColor }: { doctors: any[], primaryColor: string }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
      <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
        <Calendar className="mr-2" size={24} style={{ color: primaryColor }} />
        Agenda tu Cita Online
      </h3>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Selecciona Profesional</label>
          <select className="mt-1 block w-full p-2 border border-gray-300 rounded-md">
            {doctors.map((doc: any, i: number) => <option key={i}>{doc.full_name}</option>)}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Fecha Preferida</label>
          <input type="date" className="mt-1 block w-full p-2 border border-gray-300 rounded-md" />
        </div>
        <button 
          style={{ backgroundColor: primaryColor }}
          className="w-full text-white font-bold py-3 px-4 rounded-lg hover:opacity-90 transition-opacity"
        >
          Buscar Horas
        </button>
      </div>
    </div>
  );
};

// --- PÁGINA PÚBLICA PRINCIPAL ---
export default function PublicSitePage({ params }: { params: { domain: string } }) {
  const [siteData, setSiteData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // 1. Fetch de datos PÚBLICOS (Sin Token)
  useEffect(() => {
    const fetchSiteData = async () => {
      try {
        // Decodificamos el dominio por si el navegador pone %20 u otros caracteres
        const domain = decodeURIComponent(params.domain);
        const res = await fetch(`http://localhost:8000/public/sites/${domain}`);
        
        if (res.ok) {
          const data = await res.json();
          setSiteData(data);
        } else {
          setSiteData({ error: 'Sitio no encontrado' });
        }
      } catch (error) {
        console.error(error);
        setSiteData({ error: 'Error de conexión' });
      } finally {
        setLoading(false);
      }
    };
    fetchSiteData();
  }, [params.domain]);

  // 2. Lógica de Imágenes (Demo Visual)
  const getHeroImage = (domain: string) => {
    if (domain.includes('sonrisa')) return "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=1200&q=80";
    if (domain.includes('dental')) return "https://images.unsplash.com/photo-1606811841689-23dfddce3e95?auto=format&fit=crop&w=1200&q=80";
    return "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=1200&q=80";
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center text-gray-500">Cargando experiencia...</div>;
  if (siteData?.error) return <div className="min-h-screen flex items-center justify-center text-red-500 font-bold">Error: {siteData.error}</div>;

  // 3. Renderizado del Sitio
  return (
    <div className="bg-gray-50 min-h-screen font-sans">
      {/* HEADER DINÁMICO */}
      <header className="relative h-80 flex items-center justify-center text-center text-white">
          <div 
            className="absolute inset-0 bg-cover bg-center z-0 transition-all duration-1000" 
            style={{ backgroundImage: `url(${getHeroImage(params.domain)})` }}
          />
          <div className="absolute inset-0 bg-black/50 z-10" /> 
          
          <div className="relative z-20 container mx-auto px-6">
            <h1 className="text-5xl font-extrabold drop-shadow-lg mb-2">{siteData.clinic_name}</h1>
            <p className="text-xl font-light opacity-90">{siteData.config.welcome_text}</p>
          </div>
      </header>
      
      {/* BARRA DE COLOR CORPORATIVO */}
      <div style={{ height: '8px', backgroundColor: siteData.config.primary_color }} />

      <main className="container mx-auto px-6 py-12 grid grid-cols-1 lg:grid-cols-3 gap-12">
        {/* Columna Izquierda: Staff e Info */}
        <div className="lg:col-span-2 space-y-12">
          <section>
            <h2 className="text-2xl font-bold text-gray-800 border-b-2 pb-2 mb-6" style={{borderColor: siteData.config.primary_color}}>
              Nuestros Especialistas
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {siteData.doctors.map((doctor: any, index: number) => (
                <div key={index} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
                  <div className="h-12 w-12 rounded-full bg-gray-200 flex items-center justify-center text-xl">👨‍⚕️</div>
                  <div>
                    <p className="font-bold text-gray-800">{doctor.full_name}</p>
                    <p className="text-sm text-gray-500">Odontología General</p>
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section>
             <h2 className="text-2xl font-bold text-gray-800 border-b-2 pb-2 mb-6" style={{borderColor: siteData.config.primary_color}}>
               Contacto
             </h2>
             <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 space-y-4">
                <p className="flex items-center text-gray-700">
                  <MapPin size={20} className="mr-3" style={{color: siteData.config.primary_color}}/> 
                  {siteData.address}
                </p>
                <p className="flex items-center text-gray-700">
                  <Phone size={20} className="mr-3" style={{color: siteData.config.primary_color}}/> 
                  {siteData.phone}
                </p>
             </div>
          </section>
        </div>

        {/* Columna Derecha: Widget */}
        <div className="lg:col-span-1">
          <div className="sticky top-8">
            <BookingWidget doctors={siteData.doctors} primaryColor={siteData.config.primary_color} />
            <p className="text-center text-gray-400 text-xs mt-4">Powered by OdontoBuild SaaS</p>
          </div>
        </div>
      </main>
    </div>
  );
}