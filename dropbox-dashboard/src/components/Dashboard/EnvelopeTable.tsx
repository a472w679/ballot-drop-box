// src/components/Dashboard/EnvelopeTable.tsx
import React from 'react';
import { EnvelopeData } from '../../types';
import { exportCSV } from '../../services/api';

interface EnvelopeTableProps {
  data: EnvelopeData[];
  dropboxId: number;
}

const EnvelopeTable: React.FC<EnvelopeTableProps> = ({ data, dropboxId }) => {
  const handleExportCSV = async () => {
    try {
      const blob = await exportCSV(dropboxId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `dropbox-${dropboxId}-data.csv`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      console.error('Error exporting CSV:', error);
    }
  };

  return (
    <div>
      <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
        <table className="min-w-full text-xs text-black-700 uppercase bg-gray-50">
          <thead>
            <tr className="border-b">
              <th scope="col" className="py-6 px-4">Date</th>
              <th scope="col" className="py-6 px-4">Code 39</th>
              <th scope="col" className="py-6 px-4">IMb</th>
              <th scope="col" className="py-6 px-4">Street Address</th>
              <th scope="col" className="py-6 px-4">City</th>
              <th scope="col" className="py-6 px-4">ZIP Code</th>
              <th scope="col" className="py-6 px-4">Other (status, etc.)</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item) => (
              <tr key={item.id} className="odd:bg-white even:bg-gray-100 border-b border-gray-200">
                <th scope="row" className="py-6 px-4 text-center align-middle">{item.date}</th>
                <td className="py-6 px-4 text-center align-middle">{item.code39}</td>
                <td className="py-6 px-4 text-center align-middle">{item.imb}</td>
                <td className="py-6 px-4 text-center align-middle">{item.streetAddress}</td>
                <td className="py-6 px-4 text-center align-middle">{item.city}</td>
                <td className="py-6 px-4 text-center align-middle">{item.zipCode}</td>
                <td className="py-6 px-4 text-center align-middle">{item.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <button
        onClick={handleExportCSV}
        className="mt-6 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
      >
        Download CSV
      </button>
    </div>
  );
};

export default EnvelopeTable;

export{}