import './globals.css';

export const metadata = {
  title: 'OdontoBuild',
  description: 'Sistema Operativo Dental',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}